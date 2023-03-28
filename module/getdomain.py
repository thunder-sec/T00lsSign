import random
import datetime
import thirdpartylibrary.requests as requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127'
}


# 获取域名列表
def get_domain():
    getdomain_data = {"terraceFlag": 3, "pageNum": random.randint(1, 5), "pageSize": 50,
                      "include": {"name": "", "includeStart": "false", "includeEnd": "false"},
                      "exclude": {"name": "", "excludeStart": "false", "excludeEnd": "false"},
                      "minSuffixLength": random.randint(5, 10), "maxSuffixLength": "",
                      "deleteTime": str(datetime.date.today() + datetime.timedelta(days=1)),
                      "isIDN": "false", "myself": "false", "sidx": "delete_time", "order": "asc"}
    headers_getDomain = headers.copy()
    headers_getDomain["Content-Type"] = "application/json;charset=UTF-8"
    url_getDomain = "https://ym.longming.com/list/pre"
    try:
        rep_jsondata = json.loads(requests.post(url=url_getDomain, headers=headers_getDomain, json=getdomain_data).text)
        domain_data = []
        for i in range(50):
            domain_data.append(rep_jsondata["data"]["list"][i]["domain"])
        print("域名列表获取成功！")
        return domain_data
    except Exception as e:
        print("域名获取失败")
        return "Error"
