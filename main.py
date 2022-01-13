import requests
import json
import time
from emailSender import mailTo
from config import toList, my_sender, my_pass

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
    applylist = []
    newList = []
    for i in dataList:
        print(i)
        name = i.get("cell", {}).get("bond_nm")
        # 进展通告日
        progress_dt = i.get("cell", {}).get("progress_dt", "")
        if progress_dt and progress_dt < today:
            break
        # 申购日
        apply_date = i.get("cell", {}).get("apply_date", "")
        # 上市日
        list_date = i.get("cell", {}).get("list_date", "")
        if apply_date and apply_date == today:
            applylist.append(name)
        if list_date and list_date == today:
            newList.append(name)
    if len(applylist) == 0 and len(newList) == 0:
        print("今天没有可申购或上市的可转债")
    else:
        hour = (time.time()+8*60*60) % (24*60*60) / (60*60)
        title = f"{today}投资提醒:"
        content = ""
        if applylist:
            title += f"可转债申购{len(applylist)}支"
            if hour > 12:
                title += ",15点停止申购，请抓紧时间"
            content += f"今日申购：{'，'.join(applylist)}"
        if newList and hour < 12:
            if applylist:
                title += ","
                content += "\n"
            title += f"上市{len(newList)}支"
            content += f"今日上市：{'，'.join(newList)}"
        print(applylist, newList)
        if content != "":
            mailTo(toList, title, content, my_sender, my_pass)
            print("邮件发送成功")
