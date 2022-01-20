from requests import Session
from pprint import pprint

class Mvideo():
    """docstring for Mvideo"""
    def __init__(self):
        self.s = Session()
        self.get_token()

    def get_token(self):

        self.s.headers = {
            'Host': 'www.mvideo.ru',
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9',
        }
        r = self.s.get('https://www.mvideo.ru/').cookies
        self.s.cookies = r

        self.MVID_CITY_ID = r.get('MVID_CITY_ID')
        self.JSESSIONID = r.get('JSESSIONID')
        self.MVID_REGION_ID = r.get('MVID_REGION_ID')
        self.MVID_TIMEZONE_OFFSET = r.get('MVID_TIMEZONE_OFFSET')
        self.MVID_REGION_SHOP = r.get('MVID_REGION_SHOP')
        self.bIPs = r.get('bIPs')

        print( self.MVID_CITY_ID, self.JSESSIONID, self.MVID_REGION_ID, self.MVID_TIMEZONE_OFFSET, self.MVID_REGION_SHOP, self.bIPs)

    def parse_by_keyword(self,keyword):

        params = (
            ('query', f'{keyword}'),
            ('offset', '0'),
            ('limit', '24'),
            ('doTranslit', 'true'),
            ('context', ''),
        )
        r = self.s.get('https://www.mvideo.ru/bff/products/search', params=params).json()
        try:
            item_id = r['body']['url'].split('-')[-1]
            items = self.get_listing(item_id)
            details = self.get_products_details(items)

        except Exception as e:
            item_id = r['body']['products']
            details = self.get_products_details(item_id)

        return details


    def get_products_details(self, ids):

        self.ids = ids

        self.s.headers = {}
        self.s.headers["authority"] = "www.mvideo.ru"
        self.s.headers["sec-ch-ua"] = "Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"
        self.s.headers["x-set-application-id"] = "2b0556f0-1c9d-4b53-b2e3-ab0c10971ff3"
        self.s.headers["dnt"] = "1"
        self.s.headers["sec-ch-ua-mobile"] = "?0"
        self.s.headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        self.s.headers["content-type"] = "application/json"
        self.s.headers["accept"] = "application/json"
        self.s.headers["adrum"] = "isAjax:true"
        self.s.headers["sec-ch-ua-platform"] = "Windows"
        self.s.headers["origin"] = "https://www.mvideo.ru"
        self.s.headers["sec-fetch-site"] = "same-origin"
        self.s.headers["sec-fetch-mode"] = "cors"
        self.s.headers["sec-fetch-dest"] = "empty"
        self.s.headers["referer"] = "https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205/f/category=iphone-914"
        self.s.headers["accept-language"] = "ru-RU,ru;q=0.9"
        self.s.headers["cookie"] = f"MVID_CITY_ID={self.MVID_CITY_ID}; MVID_GUEST_ID=19399354721; MVID_REGION_ID={self.MVID_REGION_ID}; searchType2=3; COMPARISON_INDICATOR=false; CACHE_INDICATOR=false; flacktory=no; MVID_TIMEZONE_OFFSET={self.MVID_TIMEZONE_OFFSET}; MVID_KLADR_ID=6100000100000; MVID_REGION_SHOP={self.MVID_REGION_SHOP}; MVID_GEOLOCATION_NEEDED=true; MVID_IS_NEW_BR_WIDGET=false; MVID_NEW_MBONUS_BLOCK=false; MVID_CATALOG_STATE=1; MVID_AB_PROMO_DAILY=1; MVID_FILTER_TOOLTIP=2; MVID_ONLY_IN_STOCK=true; MVID_PRM20_ON=true; MVID_PRM20_CMS=true; MVID_ABC_TEST_WIDGET=0; MVID_PRODUCT_DETAILS=true; MVID_LAYOUT_TYPE=1; MVID_PRICE_FIRST=2; MVID_BLACK_FRIDAY_ENABLED=true; MVID_AB_TEST_COMPARE_ONBOARDING=true; MVID_EMPH_PERS_PRICE=1; MVID_PROMO_CATALOG_ON=true; BIGipServeratg-ps-prod_tcp80=1090837514.20480.0000; bIPs={self.bIPs}; SMSError=; authError=; _gid=GA1.2.1400290529.1641702658; tmr_lvid=76ea9fec7e22022b203dd4525409c7ed; tmr_lvidTS=1641702658286; st_uid=6483e18d239db44f6c7105a9b1a28de7; advcake_track_id=611bb217-56dc-edb4-d5e4-ae13119f6f3e; advcake_session_id=f3ba2d9e-bbca-0dd4-b6f3-7dbc1373b375; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=72cc518a-2142-454d-9e74-c6c76a9b2d37; afUserId=72ce0b03-eecc-4540-9c95-0e82c9859ff0-p; AF_SYNC=1641702662221; flocktory-uuid=59923592-0641-43a8-ba4f-9514e620362d-7; _fbp=fb.1.1641702665208.508220352; BIGipServeratg-ps-prod_tcp80_clone=1090837514.20480.0000; _gcl_au=1.1.1494911013.1641702670; _ym_uid=1641702671194360998; _ym_d=1641702671; uxs_uid=f89cb470-7104-11ec-9e79-bda194aa9b9e; _ym_isad=2; adrdel=1; adrcid=AgKrbpKA_8HuwKDrrTFfUTQ; MVID_ENVCLOUD=ycprod; MVID_CALC_BONUS_RUBLES_PROFIT=true; MVID_CART_MULTI_DELETE=true; PRESELECT_COURIER_DELIVERY_FOR_KBT=false; _ga=GA1.2.1408486885.1641702658; cto_bundle=3_f1aV9qN1BGQXgyRjlwcHVnQ2xyYlhTWWNsayUyRkRXQll6dlpENVpZZ3Vyd01lTjc4SnZhTyUyRjU3UFpkZ2c4T3N3dUJ4M296MnZOaVZzdHB2VDNzZnNKSzhqRnAlMkZwRmglMkJpMHNpajY1b1Q0OGJPNyUyQjAlMkZWcGY0ZTRaSiUyRm5MUU1BJTJCbEFIaVI; tmr_detect=0%7C1641704789615; tmr_reqNum=51; ADRUM=s=1641705191992&r=https%3A%2F%2Fwww.mvideo.ru%2Fsmartfony-i-svyaz-10%2Fsmartfony-205%2Ff%2Fcategory%3Diphone-914%3F0; JSESSIONID={self.JSESSIONID}; _ga_CFMZTSS5FM=GS1.1.1641702656.1.1.1641705192.0; _ga_BNX5WPP3YK=GS1.1.1641702656.1.1.1641705192.60; mindboxDeviceUUID=d432c493-628b-4937-95d0-56576d4a7afa; directCrm-session=%7B%22deviceGuid%22%3A%22d432c493-628b-4937-95d0-56576d4a7afa%22%7D"

        data = '{"productIds":' + str(ids).replace("'",'"') + ',"mediaTypes":["images"],"category":true,"status":true,"brand":true,"propertyTypes":["KEY"],"propertiesConfig":{"propertiesPortionSize":5},"multioffer":false}'
        r = self.s.post("https://www.mvideo.ru/bff/product-details/list", data=data).json()
        return r 

    def get_listing(self,item_id):

        params = (
            ('categoryId', str(item_id)),
            ('offset', 0),
            ('limit', 24),
            ('doTranslit', 'true'),
        )
        r = self.s.get('https://www.mvideo.ru/bff/products/listing', params=params).json()
        items = r['body']['products']
        return items

    def get_statuses(self):  

        ids_str = ''
        for x in self.ids:
            ids_str = ids_str + str(x) + ','
        ids_str = ids_str[:-1]

        params = (
            ('productIds', ids_str),
        )

        r = self.s.get('https://www.mvideo.ru/bff/products/statuses', params=params).json()

        self.statuses = {}
        for each in r['body']['statuses']:
            self.statuses[each['productId']] = each['productStatus']

        return self.statuses

    def get_prices(self):  

        ids_str = ''
        for x in self.ids:
            ids_str = ids_str + str(x) + ','
        ids_str = ids_str[:-1]

        params = (
            ('productIds', ids_str),
            ('addBonusRubles', 'true'),
            ('isPromoApplied', 'true'),
        )

        r = self.s.get('https://www.mvideo.ru/bff/products/prices', params=params).json()

        self.prices = {}
        for each in r['body']['materialPrices']:
            self.prices[each['price']['productId']] = {'basePrice':each['price']['basePrice'],'salePrice':each['price']['salePrice']}

        return self.prices

# m = Mvideo()
# details = m.parse_by_keyword("playstation 5")
# details = m.parse_by_keyword("xbox series x / s - консоли")

# pprint(details)
# statuses = m.get_statuses()
# # prices = m.get_prices()
# pprint(details['body']['products'][0])

# for each_prod in details['body']['products']:
#     product = {}
#     product['name'] = each_prod['name']
#     product['modelName'] = each_prod['modelName']
#     product['brandName'] = each_prod['brandName']
#     product['image'] = each_prod['image']
#     product['productId'] = each_prod['productId']
#     product['status'] = each_prod['status']
#     product['status'] = each_prod['status']

#     pprint( each_prod )
#     print( '\n' )

#     exit()


"""  

{'brandName': 'Acer',
 'image': 'Pdb/small_pic/480/30057652b.jpg',
 'modelName': 'Aspire 7 A715-75G-57GR NH.Q99ER.00K',
 'name': 'Ноутбук игровой Acer Aspire 7 A715-75G-57GR NH.Q99ER.00K',
 'productId': '30057652',
 'status': {'availableOnlyInRetailStore': False,
            'isCannotBeExchanged': False,
            'showCase': False,
            'soldOut': False}}

"""