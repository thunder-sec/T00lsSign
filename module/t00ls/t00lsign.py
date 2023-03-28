from module.t00ls.t00lslogin import Session
import json

sess = Session.sess
headers = Session.headers


# 签到函数
def t00ls_sign(t00ls_hash):
    sign_data = {'formhash': t00ls_hash, 'signsubmit': "apply"}
    try:
        response_sign = sess.post('https://www.t00ls.com/ajax-sign.json', data=sign_data,
                                  headers=headers)
        response_json = json.loads(response_sign.text)
        if response_json['status'] == 'success':
            print('签到成功')
            sign_message = '签到成功!'
        elif response_json['message'] == 'alreadysign':
            print('已经签过到了')
            sign_message = '已经签到过了'
        else:
            print('未知问题')
            sign_message = '不知道发生了个啥'
        return sign_message
    except Exception as e:
        print("签到失败")
        return "签到 Error"
