from urllib import request
import lxml.html as lh
import re
import json

url = "http://storefarm.naver.com/mixmatch7/products/716892897?NaPm=ct%3Dj4xy2iib%7Cci%3Dcheckout%7Ctr%3Dhdlt%7Ctrx%3D881454%7Chk%3D5f7512154fb97d83a5be9a5e2c5a8f50b15add6c"
html = request.urlopen(url).read().decode('utf-8')
doc = lh.document_fromstring(html)

result = dict()

seller_url_p = re.compile("(.*)/product")
seller_url = seller_url_p.search(url).group(1)
result["seller"] = doc.find_class("N=a:lid.home")[0].text_content() + "(" + seller_url + ")"
result["product_name"] = doc.find_class("prd_name")[0].text_content()
result["price"] = doc.find_class("fc_point sale")[0].find_class("thm")[0].text_content().strip()
result["ship_fee"] = doc.find_class("_deliveryBaseFeeArea odd2")[0].find_class("_deliveryBaseFeeAreaValue ag")[0].text_content() \
                     + " " + doc.find_class("_deliveryBaseFeeArea odd2")[0].find_class("bsk_txt _deliveryPolicy")[0].text_content()

try:
    option = dict()
    option_group_name_p = re.compile("aCombinationGroupName\" : \[([^\]]*)\]")
    option["option_group_name"] = "[" + option_group_name_p.search(html).group(1) + "]"
    options_p = re.compile("aCombinationOption\" : \[([^\]]*)\]")
    option["options"] = "[" + options_p.search(html).group(1) + "]"
    result["option"] = option
except:
    result["option"] = ""

print(result)
