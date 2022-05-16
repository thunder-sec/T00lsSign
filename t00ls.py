import base64
import datetime
import hashlib
import hmac
import json
import random
import time
import re
import urllib
import requests

# 登录信息
username = ""           # 用户名
password = ""           # 密码，md5 32位小写
question_num = ""       # 密保问题
question_answer = ""    # 密保答案
# 密保问题对应值如下
# 0 = 没有安全提问
# 1 = 母亲的名字
# 2 = 爷爷的名字
# 3 = 父亲出生的城市
# 4 = 您其中一位老师的名字
# 5 = 您个人计算机的型号
# 6 = 您最喜欢的餐馆名称
# 7 = 驾驶执照的最后四位数字

# 图鉴识别登录 www.ttshitu.com
TTusername = ""
TTpassword = ""

# 推送设置
pushServer = 0     # 推送开关，0为关闭，1为开启，默认关闭
pushType = ""       # 选择推送方式，目前支持：bark、dingding

# bark data
bark_server_url = ""    # 示例：https://test.com
bark_key = ""           # 从bark app上获取

# dingding data
access_token = ""        # webhook access_token值
secret = ""         # 安全选项选"加签"，secret值

# 请求参数
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127'
}

# 创建session
sess = requests.session()

# 登录函数
def t00ls_login(u_name, u_pass, q_num, q_ans):
    login_data = {
        'action': 'login',
        'username': u_name,
        'password': u_pass,
        'questionid': q_num,
        'answer': q_ans
    }
    response_login = sess.post(
        'https://www.t00ls.com/logging.php?action=login&loginsubmit=yes&floatlogin=yes&inajax=1', data=login_data,
        headers=headers)
    response_member = sess.get("https://www.t00ls.com/checklogin.html", headers=headers)
    findformhash = re.search('formhash=(.+)"', response_member.text)
    formhash = findformhash.group(1)
    if formhash:
        print('用户:', username, '登入成功!')
        return formhash
    else:
        return None


# 签到函数
def t00ls_sign(t00ls_hash):
    sign_data = {'formhash': t00ls_hash, 'signsubmit': "apply"}
    response_sign = sess.post('https://www.t00ls.com/ajax-sign.json', data=sign_data, headers=headers)
    response_json = json.loads(response_sign.text)
    if response_json['status'] == 'success':
        print('签到成功过')
        sign_message = '签到成功，Tubi + 1！'
    elif response_json['message'] == 'alreadysign':
        print('已经签过到了')
        sign_message = '已经签到过了'
    else:
        print('未知问题')
        sign_message = '不知道发生了个啥'
    return sign_message


# 获取域名列表
def getDomain():
    getdomain_data = {"terraceFlag": 3, "pageNum": random.randint(1, 5), "pageSize": 50,
                      "include": {"name": "", "includeStart": "false", "includeEnd": "false"},
                      "exclude": {"name": "", "excludeStart": "false", "excludeEnd": "false"},
                      "minSuffixLength": random.randint(5, 10), "maxSuffixLength": "",
                      "deleteTime": str(datetime.date.today() + datetime.timedelta(days=1)),
                      "isIDN": "false", "myself": "false", "sidx": "delete_time", "order": "asc"}
    headers_getDomain = headers.copy()
    headers_getDomain["Content-Type"] = "application/json;charset=UTF-8"
    url_getDomain = "https://ym.longming.com/list/pre"
    rep_jsondata = json.loads(requests.post(url=url_getDomain, headers=headers_getDomain, json=getdomain_data).text)
    domain_data = []
    for i in range(50):
        domain_data.append(rep_jsondata["data"]["list"][i]["domain"])
    return domain_data


# 获取验证码并解析
def getSeccode():
    url_getcode = f"https://www.t00ls.com/seccode.php?update={random.randint(1000, 9999)}"
    headersCode = headers.copy()
    headersCode["Referer"] = "https://www.t00ls.com/domain.html"
    response_code = sess.get(url=url_getcode, headers=headersCode)
    code_img = base64.b64encode(response_code.content)
    b64 = code_img.decode()
    if code_img:
        # 用图鉴进行识别
        TT_data = {"username": TTusername, "password": TTpassword, "image": b64, "typeid": 7}
        url_TT = "http://api.ttshitu.com/predict"
        result = json.loads(requests.post(url=url_TT, json=TT_data, timeout=30).text)
        if result["success"]:
            return result["data"]["result"]
        else:
            print("识别失败")
            return "false"
    else:
        print("验证码获取失败！")


# 查询域名
def searchDomain(formhash, domain_data, seccode):
    domain_url = "https://www.t00ls.com/domain.html"
    headersDomain = headers.copy()
    headersDomain["Content-Type"] = "application/x-www-form-urlencoded"
    random_domain = random.choice(domain_data)
    search_data = f"domain={random_domain}&formhash={formhash}&querydomainsubmit=%E6%9F%A5%E8%AF%A2&seccodeverify={seccode}"
    response_domain = sess.post(url=domain_url, data=search_data, headers=headersDomain, timeout=40).text
    if "已完成" in response_domain:
        print("查询域名成功")
        search_message = "查询域名成功"
    elif "验证码不正确" in response_domain:
        print("验证码不正确")
        search_message = "验证码不正确"
    elif "域名不存在或接口有误" in response_domain:
        print("接口错误或者域名不存在")
    elif random_domain in response_domain and "域名不存在或接口有误" not in response_domain:
        print("查询成功，但是没有增加TuBi")
        search_message = "查询成功，但是没有增加TuBi"
    else:
        print("查询失败")
        search_message = "查询失败"
    return search_message


# bark_push
def bark_push(message):
    data = {"title": "t00ls签到", "body": message}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    url = f"{bark_server_url}/{bark_key}/?isArchive=1"
    ret = requests.post(url, json=data, headers=headers, timeout=60)
    print("Bark: " + ret.text)


# dingding_push
def dingding_push(message):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    data = {"msgtype": "text", "text": {"content": message}}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    dingurl = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}&timestamp={timestamp}&sign={sign}"
    requests.post(url=dingurl, headers=headers, json=data, timeout=60)


# 推送函数
def push(message):
    if pushType == 'bark':
        bark_push(message)
    elif pushType == 'dingding':
        dingding_push(message)


def main(event, content):
    response_login = t00ls_login(username, password, question_num, question_answer)
    if response_login:
        sign_message = t00ls_sign(response_login)
        if pushServer == 1:
            push(sign_message)
    if response_login:
        domain_data = getDomain()
        seccode = getSeccode()
        seccode_num = 0
        while seccode_num < 5:
            search_message = searchDomain(response_login, domain_data, seccode)
            if "查询域名成功" in search_message:
                if pushServer == 1:
                    push(search_message)
                seccode_num = 5
            else:
                seccode = getSeccode()
                seccode_num = seccode_num + 1
                time.sleep(random.randint(5, 10))

