from urllib import request
import lxml.html as lh
import re
import json

url = "http://gift.kyobobook.co.kr/ht/product/detail?barcode=2310030691962"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "교보문고(http://www.kyobobook.co.kr)"
result["product_name"] = doc.find_class("subject")[0].text_content().strip()
result["price"] = doc.find_class("discount-price")[1].text_content().strip().split("\n")[0]
result["ship_fee"] = doc.find_class("delivery-info")[1].text_content().strip().split("\n")[-1].strip()
options = list()
cnt = 0
for elem in doc.find_class("options")[0].iter("option"):
    if cnt ==0:
        cnt += 1
    else:
        option_text = ""
        for text in elem.text_content().split("\n"):
            option_text += text.strip()
        options.append(option_text)
result["option"] = options

print(result)
