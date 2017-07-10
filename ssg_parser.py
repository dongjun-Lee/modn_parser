from urllib import request
import lxml.html as lh
import re
import json

url = "http://emart.ssg.com/item/itemView.ssg?itemId=1000021718070&siteNo=6001&salestrNo=6005"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()
#
try:
    seller_url = "http://emart.ssg.com" + doc.find_class("cdtl_ico_txt")[0].get("href")
    result["seller"] = doc.find_class("cdtl_ico_txt")[0].text_content() + "(" + seller_url + ")"
except:
    seller_url = "이마트(http://emart.ssg.com)"

#
result["product_name"] = doc.find_class("cdtl_info_tit")[0].text_content()
result["price"] = doc.find_class("ssg_price")[0].text_content()
try:
    result["ship_fee"] = doc.find_class("cdtl_txt_info")[0].text_content().strip()
except:
    result["ship_fee"] = doc.find_class("cdtl_delivery_txt")[0].text_content().strip()

try:
    option = dict()
    option_name_p = re.compile("uitemNm:\'([^']*)\'")
    option_names = option_name_p.findall(html)[1:]
    option_price_p = re.compile("bestAmt:\'([^']*)\'")
    option_prices = option_price_p.findall(html)[1:]
    option_qty_p = re.compile("usablInvQty:\'([^']*)\'")
    option_qtys = option_qty_p.findall(html)[1:]

    for i in range(len(option_names)):
        option[option_names[i]] = "{price : " + option_prices[i] + ", qty : " + option_qtys[i] + "}"
    result["option"] = option
except:
    result["option"] = ""

print(result)
