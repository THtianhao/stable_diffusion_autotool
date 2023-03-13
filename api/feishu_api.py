import json

import requests

from api.feishu_response import TokenResponse
from api.feishu_user_response import UserResponse, UserResponseData
from log_utils import LogUtils

feishu_base_url = "https://open.feishu.cn"
get_access_token = f"{feishu_base_url}/open-apis/auth/v3/tenant_access_token/internal"
get_user_token = f"{feishu_base_url}/open-apis/authen/v1/access_token"
get_pre_code = f"{feishu_base_url}/open-apis/authen/v1/index"
get_refresh_token = f"{feishu_base_url}/open-apis/authen/v1/refresh_access_token"

class FeishuApi:
    def __init__(self, logUtils):
        self.access_token = ""
        self.session = requests.session()
        self.log_utils: LogUtils = logUtils

    def getToken(self, app_id, app_secret):
        payload = {"app_id": app_id, "app_secret": app_secret}
        response = self.session.post(url=get_access_token, json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            bean = TokenResponse(**dict)
            if bean.code == 0:
                self.access_token = bean.tenant_access_token
                self.log_utils.i(f"access token = {self.access_token}")
                return bean
            else:
                self.log_utils.e(f"get access token fail")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def getUserToken(self, code):
        payload = {
            "grant_type": "authorization_code",
            "code": code
        }
        response = self.session.post(url=get_user_token, headers=self.get_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                return bean

    def refresh_user_access_token(self, user_refresh_token):
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": user_refresh_token
        }
        response = self.session.post(url=get_refresh_token, headers=self.get_headers(), json=payload)
        if response.status_code == 200:
            dict = json.loads(response.content)
            if dict['code'] == 0:
                bean = UserResponseData(**dict['data'])
                return bean


    def getPreCodeUrl(self):
        return "https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"
