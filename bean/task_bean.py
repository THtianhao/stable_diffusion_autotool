class TasksBean:
    def __init__(self):
        self.tasks: list[TaskBean] = []

class TaskBean:
    def __init__(self):
        self.human_model_dir_flag = ""
        self.style_model = ""
        self.base_model_flag = ""
        self.task_merge: TaskMerge = TaskMerge()
        self.task_txt_img: TaskTxt2Img = TaskTxt2Img()

class TaskMerge:
    def __init__(self):
        self.interp_method = "Add difference",
        self.multiplier = 0.9,
        self.checkpoint_format = "ckpt",

class TaskTxt2Img:
    def __init__(self):
        self.prompt = "",
        self.negative_prompt = "",
        self.seed = -1,
        self.cfg_scale = 7,
        self.sampler_index = 'DPM++ 2S a Karras',
        self.steps = 20,
        self.batch_size = 4
