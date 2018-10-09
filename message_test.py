import json
import pprint
import requests


class WeChat(object):
    def __init__(self):
        self.access_token_url = "https://api.weixin.qq.com/cgi-bin/token?"
        self.params = {
            'grant_type': 'client_credential',
            'appid': 'wx699313dbd53fd72b',  # 公众号appid,按自己实际填写
            'secret': '900596620c53eccf4a53edf67bd8e854',  # 待按自己实际填写
        }
        self.user_lst_url = "https://api.weixin.qq.com/cgi-bin/user/get?"
        pass

    def get_access_token(self):

        response = requests.get(url=self.access_token_url, params=self.params)
        access_token = response.json().get("access_token")
        return access_token

    def get_user_list(self, token):

        payload = {
            "access_token": token,
            "next_openid": None
        }
        response = requests.get(self.user_lst_url, params=payload)
        openid = response.json()
        return openid

    def post_data(self, token):
        data = {
            "touser": "oT9fT02dO-T-qx1Cd91hriVGn6r0",
            "template_id": "UL-IqbOsS3zIn9Qy14qdla1xRgTmktqOj68k98BoxyM",  # 模板ID
            "data": {
                "first": {
                    "value": "尊敬的用户，感谢您的关注和支持！",
                    "color": "#173177"
                },
                "keynote1": {
                    "value": "已完成",
                    "color": "#173177"
                },
                "keynote2": {
                    "value": "2014年5月20日12：24",
                    "color": "#173177"
                },
                "remark": {
                    "value": "感谢您选择我们的服务！",
                    "color": "#173177"
                }
            }
        }
        json_template = json.dumps(data)
        # access_token = self.get_access_token()
        print("access_token--", token)
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + token
        try:
            respone = requests.post(url, data=json_template, timeout=50)
            # 拿到返回值
            errcode = respone.json().get("errcode")
            print("test--", respone.json())
            if errcode == 0:
                print("模板消息发送成功")
            else:
                print("模板消息发送失败")
            return respone.json()
        except Exception as e:
            print("test++", str(e))

    def get_user_info(self, token, user_list):
        user_info_url = "https://api.weixin.qq.com/cgi-bin/user/info?"
        openid = user_list.get("data").get("openid")
        for item in openid:

            payload = {
                "access_token": token,
                "openid": item,
                "lang": "zh_CN"
            }

            response = requests.get(user_info_url, params=payload)
            user_info = response.json()
            if user_info["nickname"] == "马钰 精化快车":
                return user_info

    def user_list_test(self):
        users = "oT9fT01Ywj86PUxJCNAVxpvckQ6w"
        user_list = json.loads(users)
        print(type(user_list))
        print(user_list)


if __name__ == '__main__':
    token = WeChat().get_access_token()
    print(token)
    user_list = WeChat().get_user_list(token)
    result = WeChat().get_user_info(token, user_list)
    # # res = WeChat().post_data(token)
    print(result)
    # WeChat().user_list_test()