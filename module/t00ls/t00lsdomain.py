from module.t00ls.t00lslogin import Session
import random

sess = Session.sess
headers = Session.headers

# 查询结果
search_message = ""

# 查询域名
def searchDomain(formhash, domain_data, seccode):
    global search_message
    try:
        domain_url = "https://www.t00ls.com/domain.html"
        headersDomain = headers.copy()
        headersDomain["Content-Type"] = "application/x-www-form-urlencoded"
        random_domain = random.choice(domain_data)
        search_data = f"domain={random_domain}&formhash={formhash}&querydomainsubmit=%E6%9F%A5%E8%AF%A2&cf-turnstile-response={seccode}"
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
            print("查询成功，但是没有增加TuBi，可能今日已经查询过了～")
            search_message = "查询成功，但是没有增加TuBi，可能今日已经查询过了～"
        else:
            print("查询失败")
            search_message = "查询失败"
        return search_message
    except Exception as e:
        print("查询域名失败，请检查配置")
        return "Error"
