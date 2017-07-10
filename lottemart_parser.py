from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.homeplus.co.kr/app.product.GoodDetail.ghs?comm=usr.detail&good_id=121681846"
html = request.urlopen(url).read().decode('euc-kr')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = "홈플러스(http://www.homeplus.co.kr)"

result["product_name"] = doc.find_class("pro-tit")[0].text_content()
result["price"] = doc.find_class("price fc-ty7")[0].text_content()
result["ship_fee"] = "4만원 미만 3천원, 4만원 이상 무료배송"
result["point"] = "훼밀리카드 적립 0.1%~2.0%, OK캐쉬백 적립 0.05%"

try:
    option = list()
    cnt = 0
    for elem in doc.find_class("opt")[0].iter("option"):
        if cnt == 0:
            cnt += 1
        else:
            option.append(elem.text_content().strip())
    result["option"] = option
except:
    result["option"] = ""

print(result)
