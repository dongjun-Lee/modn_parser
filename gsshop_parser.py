from urllib import request
import lxml.html as lh
import re
import json

url = "http://www.gsshop.com/prd/prd.gs?prdid=26230246&lseq=390802-3&gsid=ECmain-AU390802-AU390802-3&dseq=3&svcid=pc&bnclick=main-mrcm_mainMrcmB_UrmPopularDealTemv2"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

seller_url = "http://www.gsshop.com/shop" + doc.find_class("product-brand-more-link")[0].get("href")
result["seller"] = doc.find_class("product-brand-more-link")[0].text_content() + "(" + seller_url + ")"
result["product_name"] = doc.find_class("option_tit")[0].find_class("tit")[0].text_content()
result["price"] = doc.find_class("price-definition-ins")[0].text_content().split("원")[0]
result["ship_fee"] = doc.find_class("option_tit")[0].find_class("delivery")[0].text_content()

try:
    option_p = re.compile("attrTypList\":\[([^\]]*)\]")
    result["option"] = "[" + option_p.search(html).group(1) + "]"
except:
    result["option"] = ""

print(result)
