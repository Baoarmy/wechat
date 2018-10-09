# -*- coding:utf-8 -*-
# author: bao
import datetime
import requests
import json
from flask import jsonify
from functools import wraps
from config import WeChatConfig


# 获取access_token
def get_access_token():

    result = dict()
    try:
        # with open("access_token.txt", "r") as f:
        #     content = f.read()
        #     data_dict = json.loads(content.replace("'", '"'))
        #     time = datetime.datetime.strptime(data_dict["time"], '%Y-%m-%d %H:%M:%S')
        #
        # if (datetime.datetime.now() - time).seconds < 7000:
        #     print("未到两小时，从文件读取")
        #     return {"access_token": data_dict["access_token"]}
        # else:
        #     # 超过两小时，重新获取
        #     print("超过两小时，重新获取")

        url = WeChatConfig.Urls["token_url"]
        payload = WeChatConfig.AccessToken

        try:
            respone = requests.get(url, params=payload, timeout=50)
            access_token = respone.json().get("access_token")
            content = "{'access_token':" + "'" + str(access_token) + "'" + ",'time':" + "'" + str(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "'" + "}"
            # 写入文件
            with open("access_token.txt", "w") as f:
                f.write(content)

            result.update({"access_token": access_token})
        except Exception as e:
            result.update({"msg": str(e)})
    except Exception as e:
        result.update({"msg": str(e)})

    return result

# access_token装饰器


def access_token(func):
    @wraps(func)
    def decorate_view(*args, **kwargs):
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return jsonify({"code": 400, "msg": "无有效token，拉取用户列表失败！"})
        return func(*args, **kwargs)
    return decorate_view
