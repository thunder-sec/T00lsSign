from module.config import config
import thirdpartylibrary.requests as requests


# bark_push
def bark_push(message):
    try:
        data = {"title": "t00ls签到", "body": message}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        url = f"{config.bark_ServerUrl}/{config.bark_Key}/?isArchive=1"
        ret = requests.post(url, json=data, headers=headers, timeout=60)
        print("Bark: " + ret.text)
    except:
        print("Bark推送出错，请检查bark配置。")
