# -*- coding: utf-8 -*-
# author: bao

from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger
from config import WeChatConfig
from .messages import (GetUsersOpenid, GetTemplateList, SendTemplateMessage,
                       GetUsersInfo, HelloWorld)

# init blueprint
message = Blueprint("message", __name__)

# init api
api = swagger.docs(Api(message), description="【总览】API文档",
                   **WeChatConfig.ApidocConnfig)


# 服务测试
api.add_resource(HelloWorld, "/test")

# 获取关注用户列表
api.add_resource(GetUsersOpenid, "/users")
api.add_resource(GetTemplateList, "/templates")
api.add_resource(SendTemplateMessage, "/templates/send")
api.add_resource(GetUsersInfo, "/users/info")