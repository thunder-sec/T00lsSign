import thirdpartylibrary.requests as requests
from module.config import config
import json
import time
import random


# 获取验证码并解析
def get_seccode():
    try:
        postdata = {"clientKey": config.clientKey,
                    "task": {"type": "TurnstileTaskProxyless", "websiteURL": "https://www.t00ls.com/domain.html",
                             "websiteKey": "0x4AAAAAAADUcE7ghOzWNmEe"}, "softId": 0}
        createTaskurl = "https://api.anti-captcha.com/createTask"
        result = json.loads(requests.post(url=createTaskurl, json=postdata, timeout=30).text)
        if result["errorId"] == 0:
            taskId = result["taskId"]
            time.sleep(random.randint(3, 6))
            taskresult = gettaskresult(taskId)
            numbertest = 0
            while numbertest < 5:
                if taskresult["errorId"] == 0 and taskresult["status"] == "ready":
                    token = taskresult["solution"]["token"]
                    return token
                elif taskresult["status"] == "processing":
                    time.sleep(random.randint(3, 6))
                    taskresult = gettaskresult(taskId)
                    numbertest = numbertest + 1
                else:
                    print("getTaskResult失败，检查配置是否错误")
                    return "Error"
        else:
            print("createTask失败，检查是否配置错误")
            return "Error"
    except Exception as e:
        print("获取验证码解析失败")
        return "Error"


def gettaskresult(taskId):
    gettaskresult_data = {"clientKey": config.clientKey, "taskId": taskId}
    gettaskresult_url = "https://api.anti-captcha.com/getTaskResult"
    taskresult = json.loads(requests.post(url=gettaskresult_url, json=gettaskresult_data, timeout=30).text)
    return taskresult
