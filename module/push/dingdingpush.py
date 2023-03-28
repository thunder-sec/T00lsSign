import base64
import hashlib
import hmac
import urllib
from module.config import config
import thirdpartylibrary.requests as requests
import time


# dingding_push
def dingding_push(message):
    try:
        timestamp = str(round(time.time() * 1000))
        secret_enc = config.dingding_Secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, config.dingding_Secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        data = {"msgtype": "text", "text": {"content": message}}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        dingurl = f"https://oapi.dingtalk.com/robot/send?access_token={config.dingding_AccessToken}&timestamp={timestamp}&sign={sign} "
        requests.post(url=dingurl, headers=headers, json=data, timeout=60)
    except:
        print("dingding推送出现问题，请检查配置。")
