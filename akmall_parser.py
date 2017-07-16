from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.akmall.com/goods/GoodsDetail.do?urlpath=B_05_01%400&recopick=4&location=7%400%401012676&goods_id=76482637"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

try:
    for tr in doc.find_class("tbl_type07")[0].iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "A/S 책임자와 전화번호":
                for td in tr.iter("td"):
                    result["seller"] = td.text_content().strip()
                    break
                break
except:
    result["seller"] = "ak몰(http://www.akmall.com)"

result["price"] = doc.find_class("sale")[0].find_class("c_pink")[1].text_content().strip().split("\n")[0]

for elem in doc.find_class("goods_img")[0].iter("h4"):
    result["product_name"] = elem.text_content().strip()
    break

for elem in doc.find_class("deli")[0].iter("span"):
    result["ship_fee"] = elem.text_content().strip()

try:
    result["point"] = "마일리지 " + doc.find_class("layertip")[0].text_content().strip().split("\n")[0] + "점"
except:
    result["point"] = ""

cnt = 0
options = list()
for elem in doc.find_class("group_4")[0].iter("option"):
    if cnt == 0:
        cnt += 1
    else:
        options.append(elem.text_content())
    result["option"] = options

print(result)
