# -*- coding: utf-8 -*-
# author: boe

import datetime
import hmac
import json
import time
import logging
from logging import Formatter
from logging.handlers import SMTPHandler, TimedRotatingFileHandler

from fabric.context_managers import lcd
from flask import Flask, jsonify, request
from flask_mail import Mail
from fabric.api import local


# create app
app = Flask(__name__)

# ---------- Mail settings ------------------------
class MailConfig(object):
    ADMINS = ["421152207@qq.com",]
    MAIL_SERVER = 'smtp.163.com'  # 邮件服务器地址
    MAIL_PORT = 25  # 邮件服务器端口
    MAIL_USERNAME = 'moubo002@163.com'
    MAIL_PASSWORD = 'gogopyth0n'


app.config.from_object(MailConfig)
mail = Mail()
mail.init_app(app)

# ---------- Logger settings ------------------------
mail_handler = SMTPHandler((app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                           app.config["MAIL_USERNAME"], app.config["ADMINS"],
                           "DevOps通知: 自动部署结果",
                           credentials=(app.config["MAIL_USERNAME"],
                                        app.config["MAIL_PASSWORD"]), timeout=20)
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)

# 结果邮件
_msg = """时间: {}
    仓库-分支: {} - {}
    结果：{}"""


# ---------- API service info ------------------------
SERVER_INFO = {
    "wedia-api": {
        "token": "iamtomato",
        "conf": "/etc/supervisor/supervisord.conf",
        "branch": "no_cache",
        "services": ["wedia_serv_test01", "celery_cache_report", "celery_kws_wc", "celery_report_default"],
        "path": "/www/wedia-api"
    },
    "seed-api": {
        "token": "iamseed",
        "conf": "/etc/supervisor/supervisord.conf",
        "branch": "develop",
        "services": ["seed_serv_test01",],
        "path": "/www/seed/seed-api"
    }
}


# views
@app.route("/test", methods=["GET",])
def test():
    return jsonify({"code": 200, "msg": "success"})


@app.route("/deploy", methods=["POST", ])
def deploy():
    # request.values: 获取所有参数
    # request.form: 获取表单数据
    # request.args: 获取get请求参数
    # request.get_data, get_json: 获取json提交的参数
    _data = request.data
    _data_dict = json.loads(_data)
    _repo = _data_dict["repository"]["name"]
    print("the repo: ", _repo)
    _branch = _data_dict["ref"]

    # 获取headers参数, 校验token
    event = request.headers.get('X-Coding-Event')
    # delivery = request.headers.get('X-Coding-Delivery')
    # webHook_version = request.headers.get('X-Coding-WebHook-Version')
    signature = request.headers.get('X-Coding-Signature')
    sha1 = hmac.new(bytes(SERVER_INFO[_repo]["token"], encoding="utf8"), _data, 'sha1')
    sha1 = sha1.hexdigest()
    calculate_signature = 'sha1=' + sha1

    if not calculate_signature == signature:
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        app.logger.error(_msg.format(now_date, _repo, _branch, "Token错误，取消>自动部署"))
        return jsonify({"code": 400})
    else:
        # 开始更新服务
        if _branch.split("/")[-1] == SERVER_INFO[_repo]["branch"]:
            with lcd(SERVER_INFO[_repo]["path"]):
                print("pull code....")
                try:
                    _pull_cmd = "git pull origin " + SERVER_INFO[_repo]["branch"]
                    local(_pull_cmd)
                except Exception as ex:
                    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    app.logger.error(_msg.format(now_date, _repo, _branch, "pull代码错误: %s" % str(ex)))

                    # 暂停5s
                time.sleep(5)

                # restart server
                try:
                    # 重启服务
                    for serv in SERVER_INFO[_repo]["services"]:
                        local("supervisorctl -c /etc/supervisor/supervisord.conf stop %s" % serv)
                        time.sleep(1)
                        local("supervisorctl -c /etc/supervisor/supervisord.conf start %s" % serv)
                except Exception as ex:
                    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    app.logger.error(_msg.format(now_date, _repo, _branch, "重启服务报错: % s" % str(ex)))
        else:
            print("Exit..")

    return jsonify({"code": 200})


if __name__ == "__main__":
    app.run("0.0.0.0", port=8808, threaded=True)
