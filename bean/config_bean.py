class ConfigBean:
    def __init__(self):
        self.port = ""
        self.host = ""
        self.task_path = ""
        self.operation = 1  # 1为merge 2为 merge+ txt2Img
        self.upload_feishu = 1  # 1 上传 2 不上传
