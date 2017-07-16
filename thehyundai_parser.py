from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.thehyundai.com/front/pda/itemPtc.thd?slitmCd=2054002993&MainpageGroup=TheDreamDealSub&GroupbannerName=TheDreamDealSub_1"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("prd-title")[0].text_content().strip().split("\r\n")[0]
result["seller"] = doc.find_class("list-info")[0].text_content().strip()
result["price"] = doc.find_class("dis-price")[0].text_content().strip().split("\r\n")[0]
for td in doc.find_class("itemOptBasicInfo")[0].iter("td"):
    result["ship_fee"] = td.text_content().strip()
    break

try:
    option = dict()
    for elem in doc.find_class("depth-opt-list")[0].iter("li"):
        option_name = elem.find_class("opt-name")[0].text_content().strip()
        option_price = elem.find_class("price")[0].text_content().strip()
        option[option_name] = option_price
    result["option"] = option
except:
    result["option"] = ""

print(result)
