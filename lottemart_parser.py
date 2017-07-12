from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.lottemart.com/product/ProductDetail.do?ProductCD=L000002567665&CategoryID=C001005900010001&socialSeq=&koostYn=N"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "롯데마트몰(http://www.lottemartcom)"

result["product_name"] = doc.find_class("detail-type")[0].text_content()
result["price"] = doc.get_element_by_id("currSellPrcValue").text_content()
# result["ship_fee"] = "4만원 미만 3천원, 4만원 이상 무료배송"
# result["point"] = "훼밀리카드 적립 0.1%~2.0%, OK캐쉬백 적립 0.05%"

print(result)
