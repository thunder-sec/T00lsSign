import random
import time
from module.push.push import push
from module.t00ls.t00lsdomain import searchDomain
from module.t00ls.t00lsign import t00ls_sign
from module.t00ls.t00lslogin import t00ls_login
from module.config import config
from module.getdomain import get_domain
from module.getcfresponse import get_seccode
from module.t00ls.t00lstubilog import t00ls_tubilog


def core():
    global search_message
    try:
        response_login = t00ls_login(config.t00ls_UserName, config.t00ls_PassWord, config.t00ls_Question_Num,
                                     config.t00ls_Question_Answer)
        if response_login is not None and response_login != "Error":
            sign_message = t00ls_sign(response_login)
            if config.pushServer == "1":
                push(sign_message)
            else:
                print("推送设置关闭状态，需要开启的话请更改配置文件中的 pushType。")
        else:
            print("登陆失败！")
        if response_login is not None and response_login != "Error":
            domain_data = get_domain()
            seccode = get_seccode()
            seccode_num = 0
            while seccode_num < 5 and seccode != "Error":
                search_message = searchDomain(response_login, domain_data, seccode)
                if "查询域名成功" in search_message:
                    if config.pushServer == "1":
                        push(search_message)
                    seccode_num = 5
                elif t00ls_tubilog():
                    search_message = "今日已经查询过域名，Tubi已经+1～"
                    if config.pushServer == "1":
                        push(search_message)
                    seccode_num = 5
                else:
                    seccode = get_seccode()
                    seccode_num = seccode_num + 1
                    time.sleep(random.randint(5, 10))
    except Exception as e:
        print(e)
