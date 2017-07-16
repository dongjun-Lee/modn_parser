from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.galleria.co.kr/item/showItemDtl.do?item_id=5369409&sale_shop_gubun_code=00&sale_shop_id=0&con_code=&search_nm=&search_dispctg_list=&galloc=#"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

product_name_p = re.compile("comp_item_name = \"([^\"]*)\"")
product_name = product_name_p.search(html).group(1)
result["product_name"] = product_name

result["price"] = doc.find_class("t_price")[0].text_content()
result["seller"] = doc.find_class("as_detailbox")[0].text_content().strip().split("\r\n")[0]
result["ship_fee"] = doc.find_class("section")[1].text_content().strip()

options = set()
options_p = re.compile("attr_code_val = \"([^\"]*)\"")
for option in options_p.findall(html):
    options.add(option)
option = dict()
for o in options:
    option[o] = result["price"]
result["option"] = option

print(result)
