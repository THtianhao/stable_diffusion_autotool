import base64

from PIL import Image

from api.feishu_api import FeishuApi

if __name__ == '__main__':
    user_token = "u-1wXA2VyR14VrPXPO68UIVdggkABhk013p0G014k00JUd"
    sheet_token = "shtcn0h4PBTtDFz2xtuIebUXfBd"
    feishu_api = FeishuApi()
    feishu_api.set_token(user_token)
    sheetId = feishu_api.query_sheetId(sheet_token)
    test_value = {
        "valueRange": {
            "range": f"{sheetId}!A1:M1",
            "values": [
                [
                    "效果图1", "效果图2", "效果图3", "效果图4", "人物资源", "风格资源", "提示词", "反向提示词", "采样方式", "采样步数", "CFG Scale",  "seed", "Checkpoint Multiplier"
                ]
            ]
        }
    }
    feishu_api.qut_sheet(sheet_token, test_value)


