import json

import requests

from api.feishu_response import TokenResponse

feishu_base_url = "https://open.feishu.cn/open-apis/auth/v3"
get_access_token = f"{feishu_base_url}/tenant_access_token/internal"

token = ""
session = requests.session()


def getToken(app_id, app_secret):
    payload = {"app_id": app_id, "app_secret": app_secret}
    response = session.post(url=get_access_token, json=payload)
    print(response)
    # dict = json.load(response.)
    # response = TokenResponse(**dict)