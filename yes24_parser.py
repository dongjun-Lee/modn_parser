from urllib import request
import lxml.html as lh
import re
import json

# url = "http://www.yes24.com/24/goods/40996491"
url = "http://www.yes24.com/24/goods/29410976"
html = request.urlopen(url).read().decode('euc-kr')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "yes24(http://www.yes24.com)"
result["product_name"] = doc.find_class("gd_name")[0].text_content()
result["price"] = doc.find_class("yes_m")[1].text_content()
result["ship_fee"] = doc.find_class("gd_deliCost")[0].find_class("txC_black")[0].text_content()

sale_state = doc.find_class("gd_saleState")[0].text_content()
if sale_state == "판매중":
    result["is_on_sale"] = True
else:
    result["is_on_sale"] = False

# print(doc.find_class("gd_infoLi")[0].find_class("yes_m")[0].text_content().strip() + " hihi")

cnt = 0
point_str = ""
for elem in doc.find_class("gd_infoLi")[0].iter("li"):
    if cnt == 0:
        point_str += elem.text_content().strip()
        cnt += 1
    else:
        point_str += ", " + elem.text_content().strip().split("\n")[0].replace("\r", "")

result["point"] = point_str

for elem in doc.find_class("saleInfoTb")[0].iter("tbody"):
    result["discount"] = elem.text_content().strip().replace(")", ") / ")
    break

option_p = re.compile("\'#options\'\),{(.*)}\);")
option_json = json.loads("{" + option_p.search(html).group(1) + "}")
output_option_dict = dict()

for key, value in option_json.items():
    option_name = key
    option_price = json.loads(value)['opt_salepr']
    output_option_dict[option_name] = option_price

result["option"] = output_option_dict

print(result)
