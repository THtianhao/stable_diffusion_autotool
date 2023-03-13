import json
from dataclasses import asdict

import requests

from api.feishu_response import TokenResponse
from api.feishu_user_response import UserResponse

feishu_base_url = "https://open.feishu.cn"
get_access_token = f"{feishu_base_url}/open-apis/auth/v3/tenant_access_token/internal"
get_user_token = f"{feishu_base_url}/open-apis/authen/v1/access_token"
get_pre_code = f"{feishu_base_url}/open-apis/authen/v1/index"

token = ""
session = requests.session()

def getToken(app_id, app_secret):
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = session.post(url=get_access_token, json=payload)
    if response.status_code == 200:
        dict = json.loads(response.content)
        bean = TokenResponse(**dict)
        print(bean.tenant_access_token)
        return bean

def getUserToken(code):
    payload = {
        "grant_type": "authorization_code",
        "code": code
    }
    response = session.post(url=get_user_token, json=payload)
    if response.status_code == 200:
        dict = json.loads(response.content)
        bean = UserResponse(**dict)
        print(bean.data.access_token)
        return bean

def getPreCodeUrl():
    return "https://open.feishu.cn/open-apis/authen/v1/index?app_id=cli_a483ea8b94e3100e&redirect_uri=http://127.0.0.1"
