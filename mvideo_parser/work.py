# - *- coding: utf- 8 - *-
from threading import Thread
from time import sleep

from pprint import pprint

from mvideo_parser.mvideo import Mvideo
from utils.decorators import catcherError
from discord.discord_bot import Discord
from database import db
from utils.base_functions import log_action
from utils.base_functions import log

dis_delay = 1
loop_delay = 5

@catcherError
def send_dis(item_id, item_name, item_link, img_links, basePrice, salePrice):

    d = Discord()

    item_link = f"https://www.mvideo.ru/products/{item_link}-{item_id}"
    img_links = f"http://static.mvideo.ru/{img_links}"
    
    if basePrice != salePrice:
        item_price = f"**{ str(salePrice) } ₽**  ~~{ str(basePrice) } ₽~~"
    else:
        item_price = f"**{str(basePrice)} ₽**"

    d.send_message(item_name,item_link, img_links, item_price)

@catcherError
def start(key_words, black_list):

    m = Mvideo()
    i = 0
    while 1:
        try:

            for word in key_words:
                details = m.parse_by_keyword(word)
                # details = m.get_products_details(item_list)
                statuses = m.get_statuses()
                prices = m.get_prices()

                inBlack = False
                for each_prod in details['body']['products']:
                    product = {}
                    product['name'] = each_prod['name']
                    product['modelName'] = each_prod['modelName']
                    product['brandName'] = each_prod['brandName']
                    product['image'] = each_prod['image']
                    product['productId'] = each_prod['productId']
                    product['status'] = each_prod['status']
                    product['status'] = each_prod['status']
                    product['nameTranslit'] = each_prod['nameTranslit']

                    item_id = str(product['productId'])
                    status = statuses[item_id]

                    basePrice = str(prices[item_id]['basePrice'])
                    salePrice = str(prices[item_id]['salePrice'])

                    # блек фильтр #
                    for each_data in black_list:
                        if each_data in product['name']:
                            inBlack = True
                            # log_action({'action':'Пропуск','info':'Товар в блоке','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                            break
                        if each_data in f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}":
                            # log_action({'action':'Пропуск','info':'Товар в блоке','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                            inBlack = True
                            break

                    if inBlack:
                        continue
                    ################

                    result = db.select_by_item_id(item_id)
                    if result == None:
                        db.add_new_item(item_id,status,basePrice+'|'+salePrice)  
                        if status != 'Available':
                            log_action({'action':'❗️Только сохранение в бд','info':'Товара нет в наличии','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                            continue

                        log_action({'action':'✅Вывод в дис','info':'Новый товар','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                        send_dis(item_id, product['name'], product['nameTranslit'], product['image'], basePrice, salePrice)
                        sleep(dis_delay)




                    else:
                        old_status = result['status']
                        old_price = result['price']
                        old_basePrice = result['price'].split('|')[0]
                        old_salePrice = result['price'].split('|')[1]

                        if status != 'Available':
                            log_action({'action':'❗️Пропуск','info':'Товара еще нет в наличии','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                            continue

                        if status == old_status:
                            if int(old_salePrice) > int(salePrice):
                                db.update_watcher(item_id,'price',basePrice+'|'+salePrice)

                                log_action({'action':'✅Вывод в дис','info':'Изменение цены','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                                send_dis(item_id, product['name'], product['nameTranslit'], product['image'], basePrice, salePrice)
                                sleep(dis_delay)

                            else:
                                log_action({'action':'❗️Пропуск','info':'Уже выводили. Цена не изменилась','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                                continue


                        else:
                            db.update_watcher(item_id,'status',status)

                            log_action({'action':'✅Вывод в дис','info':'Товар снова в наличии','Name':product['name'],'ProductID':product['productId'],'avalible': status,'basePrice':basePrice,'salePrice':salePrice, 'link':f"https://www.mvideo.ru/products/{product['nameTranslit']}-{item_id}"})
                            send_dis(item_id, product['name'], product['nameTranslit'], product['image'], basePrice, salePrice)
                            sleep(dis_delay)
                            

            i = i+1
            print('i=' + str(i))

        except Exception as e:
            log(e)

        finally:
            sleep(loop_delay)