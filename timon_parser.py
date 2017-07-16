from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.ticketmonster.co.kr/deal/607253754/1040000?coupon_srl=0#content_start"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["product_name"] = doc.find_class("tit")[0].text_content().strip().split("\r\n")[0]
result["seller"] = "티몬고객센터 1544-6240"
for elem in doc.find_class("zzim_area")[0].find_class("detail")[0].iter("span"):
    result["price"] = elem.text_content()

cnt = 0
for elem in doc.find_class("info_box2")[0].iter("li"):
    if cnt == 0:
        cnt += 1
    else:
        result["ship_fee"] = elem.text_content().strip()
        break

try:
    option_p = re.compile("<div id=\"deal_summary\" class=\"blind\">([^<]*)<")
    options = option_p.search(html).group(1).strip().split("\n")
    print(options)
    result["option"] = options
except:
    result["option"] = ""

print(result)
