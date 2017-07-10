from urllib import request
import lxml.html as lh
import re
import json
from lxml import etree

# 판매자, 상품이름, 옵션종류 및 종류 별 가격, 배송비
# 품절여부, 혜택, 쿠폰, 카드 할인

url = "http://item.gmarket.co.kr/Item?goodscode=682202592&search_keyword="
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

for elem in doc.find_class("shopurl")[0].iter('strong'):
    result["seller"] = elem.text_content() + "(" + doc.find_class("shopurl")[0].get("href") + ")"

result["product_name"] = doc.find_class("itemtit")[0].text_content()
result["price"] = doc.find_class("price_real")[0].text_content()
result["ship_fee"] = doc.find_class("txt_emp")[0].text_content()
# result["point"] = doc.find_class("cashback")[0].find_class("nav")[0].text_content().split("\n")[0]
result["point"] = doc.find_class("cashback")[0].find_class("nav")[0].text_content().replace("열기", "").strip()


option_p = re.compile("combOptionObj = {(.*)}")
option_json = json.loads("{" + option_p.search(html).group(1) + "}")
result["option"] = option_json
# print(option_json["OptionDepth"])

discount_p = re.compile("OrderSet.Discount = {(.*)};")
discount_json = json.loads("{" + discount_p.search(html).group(1) + "}")
result["discount"] = discount_json
# print(discount_json)

print(result)
