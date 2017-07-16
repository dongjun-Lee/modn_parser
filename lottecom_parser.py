from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.lotte.com/goods/viewGoodsDetail.lotte?goods_no=396540044&infw_disp_no_sct_cd=20&infw_disp_no=5406662&allViewYn=N"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

try:
    for tr in doc.find_class("prd-point")[0].iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "A/S 책임자와 전화번호":
                for td in tr.iter("td"):
                    result["seller"] = td.text_content().strip()
                    break
                break
except:
    result["seller"] = "롯데닷컴(http://www.lotte.com)"

result["product_name"] = doc.find_class("group_tit")[0].text_content()
result["price"] = doc.find_class("after_price")[0].find_class("final")[0].text_content()

cnt = 0
ship_fee = ""
for tr in doc.find_class("prd-point")[1].iter("tr"):
    if cnt == 0:
        cnt += 1
    else:
        for td in tr.iter("td"):
            ship_fee += td.text_content().strip()
            ship_fee += ", "
        break
result["ship_fee"] = ship_fee

try:
    option = dict()
    for elem in doc.find_class("opt_area")[0].iter("li"):
        option_name = elem.find_class("sec01")[0].text_content()
        option_price = elem.find_class("sec02")[0].text_content()
        option_on_sale = elem.find_class("opt_thum")[0].text_content().strip()
        on_sale = True
        if option_on_sale == "품절":
            on_sale = False

        option[option_name] = "{price : " + option_price + ", on_sale : " + str(on_sale) + "}"
    result["option"] = option
except:
    result["option"] = ""

print(result)
