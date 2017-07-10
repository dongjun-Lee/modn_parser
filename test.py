from urllib import request
import json
import re

url = "http://66girls.co.kr/product/detail.html?product_no=57109&cate_no=71&display_group=2"
html = request.urlopen(url).read().decode("unicode_escape")
option_p = re.compile("option_stock_data = \'{([^']*)}\';")

option_json = json.loads("{" + option_p.search(html).group(1) + "}")
print(option_json)