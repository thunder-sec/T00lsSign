import datetime
from module.t00ls.t00lslogin import Session
from thirdpartylibrary.bs4 import BeautifulSoup

sess = Session.sess
headers = Session.headers


# 获取Tubilog
def t00ls_tubilog():
    try:
        tubilog = sess.get("https://www.t00ls.com/members-tubilog-15186.html", headers=headers).text
        soup = BeautifulSoup(tubilog, 'html.parser')
        tubilist = soup.tbody
        trs = tubilist.find_all("tr")
        for tr in trs:
            date = tr.find_all("td")[1].text
            domainlog = tr.find_all("td")[4].text
            if str(datetime.date.today()) in date and "查询新域名" in domainlog:
                domaindata = True
                break
            else:
                domaindata = False
        return domaindata
    except:
        print("获取Tubilog出现错误。")
        return "Error"
