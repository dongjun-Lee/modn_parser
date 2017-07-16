from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=1241347885&grbyEndDtime=20170716235900&llog=01334_8&dispAdutCd=ec_01334_8"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("dg_tit")[0].text_content().strip()
result["price"] = doc.find_class("price2")[0].text_content().strip().split("~")[0] + "~"

for td in doc.find_class("ntable_02")[0].iter("td"):
    result["ship_fee"] = td.text_content().strip()
    break

try:
    for tr in doc.find_class("ntable_01")[0].iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "A/S 책임자/전화번호":
                for td in tr.iter("td"):
                    result["seller"] = td.text_content().strip()
                    break
                break
except:
    result["seller"] = "롯데i몰(http://www.lotteimall.com)"


try:
    option = dict()
    cnt = 0
    for elem in doc.find_class("addClassOnClick2")[0].iter("li"):
        if cnt == 0:
            cnt += 1
        else:
            option_name = elem.find_class("info")[0].text_content().strip()
            option_price = elem.find_class("price")[0].text_content().strip()
            option[option_name] = option_price
            result["option"] = option
except:
    result["option"] = ""

print(result)
