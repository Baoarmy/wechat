# -*- coding: utf-8 -*-
# author: bao


class WeChatConfig(object):
    """
    # 配置信息
    """
    # ------------------ API文档 settings -------------------------------
    ApidocConnfig = {
        "apiVersion": "0.1",
        "basePath": "http://192.168.75.131",
        "resourcePath": "/",
        "produces": ["application/json", "text/html"],
        "api_spec_url": "/api/spec"
    }

    # 获取access_token信息验证配置
    AccessToken = {
        'grant_type': 'client_credential',
        'appid': 'wx699313dbd53fd72b',  # 公众号appid,按自己实际填写
        'secret': '900596620c53eccf4a53edf67bd8e854',  # 待按自己实际填写
    }

    # 各种url配置
    Urls = {
        "token_url": "https://api.weixin.qq.com/cgi-bin/token?",
        "openid_list_url": "https://api.weixin.qq.com/cgi-bin/user/get?",
        "user_info_url": "https://api.weixin.qq.com/cgi-bin/user/info?",
        "template_message_url": "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}",
        "users_info_url": "https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={}",
        "template_id_url": "https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?",
        "del_template_url": "https://api.weixin.qq.com/cgi-bin/template/del_private_template?access_token={}"
    }

    LOG_PATH = "/root/message/logs/"
