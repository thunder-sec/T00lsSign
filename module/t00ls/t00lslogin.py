import thirdpartylibrary.requests as requests
import re
from module.config import config


class Session:
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
    try:
        Session.sess.post(
            'https://www.t00ls.com/logging.php?action=login&loginsubmit=yes&floatlogin=yes&inajax=1', data=login_data,
            headers=Session.headers)
        response_member = Session.sess.get("https://www.t00ls.com/checklogin.html", headers=Session.headers)
        findformhash = re.search('formhash=(.+)"', response_member.text)
        formhash = findformhash.group(1)
        if formhash:
            print('用户:', config.t00ls_UserName, '登入成功!')
            return formhash
        else:
            return None
    except Exception as e:
        return "Error"
