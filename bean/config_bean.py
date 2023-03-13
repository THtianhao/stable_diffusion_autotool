from dataclasses import dataclass

class ConfigBean:
    def __init__(self, port="", host="", task_path="", operation=1, upload_feishu=2, feishu_code="", refresh_token=""):
        self.port: str = port
        self.host: str = host
        self.task_path: str = task_path
        self.operation: int = operation  # 1为merge 2为 merge+ txt2Img
        self.upload_feishu: int = upload_feishu  # 1 上传 2 不上传
        self.feishu_code: str = feishu_code
        self.refresh_token: str = refresh_token
