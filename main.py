import requests
import json
import time
from emailSender import mailTo
from config import toList

today = time.strftime("%Y-%m-%d")

url = "https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=1628932151970"

data = {
    "progress": "",
    "rp": 22,
    "page": 1,
}

res = requests.post(url, data)
text = res.text
dl = json.loads(text)
dataList = dl.get("rows", [])

if not len(dataList):
    print("数据爬取失败")
else:
    rowlist = []
    for i in dataList:
        date_ = i.get("cell", {}).get("apply_date", "")
        name = i.get("cell", {}).get("bond_nm")
        if date_ and date_ == today:
            rowlist.append(name)
        #elif i.get("cell", {}).get("apply_date", "") < today:
        #    continue
    if not len(rowlist):
        print("今天没有可申购的可转债")
    else:
            mailTo(toList,  f"{today}投资提醒:可转债申购{str(len(rowlist))}支", "\n".join(rowlist))
            print("邮件发送成功")
