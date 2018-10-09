# -*- coding: utf-8 -*-
# author: bao

import requests
import json

from flask_restful import Resource, reqparse
from flask_restful_swagger import swagger
from .utils import get_access_token
from config import WeChatConfig


# test
class HelloWorld(Resource):
    """
    # connecting test
    """
    @swagger.operation(
        notes="测试服务是否可用",
        nickname="get",
        parameters=[],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 404,
                "message": "URL Not Found"
            }
        ]
    )
    def get(self):
        """
        Get a todo task

        说明：如果返回200，则服务可用。否则，服务不可用。
        """
        return {"msg": "Hello, 精化快车!"}


class UserInfoItem(object):
    def __init__(self, user_list):
        pass


class GetUsersOpenid(Resource):
    """
    # 获取关注用户的openid列表
    """

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("page", type=int, default=None)
        self.parser.add_argument("offset", type=int, default=None)
        self.parser.add_argument("user_list", type=str, default="")
        pass

    @swagger.operation(
        notes="获取关注用户的openid列表",
        nickname="get",
        parameters=[
            {
                "name": "page",
                "description": "页码",
                "required": False,
                "dataType": "int",
                "paramType": "query",
                "defaultValue": None
            },
            {
                "name": "offset",
                "description": "每页显示数量",
                "required": False,
                "dataType": "int",
                "paramType": "query",
                "defaultValue": None

            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 404,
                "message": "No Such Articles"
            }
        ]
    )
    def get(self):
        _args = self.parser.parse_args()
        if _args["page"] and _args["offset"]:
            start = (_args["page"] - 1) * _args["offset"]
            end = _args["page"] * _args["offset"]

        # 关注用户openid的url接口
        url = WeChatConfig.Urls["openid_list_url"]
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return {"code": 400, "msg": "无有效token，拉取用户列表失败！"}

        payload = {
            "access_token": access_token["access_token"],
            "next_openid": None
        }

        response = requests.get(url, params=payload)

        return {"code": 200, "data": response.json()}

    @swagger.operation(
        notes="批量获取用户信息",
        nickname="post",
        parameters=[
            {
                "name": "user_list",
                "description": "批量获取用户信息",
                "required": True,
                "dataType": UserInfoItem.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 405,
                "message": "Invalid Input"
            }
        ]
    )
    # 批量获取用户信息
    def post(self):
        _args = self.parser.parse_args()
        if not _args["user_list"]:
            return {"code": 400, "msg": "请传入openid参数"}

        user_list = json.loads(_args["user_list"].replace("'", '"'))
        payload = {"user_list": []}
        for user in user_list:
            tmp = dict()
            tmp["openid"] = user
            tmp["lang"] = "zh_CN"
            payload["user_list"].append(tmp)

        # 获取access_token
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return {"code": 400, "msg": "无有效token，拉取用户列表失败！"}

        url = WeChatConfig.Urls["users_info_url"].format(access_token["access_token"])

        response = requests.post(url, data=json.dumps(payload))

        return {"code": 200, "data": response.json()}


# 获取微信服务号已添加的模板
class GetTemplateList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("tid", type=str, trim=True, default="")

        pass

    @swagger.operation(
        notes="获取已添加的模板消息列表",
        nickname="get",
        parameters=[
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 404,
                "message": "No Such Articles"
            }
        ]
    )
    def get(self):
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return {"code": 400, "msg": "无有效token，拉取用户列表失败！"}

        payload = {
            "access_token": access_token["access_token"]
        }
        url = WeChatConfig.Urls["template_id_url"]
        response = requests.get(url, params=payload)

        return {"code": 200, "data": response.json().get("template_list")}

    @swagger.operation(
        notes="要删除的模板id",
        nickname="delete",
        parameters=[
            {
                "name": "tid",
                "description": "要删除的模板id",
                "required": True,
                "dataType": "string",
                "paramType": "query",
                "defaultValue": ""
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 404,
                "message": "URL Not Found"
            }
        ]
    )
    def delete(self):
        _args = self.parser.parse_args()
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return {"code": 400, "msg": "无有效token，拉取用户列表失败！"}

        url = WeChatConfig.Urls["del_template_url"].format(access_token["access_token"])
        payload = {
            "template_id": _args["tid"]
        }
        response = requests.post(url, data=json.dumps(payload))
        return {"code": 200, "data": response.json()}


@swagger.model
class TemplateMessageItem(object):
    def __init__(self, user, first, keyword1, keyword2, keyword3, keyword4, remark, url):
        pass


# 给所有用户发送模板消息
class SendTemplateMessage(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("title", type=str, trim=True, default="")
        self.parser.add_argument("user", type=str, trim=True, default="")
        self.parser.add_argument("first", type=str, trim=True, default="")
        self.parser.add_argument("keyword1", type=str, trim=True, default="")
        self.parser.add_argument("keyword2", type=str, trim=True, default="")
        self.parser.add_argument("keyword3", type=str, trim=True, default="")
        self.parser.add_argument("keyword4", type=str, trim=True, default="")
        self.parser.add_argument("keyword5", type=str, trim=True, default="")
        self.parser.add_argument("keyword6", type=str, trim=True, default="")
        self.parser.add_argument("remark", type=str, trim=True, default="")
        self.parser.add_argument("url", type=str, trim=True, default="")
        pass

    @swagger.operation(
        notes="发送模板信息",
        nickname="post",
        parameters=[
            {
                "name": "message",
                "description": "发送模板消息",
                "required": True,
                "dataType": TemplateMessageItem.__name__,
                "paramType": "body",
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 405,
                "message": "Invalid Input"
            }
        ]
    )
    def post(self):
        _args = self.parser.parse_args()
        template_id = None
        if not _args["title"]:
            return {"code": 400, "msg": "请输入消息模板名称!"}
        # 获取access_token
        access_token = get_access_token()
        if not access_token.get("access_token", None):
            return {"code": 400, "msg": "无有效token，拉取用户列表失败！"}

        # 获取用户模板template_id
        tmp_payload = {
            "access_token": access_token["access_token"]
        }
        url = WeChatConfig.Urls["template_id_url"]
        response = requests.get(url, params=tmp_payload)
        tmp_list = response.json().get("template_list")
        for item in tmp_list:
            if item["title"] == _args["title"]:
                template_id = item["template_id"]
                break
        if not template_id:
            return {"code": 400, "msg": "所选模板不存在!"}
        # 组装消息内容
        params = {k: {"value": v, "color": "#173177"} for k, v in _args.items() if v}
        if params.get("user", None):
            params.pop("user")
        if params.get("title", None):
            params.pop("title")

        # 传user参数则只向这些用户发送消息
        if _args["user"]:
            users = json.loads(_args["user"].replace("'", '"'))
        else:
            # ---------------------------关注用户openid的列表-------------------------------
            user_url = WeChatConfig.Urls["openid_list_url"]
            payload = {
                "access_token": access_token["access_token"],
                "next_openid": None
            }

            response = requests.get(user_url, params=payload)
            users = response.json().get("data").get("openid")
        # ----------------------------获取用户openid列表结束----------------------------
        result = dict()
        send_failed = list()
        for user in users:
            data = {
                "touser": user,
                "template_id": template_id,  # 模板ID
                "data": params
            }
            if _args["url"]:
                data["url"] = _args["url"]
            json_template = json.dumps(data)
            url = WeChatConfig.Urls["template_message_url"].format(access_token["access_token"])
            try:
                respone = requests.post(url, data=json_template, timeout=50)
                # 拿到返回值
                errcode = respone.json().get("errcode")
                if errcode != 0:
                    send_failed.append(user)
            except Exception as e:
                print(str(e))
                # result.update({"code": 400, "msg": "模板消息发送失败:{}".format(str(e))})
        result.update({"code": 200, "msg": "模板消息发送成功", "发送失败用户": send_failed})

        return result


# 根据用户昵称获取用户信息
class GetUsersInfo(Resource):
    """
    # 获取关注用户的openid列表
    """

    def __init__(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("nickname", type=str, default="")
        pass

    @swagger.operation(
        notes="根据用户昵称获取用户信息",
        nickname="get",
        parameters=[
            {
                "name": "nickname",
                "description": "用户昵称",
                "required": False,
                "dataType": "str",
                "paramType": "query",
                "defaultValue": None

            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "success"
            },
            {
                "code": 404,
                "message": "No Such Articles"
            }
        ]
    )
    def get(self):
        _args = self.parser.parse_args()
        if not _args["nickname"]:
            return {"code": 400, "msg": "请输入用户昵称！"}
        access_token = get_access_token()
        info_url = WeChatConfig.Urls["user_info_url"]
        # ---------------------------关注用户openid的列表-------------------------------
        user_url = WeChatConfig.Urls["openid_list_url"]
        payload = {
            "access_token": access_token["access_token"],
            "next_openid": None
        }

        response = requests.get(user_url, params=payload)
        result = dict()
        try:
            users = response.json().get("data").get("openid")
            # ----------------------------获取用户openid列表结束----------------------------
            data = {}
            i = 1
            for item in users:
                i += 1

                payload = {
                    "access_token": access_token["access_token"],
                    "openid": item,
                    "lang": "zh_CN"
                }

                response = requests.get(info_url, params=payload)
                user_info = response.json()
                if user_info["nickname"] == _args["nickname"]:
                    data = user_info
                    break

            result.update({"code": 200, "data": data})
        except Exception as ex:
            result.update({"code": 400, "data": str(ex)})
        if not result["data"]:
            result["data"] = "不存在此用户"
        return result
