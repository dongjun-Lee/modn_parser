from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.bandinlunis.com/front/product/detailProduct.do?prodId=6836168"
html = request.urlopen(url).read().decode('euc-kr')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "반디앤루니스(http://www.bandinlunis.com)"
for elem in doc.find_class("pDetail")[0].iter("h4"):
    result["product_name"] = elem.text_content().strip()
    break
result["price"] = doc.find_class("price")[0].text_content()
# result["ship_fee"] = doc.find_class("txt_shipping")[0].find_class("tbl_right")[0].text_content().strip()

for elem in doc.find_class("clfix pos_rel")[1].iter("strong"):
    result["point"] = elem.text_content()
    break

for c in doc.find_class("gap"):
    try:
        if c.find_class("pdL")[0].text_content() == "배송비":
            for elem in c.find_class("pdR")[0].iter("strong"):
                result["ship_fee"] = elem.text_content()
                break
    except IndexError:
        pass

cnt = 0
options = list()
for c in doc.find_class("gap"):
    try:
        if c.find_class("pdL")[0].text_content() == "옵션선택":
            for elem in c.find_class("pdR")[0].iter("option"):
                if cnt == 0:
                    cnt += 1
                else:
                    option_text = ""
                    for text in elem.text_content().split("\n"):
                        option_text += text.strip()
                    options.append(option_text)
            break
    except IndexError:
        pass

result["option"] = options

print(result)
