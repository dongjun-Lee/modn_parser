from urllib import request
import lxml.html as lh
import re
import json

# url = "http://www.lottemart.com/product/ProductDetail.do?ProductCD=L000002567665&CategoryID=C001005900010001&socialSeq=&koostYn=N"
url = "http://www.lottemart.com/product/ProductDetail.do?CategoryID=C001002900010016&ProductCD=D000002683360&socialSeq=&koostYn=N&SITELOC=AF001"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("detail-type")[0].text_content()

price_p = re.compile("price\':\'([^']*)\'")
price = price_p.search(html).group(1)
result["price"] = price

seller = ""
for tr in doc.get_element_by_id("tab01").iter("tr"):
    for th in tr.iter("th"):
        if th.text_content() == "A/S책임자 연락처":
            for td in tr.iter("td"):
                seller = td.text_content().strip()
                break
if seller == "":
    result["seller"] = "롯데마트(02-2145-8000)"
else:
    result["seller"] = seller

result["ship_fee"] = "3만원미만:2500원, 3만원이상:무료"

try:
    option = dict()
    for elem in doc.find_class("bundle-list")[0].iter("article"):
        option_name = elem.find_class("prod-name")[0].text_content().strip()
        option_price = elem.find_class("price-strike-type1")[0].text_content().strip()
        option[option_name] = option_price
    result["option"] = option
except:
    result["option"] = ""

print(result)
