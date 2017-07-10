from urllib import request
import lxml.html as lh
import re
import json

url = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B402422178"
html = request.urlopen(url).read().decode('euc-kr')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = doc.find_class("shop-title")[0].text_content() + "(" + doc.find_class("btn_gostore")[0].get("href") + ")"

result["product_name"] = doc.find_class("itemtit")[0].text_content()
result["price"] = doc.find_class("price_real")[0].text_content()
result["ship_fee"] = doc.find_class("txt_emp")[0].text_content()
result["point"] = doc.find_class("cashback_item")[0].find_class("nav")[0].text_content().replace("열기", "").strip()

option_p = re.compile("ItemRequests=(.*);")
option_json = json.loads(option_p.search(html).group(1))
result["option"] = option_json

result["discount"] = "http://itempage3.auction.co.kr/popup/CreditCardPromotion.html"

print(result)
