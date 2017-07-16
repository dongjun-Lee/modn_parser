from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd=2054673152&MainpageGroup=GoodLuckDeal&GroupbannerName=GoodLuckDeal_2_79549_0714"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("tit")[0].text_content()
result["price"] = doc.find_class("price")[0].find_class("digit")[0].text_content().strip().split("\r\n")[0]
result["ship_fee"] = doc.find_class("productInfoDL mb15")[0].text_content().strip().split("\n")[-1].strip()

for tr in doc.find_class("formTable mt10")[0].iter("tr"):
    for th in tr.iter("th"):
        if th.text_content() == "배송비":
            for td in tr.iter("td"):
                result["ship_fee"] = td.text_content().strip()
                break
        if th.text_content() == "A/S책임자와 전화번호":
            for td in tr.iter("td"):
                result["seller"] = td.text_content().strip()
                break

option = dict()
try:
    for elem in doc.find_class("sstpl_selbox")[0].iter("li"):
        option_name = elem.find_class("info")[0].text_content()
        option_price = elem.find_class("price")[0].text_content()
        option[option_name] = option_price
except:
    pass
result["option"] = option

print(result)
