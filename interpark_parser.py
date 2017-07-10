from urllib import request
import lxml.html as lh
import re
import json

url = "http://shopping.interpark.com/product/productInfo.do?prdNo=4979030863&dispNo=001241"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

result["price"] = doc.find_class("salePrice")[0].text_content()

print(result)



