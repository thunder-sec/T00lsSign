import configparser


class Config:
    def __init__(self):
        configsite = configparser.ConfigParser()
        configsite.read('config.conf', encoding="utf-8")
        self.t00ls_UserName = configsite.get("login", "username").strip()
        self.t00ls_PassWord = configsite.get("login", "password").strip()
        self.t00ls_Question_Num = configsite.get("login", "question_num").strip()
        self.t00ls_Question_Answer = configsite.get("login", "question_answer").strip()
        self.clientKey = configsite.get("anti-captcha", "clientKey").strip()
        self.pushServer = configsite.get("push", "pushServer").strip()
        self.pushType = configsite.get("push", "pushType").strip().lower()
        self.bark_ServerUrl = configsite.get("bark", "bark_ServerUrl").strip()
        self.bark_Key = configsite.get("bark", "bark_Key").strip()
        self.dingding_AccessToken = configsite.get("dingding", "dingding_AccessToken").strip()
        self.dingding_Secret = configsite.get("dingding", "dingding_Secret").strip()


config = Config()
