from urllib.request import Request, urlopen
import lxml.html as lh

url = "http://deal.11st.co.kr/product/SellerProductDetail.tmall?method=getSellerProductDetail&prdNo=1013670781&trTypeCd=22&trCtgrNo=895019"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read().decode('euc-kr')
doc = lh.document_fromstring(html)

result = dict()

result["seller"] = doc.find_class("seller_nickname")[0].text_content()

for elem in doc.find_class("heading")[0].iter("h2"):
    result["product_name"] = elem.text_content()
    break

result["sale_price"] = doc.find_class("sale_price")[0].text_content()
result["ship_fee"] = doc.find_class("det_info")[1].find_class("col first")[0].text_content()

result["discount"] = "http://www.11st.co.kr/browsing/CardBenefitPlace.tmall?method=getCardBenefit&addCtgrNo=952004"

print(result)


