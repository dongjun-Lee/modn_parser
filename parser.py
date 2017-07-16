from urllib import request
from urllib.request import Request, urlopen
import lxml.html as lh
import re
import json


def gmarket_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    for elem in doc.find_class("shopurl")[0].iter('strong'):
        result["seller"] = elem.text_content() + "(" + doc.find_class("shopurl")[0].get("href") + ")"

    result["product_name"] = doc.find_class("itemtit")[0].text_content()
    result["price"] = doc.find_class("price_real")[0].text_content()
    result["ship_fee"] = doc.find_class("txt_emp")[0].text_content()
    result["point"] = doc.find_class("cashback")[0].find_class("nav")[0].text_content().replace("열기", "").strip()

    try:
        option_p = re.compile("combOptionObj = {(.*)}")
        option_json = json.loads("{" + option_p.search(html).group(1) + "}")
        result["option"] = option_json
    except:
        result["option"] = ""

    try:
        discount_p = re.compile("OrderSet.Discount = {(.*)};")
        discount_json = json.loads("{" + discount_p.search(html).group(1) + "}")
        result["discount"] = discount_json
    except:
        result["option"] = ""

    return result


def auction_parse(url):
    html = request.urlopen(url).read().decode('euc-kr')
    doc = lh.document_fromstring(html)

    result = dict()

    result["seller"] = doc.find_class("shop-title")[0].text_content() + "(" + doc.find_class("btn_gostore")[0].get(
        "href") + ")"

    result["product_name"] = doc.find_class("itemtit")[0].text_content()
    result["price"] = doc.find_class("price_real")[0].text_content()
    result["ship_fee"] = doc.find_class("txt_emp")[0].text_content()
    result["point"] = doc.find_class("cashback_item")[0].find_class("nav")[0].text_content().replace("열기", "").strip()

    try:
        option_p = re.compile("ItemRequests=(.*);")
        option_json = json.loads(option_p.search(html).group(1))
        result["option"] = option_json
    except:
        result["option"] = ""

    result["discount"] = "http://itempage3.auction.co.kr/popup/CreditCardPromotion.html"

    return result


def elevenst_parse(url):
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
    try:
        option = dict()
        for li in doc.find_class("photo"):
            option_name = li.find_class("title")[0].text_content()
            option_price = li.find_class("prdc_price")[0].text_content()
            option[option_name] = option_price
        result["option"] = option
    except:
        result["option"] = ""

    result["discount"] = "http://www.11st.co.kr/browsing/CardBenefitPlace.tmall?method=getCardBenefit&addCtgrNo=952004"
    print(result)


def naver_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    seller_url_p = re.compile("(.*)/product")
    seller_url = seller_url_p.search(url).group(1)
    result["seller"] = doc.find_class("N=a:lid.home")[0].text_content() + "(" + seller_url + ")"
    result["product_name"] = doc.find_class("prd_name")[0].text_content()
    result["price"] = doc.find_class("fc_point sale")[0].find_class("thm")[0].text_content().strip()
    result["ship_fee"] = doc.find_class("_deliveryBaseFeeArea odd2")[0].find_class("_deliveryBaseFeeAreaValue ag")[
                             0].text_content() \
                         + " " + doc.find_class("_deliveryBaseFeeArea odd2")[0].find_class("bsk_txt _deliveryPolicy")[
                             0].text_content()

    try:
        option = dict()
        option_group_name_p = re.compile("aCombinationGroupName\" : \[([^\]]*)\]")
        option["option_group_name"] = "[" + option_group_name_p.search(html).group(1) + "]"
        options_p = re.compile("aCombinationOption\" : \[([^\]]*)\]")
        option["options"] = "[" + options_p.search(html).group(1) + "]"
        result["option"] = option
    except:
        result["option"] = ""

    return result


def ssg_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()
    try:
        seller_url = "http://emart.ssg.com" + doc.find_class("cdtl_ico_txt")[0].get("href")
        result["seller"] = doc.find_class("cdtl_ico_txt")[0].text_content() + "(" + seller_url + ")"
    except:
        seller_url = "이마트(http://emart.ssg.com)"

    result["product_name"] = doc.find_class("cdtl_info_tit")[0].text_content()
    result["price"] = doc.find_class("ssg_price")[0].text_content()
    try:
        result["ship_fee"] = doc.find_class("cdtl_txt_info")[0].text_content().strip()
    except:
        result["ship_fee"] = doc.find_class("cdtl_delivery_txt")[0].text_content().strip()

    try:
        option = dict()
        option_name_p = re.compile("uitemNm:\'([^']*)\'")
        option_names = option_name_p.findall(html)[1:]
        option_price_p = re.compile("bestAmt:\'([^']*)\'")
        option_prices = option_price_p.findall(html)[1:]
        option_qty_p = re.compile("usablInvQty:\'([^']*)\'")
        option_qtys = option_qty_p.findall(html)[1:]

        for i in range(len(option_names)):
            option[option_names[i]] = "{price : " + option_prices[i] + ", qty : " + option_qtys[i] + "}"
        result["option"] = option
    except:
        result["option"] = ""

    return result

def akmall_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    try:
        for tr in doc.find_class("tbl_type07")[0].iter("tr"):
            for th in tr.iter("th"):
                if th.text_content() == "A/S 책임자와 전화번호":
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
                    break
    except:
        result["seller"] = "ak몰(http://www.akmall.com)"

    result["price"] = doc.find_class("sale")[0].find_class("c_pink")[1].text_content().strip().split("\n")[0]

    for elem in doc.find_class("goods_img")[0].iter("h4"):
        result["product_name"] = elem.text_content().strip()
        break

    for elem in doc.find_class("deli")[0].iter("span"):
        result["ship_fee"] = elem.text_content().strip()

    try:
        result["point"] = "마일리지 " + doc.find_class("layertip")[0].text_content().strip().split("\n")[0] + "점"
    except:
        result["point"] = ""

    cnt = 0
    try:
        options = list()
        for elem in doc.find_class("group_4")[0].iter("option"):
            if cnt == 0:
                cnt += 1
            else:
                options.append(elem.text_content())
        result["option"] = options
    except:
        result["option"] = ""

    return result


def thehyundai_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    result["product_name"] = doc.find_class("prd-title")[0].text_content().strip().split("\r\n")[0]
    result["seller"] = doc.find_class("list-info")[0].text_content().strip()
    result["price"] = doc.find_class("dis-price")[0].text_content().strip().split("\r\n")[0]
    for td in doc.find_class("itemOptBasicInfo")[0].iter("td"):
        result["ship_fee"] = td.text_content().strip()
        break

    try:
        option = dict()
        for elem in doc.find_class("depth-opt-list")[0].iter("li"):
            option_name = elem.find_class("opt-name")[0].text_content().strip()
            option_price = elem.find_class("price")[0].text_content().strip()
            option[option_name] = option_price
        result["option"] = option
    except:
        result["option"] = ""

    return result


def galleria_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    product_name_p = re.compile("comp_item_name = \"([^\"]*)\"")
    product_name = product_name_p.search(html).group(1)
    result["product_name"] = product_name

    result["price"] = doc.find_class("t_price")[0].text_content()
    result["seller"] = doc.find_class("as_detailbox")[0].text_content().strip().split("\r\n")[0]
    result["ship_fee"] = doc.find_class("section")[1].text_content().strip()

    try:
        options = set()
        options_p = re.compile("attr_code_val = \"([^\"]*)\"")
        for option in options_p.findall(html):
            options.add(option)
        option = dict()
        for o in options:
            option[o] = result["price"]
        result["option"] = option
    except:
        result["option"] = ""

    return result


def ellotte_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    result["product_name"] = doc.find_class("group_tit")[0].text_content().strip()
    result["price"] = doc.find_class("after_price")[0].text_content().strip().split("~")[0] + "~"

    for td in doc.find_class("prd-point")[1].iter("td"):
        result["ship_fee"] = td.text_content().strip()
        break

    try:
        for tr in doc.find_class("prd-point")[0].iter("tr"):
            for th in tr.iter("th"):
                if th.text_content() == "A/S 책임자와 전화번호":
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
                    break
    except:
        result["seller"] = "el롯데(http://www.ellotte.com)"

    try:
        option = dict()
        cnt = 0
        for elem in doc.find_class("opt_area")[0].find_class("list thum_list")[0].iter("li"):
            option_name = elem.find_class("sec01")[0].text_content().strip()
            option_price = elem.find_class("sec02")[0].text_content().strip()
            option[option_name] = option_price
            result["option"] = option
    except:
        result["option"] = ""

    return result


def hmall_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    result["product_name"] = doc.find_class("tit")[0].text_content()
    result["price"] = doc.find_class("price")[0].find_class("digit")[0].text_content().strip().split("\r\n")[0]
    result["ship_fee"] = doc.find_class("productInfoDL mb15")[0].text_content().strip().split("\n")[-1].strip()

    for tr in doc.find_class("formTable mt10")[0].iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "배송비":
                for td in tr.iter("td"):
                    result["ship_fee"] = td.text_content().strip()
                    break
            if th.text_content() == "A/S책임자와 전화번호":
                for td in tr.iter("td"):
                    result["seller"] = td.text_content().strip()
                    break

    option = dict()
    try:
        for elem in doc.find_class("sstpl_selbox")[0].iter("li"):
            option_name = elem.find_class("info")[0].text_content()
            option_price = elem.find_class("price")[0].text_content()
            option[option_name] = option_price
    except:
        pass
    result["option"] = option

    return result


def kyobo_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    try:
        for tr in doc.find_class("tlb_type")[0].iter("tr"):
            for th in tr.iter("th"):
                if th.text_content() == "A/S":
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
    except:
        result["seller"] = "교보문고(http://www.kyobobook.co.kr)"

    result["product_name"] = doc.find_class("subject")[0].text_content().strip()
    result["price"] = doc.find_class("discount-price")[1].text_content().strip().split("\n")[0]
    result["ship_fee"] = doc.find_class("delivery-info")[1].text_content().strip().split("\n")[-1].strip()
    options = list()
    cnt = 0
    try:
        for elem in doc.find_class("options")[0].iter("option"):
            if cnt == 0:
                cnt += 1
            else:
                option_text = ""
                for text in elem.text_content().split("\n"):
                    option_text += text.strip()
                options.append(option_text)
        result["option"] = options
    except:
        result["option"] = ""

    return result


def bandi_parse(url):
    html = request.urlopen(url).read().decode('euc-kr')
    doc = lh.document_fromstring(html)

    result = dict()

    try:
        for tr in doc.find_class("boardInfo")[0].iter("tr"):
            for th in tr.iter("th"):
                if "A/S" in th.text_content():
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
    except:
        result["seller"] = "반디앤루니스(http://www.bandinlunis.com)"

    for elem in doc.find_class("pDetail")[0].iter("h4"):
        result["product_name"] = elem.text_content().strip()
        break
    result["price"] = doc.find_class("price")[0].text_content()

    for elem in doc.find_class("clfix pos_rel")[1].iter("strong"):
        result["point"] = elem.text_content()
        break

    for c in doc.find_class("gap"):
        try:
            if c.find_class("pdL")[0].text_content() == "배송비":
                for elem in c.find_class("pdR")[0].iter("strong"):
                    result["ship_fee"] = elem.text_content()
                    break
        except IndexError:
            pass

    cnt = 0
    options = list()
    for c in doc.find_class("gap"):
        try:
            if c.find_class("pdL")[0].text_content() == "옵션선택":
                for elem in c.find_class("pdR")[0].iter("option"):
                    if cnt == 0:
                        cnt += 1
                    else:
                        option_text = ""
                        for text in elem.text_content().split("\n"):
                            option_text += text.strip()
                        options.append(option_text)
                break
        except IndexError:
            pass

    result["option"] = options

    return result


def yes24_parse(url):
    html = request.urlopen(url).read().decode('euc-kr')
    doc = lh.document_fromstring(html)

    result = dict()

    try:
        for tr in doc.find_class("tb_detail01")[1].iter("tr"):
            for th in tr.iter("th"):
                if "A/S" in th.text_content():
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
    except:
        result["seller"] = "yes24(http://www.yes24.com)"
    result["product_name"] = doc.find_class("gd_name")[0].text_content()
    result["price"] = doc.find_class("yes_m")[1].text_content()
    result["ship_fee"] = doc.find_class("gd_deliCost")[0].find_class("txC_black")[0].text_content()

    sale_state = doc.find_class("gd_saleState")[0].text_content()
    if sale_state == "판매중":
        result["is_on_sale"] = True
    else:
        result["is_on_sale"] = False

    cnt = 0
    point_str = ""
    for elem in doc.find_class("gd_infoLi")[0].iter("li"):
        if cnt == 0:
            point_str += elem.text_content().strip()
            cnt += 1
        else:
            point_str += ", " + elem.text_content().strip().split("\n")[0].replace("\r", "")

    result["point"] = point_str

    for elem in doc.find_class("saleInfoTb")[0].iter("tbody"):
        result["discount"] = elem.text_content().strip().replace(")", ") / ")
        break

    try:
        option_p = re.compile("\'#options\'\),{(.*)}\);")
        option_json = json.loads("{" + option_p.search(html).group(1) + "}")
        output_option_dict = dict()

        for key, value in option_json.items():
            option_name = key
            option_price = json.loads(value)['opt_salepr']
            output_option_dict[option_name] = option_price

        result["option"] = output_option_dict
    except:
        result["option"] = ""

    return result


def sixsix_parse(url):
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

    return result


def lottemart_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    result["product_name"] = doc.find_class("detail-type")[0].text_content()

    price_p = re.compile("price\':\'([^']*)\'")
    price = price_p.search(html).group(1)
    result["price"] = price

    seller = ""
    for tr in doc.get_element_by_id("tab01").iter("tr"):
        for th in tr.iter("th"):
            if th.text_content() == "A/S책임자 연락처":
                for td in tr.iter("td"):
                    seller = td.text_content().strip()
                    break
    if seller == "":
        result["seller"] = "롯데마트(02-2145-8000)"
    else:
        result["seller"] = seller

    result["ship_fee"] = "3만원미만:2500원, 3만원이상:무료"

    try:
        option = dict()
        for elem in doc.find_class("bundle-list")[0].iter("article"):
            option_name = elem.find_class("prod-name")[0].text_content().strip()
            option_price = elem.find_class("price-strike-type1")[0].text_content().strip()
            option[option_name] = option_price
        result["option"] = option
    except:
        result["option"] = ""

    return result


def homeplus_parse(url):
    html = request.urlopen(url).read().decode('euc-kr')
    doc = lh.document_fromstring(html)

    result = dict()

    result["seller"] = "홈플러스(http://www.homeplus.co.kr)"

    result["product_name"] = doc.find_class("pro-tit")[0].text_content()
    result["price"] = doc.find_class("price")[0].text_content().strip().split("\r\n")[0]
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

    return result


def gsshop_parse(url):
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

    return result


def lottecom_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    try:
        for tr in doc.find_class("prd-point")[0].iter("tr"):
            for th in tr.iter("th"):
                if th.text_content() == "A/S 책임자와 전화번호":
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
                    break
    except:
        result["seller"] = "롯데닷컴(http://www.lotte.com)"

    result["product_name"] = doc.find_class("group_tit")[0].text_content()
    result["price"] = doc.find_class("after_price")[0].find_class("final")[0].text_content()

    cnt = 0
    ship_fee = ""
    for tr in doc.find_class("prd-point")[1].iter("tr"):
        if cnt == 0:
            cnt += 1
        else:
            for td in tr.iter("td"):
                ship_fee += td.text_content().strip()
                ship_fee += ", "
            break
    result["ship_fee"] = ship_fee

    try:
        option = dict()
        for elem in doc.find_class("opt_area")[0].iter("li"):
            option_name = elem.find_class("sec01")[0].text_content()
            option_price = elem.find_class("sec02")[0].text_content()
            option_on_sale = elem.find_class("opt_thum")[0].text_content().strip()
            on_sale = True
            if option_on_sale == "품절":
                on_sale = False

            option[option_name] = "{price : " + option_price + ", on_sale : " + str(on_sale) + "}"
        result["option"] = option
    except:
        result["option"] = ""

    return result


def lottei_parse(url):
    html = request.urlopen(url).read().decode('utf-8')
    doc = lh.document_fromstring(html)

    result = dict()

    result["product_name"] = doc.find_class("dg_tit")[0].text_content().strip()
    result["price"] = doc.find_class("price2")[0].text_content().strip().split("~")[0] + "~"

    for td in doc.find_class("ntable_02")[0].iter("td"):
        result["ship_fee"] = td.text_content().strip()
        break

    try:
        for tr in doc.find_class("ntable_01")[0].iter("tr"):
            for th in tr.iter("th"):
                if th.text_content() == "A/S 책임자/전화번호":
                    for td in tr.iter("td"):
                        result["seller"] = td.text_content().strip()
                        break
                    break
    except:
        result["seller"] = "롯데i몰(http://www.lotteimall.com)"

    try:
        option = dict()
        cnt = 0
        for elem in doc.find_class("addClassOnClick2")[0].iter("li"):
            if cnt == 0:
                cnt += 1
            else:
                option_name = elem.find_class("info")[0].text_content().strip()
                option_price = elem.find_class("price")[0].text_content().strip()
                option[option_name] = option_price
                result["option"] = option
    except:
        result["option"] = ""

    return result


def timon_parse(url):
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
        result["option"] = options
    except:
        result["option"] = ""

    return result


def parse(url):
    if "gmarket" in url:
        return gmarket_parse(url)
    elif "auction" in url:
        return auction_parse(url)
    elif "11st" in url:
        return elevenst_parse(url)
    elif "naver" in url:
        return naver_parse(url)
    elif "ssg" in url:
        return ssg_parse(url)
    elif "akmall" in url:
        return akmall_parse(url)
    elif "thehyundai" in url:
        return thehyundai_parse(url)
    elif "galleria" in url:
        return galleria_parse(url)
    elif "ellotte" in url:
        return ellotte_parse(url)
    elif "hyundaihmall" in url:
        return hmall_parse(url)
    elif "kyobo" in url:
        return kyobo_parse(url)
    elif "bandinlunis" in url:
        return bandi_parse(url)
    elif "yes24" in url:
        return yes24_parse(url)
    elif "66girls" in url:
        return sixsix_parse(url)
    elif "lottemart" in url:
        return lottemart_parse(url)
    elif "homeplus" in url:
        return homeplus_parse(url)
    elif "gsshop" in url:
        return gsshop_parse(url)
    elif "lotte.com" in url:
        return lottecom_parse(url)
    elif "lotteimall" in url:
        return lottei_parse(url)
    elif "ticketmonster" in url:
        return timon_parse(url)
