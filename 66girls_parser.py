from urllib import request
import lxml.html as lh
import json
import re

url = "http://66girls.co.kr/product/detail.html?product_no=57109&cate_no=71&display_group=2"
raw_html = request.urlopen(url).read()
html = raw_html.decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "66걸즈(http://66girls.co.kr/)"
result["ship_fee"] = "50000원 이상 무료배송, 이하 1800원"

for elem in doc.find_class("infoArea")[0].iter("tr"):
    title = elem.text_content().split()[0]
    content = elem.text_content().split()[1]

    if title == "상품명":
        result["product_name"] = content
    elif title == "판매가":
        result["price_real"] = content
    elif title == "적립금":
        result["point"] = content
        break

try:
    html2 = raw_html.decode("unicode_escape")
    option_p = re.compile("option_stock_data = \'{([^']*)}\';")
    option_json = json.loads("{" + option_p.search(html2).group(1) + "}")
    result["option"] = option_json
except AttributeError:
    result["option"] = ""

print(result)