from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.ellotte.com/goods/viewGoodsDetail.lotte?goods_no=358060693&infw_disp_no_sct_cd=20&infw_disp_no=5405984&allViewYn=N"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("group_tit")[0].text_content().strip()
result["price"] = doc.find_class("after_price")[0].text_content().strip().split("~")[0] + "~"

for td in doc.find_class("prd-point")[1].iter("td"):
    result["ship_fee"] = td.text_content().strip()
    break

try:
    for tr in doc.find_class("prd-point")[0].iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "A/S 책임자와 전화번호":
                for td in tr.iter("td"):
                    result["seller"] = td.text_content().strip()
                    break
                break
except:
    result["seller"] = "el롯데(http://www.ellotte.com)"

try:
    option = dict()
    cnt = 0
    for elem in doc.find_class("opt_area")[0].find_class("list thum_list")[0].iter("li"):
        option_name = elem.find_class("sec01")[0].text_content().strip()
        option_price = elem.find_class("sec02")[0].text_content().strip()
        option[option_name] = option_price
        result["option"] = option
except:
    result["option"] = ""

print(result)
