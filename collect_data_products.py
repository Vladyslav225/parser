import bs4
import requests
import json

import config


def page_smartfony(title, url):
    links_with_reviewes = []
    links_for_parser = []

    try:
        response = requests.get(url, headers=config.HEADERS)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

    except Exception as ex:
        print(ex)

    try:
        _catalog = soup.find('div', {'class':'catalog-facet'}).find_all('div')

    except Exception as ex:
        print(ex)

    for _product in _catalog:
        block_product = _product.find('div', {'class':'br10 p8 border-box pr productCardCategory-0-2-274'})

        if block_product == None:
            continue

        element_review_link = block_product.find('div', {'class':''}).find('div', {'class':'pt8 pb8 df aic border-box container-0-2-294'}).find('a', {'class':'link link-0-2-296 ml8'})

        if element_review_link == None:
            continue

        review_link = element_review_link.get('href')
        
        if 'https://www.ctrs.com.ua' not in review_link:
            full_reviuw_link = 'https://www.ctrs.com.ua' + review_link

            links_with_reviewes.append(full_reviuw_link)

    for new_list in links_with_reviewes[:3]:
        links_for_parser.append(new_list)
    # print(links_for_parser)

    # product_1 = links_for_parser[0]
    product_1 = 'https://www.ctrs.com.ua/smartfony/g990b-zwd-white-samsung-s21fe-6128-gb-702243.html'

    response_link_review = requests.get(product_1)

    with open('product_one.json', 'w') as json_file:
        json.dump(response_link_review.json(), json_file, indent=4, ensure_ascii=False)
 
    # response_link_review = requests.get('https://api.ctrs.com.ua/products/685028/reviews?page=1&productId=685028')
    # convert_to_json = response_link_review.json()

    # for review in convert_to_json['data']:
    #     print(review)
    


# dict_ = { 
# 'data': {
#     'reviews': [{
#         'counters': {
#             'answers': 1, 
#             'complains': 0, 
#             'dislikes': 0, 
#             'likes': 0
#             }, 
#             'created_at': 1644486741, 
#             'evaluations': [], 
#             'id': 158421, 
#             'is_complained': False, 
#             'is_disliked': False, 
#             'is_liked': False, 
#             'params': {
#                 'mark': 5, 
#                 'content': 
#                 'З 10.05.2021 користуюся цим телефоном. Дуже хороший телефон. ', 
#                 'subscribe': False, 
#                 'bad_things': 'Поки не знайшов. ', 
#                 'good_things': 'Хороший телефон. ', 
#                 'user_experience': 5
#                 }, 
#                 'status': 2,
#                 'text': 'З 10.05.2021 користуюся цим телефоном. Дуже хороший телефон. ', 
#                 'top_answer': {
#                     'counters': {
#                         'answers': 0, 
#                         'complains': 0, 
#                         'dislikes': 0, 
#                         'likes': 0
#                         }, 
#                         'created_at': 1644490078, 
#                         'id': 158428, 
#                         'is_complained': False, 
#                         'is_disliked': False, 
#                         'is_liked': False, 
#                         'status': 2, 
#                         'text': 'Дякуємо за відгук!', 
#                         'user_data': {
#                             'avatar': 'https://i.citrus.world/uploads/avatar/b19434f94001c3e88d3331b4ec752ba3.jpg', 
#                             'name': 'Представник компанії «Цитрус»'
#                             }
#                         }, 
#                         'user_data': {
#                             'avatar': 'https://i.citrus.world/uploads/avatar/1ceb1faaf5512567cfba90ff4b8d33cb.jpg', 
#                             'name': 'Левицький Михайло Іванович'
#                             }
#                         }, 
#                         {
#                             'counters': {
#                                 'answers': 1, 
#                                 'complains': 0, 
#                                 'dislikes': 0, 
#                                 'likes': 0}, 
#                                 'created_at': 1638037209, 
#                                 'evaluations': [], 
#                                 'id': 149810, 
#                                 'is_complained': False, 
#                                 'is_disliked': False, 
#                                 'is_liked': False, 
#                                 'params': {
#                                     'mark': 5, 
#                                     'content': 'Очень стильный , удобный  , функциональный телефон. Прекрасное качество фото. Недостатков не заметила. Ребята в магазине качественно проконсультировали.', 
#                                     'subscribe': True, 
#                                     'bad_things': 'Не замечено', 
#                                     'good_things': 'Все качественно сделано', 
#                                     'user_experience': 1
#                                     }, 
#                                     'status': 2, 
#                                     'text': 'Очень стильный , удобный  , функциональный телефон. Прекрасное качество фото. Недостатков не заметила. Ребята в магазине качественно проконсультировали.', 
#                                             'top_answer': {
#                                                 'counters': {
#                                                     'answers': 0, 
#                                                     'complains': 0, 
#                                                     'dislikes': 0, 
#                                                     'likes': 0
#                                                     }, 
#                                                     'created_at': 1638172400, 
#                                                     'id': 149975, 
#                                                     'is_complained': False, 
#                                                     'is_disliked': False, 
#                                                     'is_liked': False, 
#                                                     'status': 2, 
#                                                     'text': 'Дякуємо за відгук! Самі б користувались цим товаром із задоволенням :)', 
#                                                     'user_data': {
#                                                         'avatar': 'https://i.citrus.world/uploads/avatar/dd9d8f7940873d10e61f61bd6e481155.jpg', 
#                                                         'name': 'Щукина Ника'
#                                                         }
#                                                     }, 
#                                                     'user_data': {
#                                                         'avatar': 'https://i.citrus.world/img/bg/avatar-none.png', 
#                                                         'name': 'Табунчик Оксана Дмитриевна'
#                                                         }
#                                                     }, 
#                                                     {
#                                                         'counters': {
#                                                             'answers': 1, 
#                                                             'complains': 0, 
#                                                             'dislikes': 0, 
#                                                             'likes': 1}, 
#                                                             'created_at': 1636893143, 
#                                                             'evaluations': [], 
#                                                             'id': 147108, 
#                                                             'is_complained': False, 
#                                                             'is_disliked': False, 
#                                                             'is_liked': False, 
#                                                             'params': {
#                                                                 'mark': 5, 
#                                                                 'content': 'Дуже хороший телефон.', 
#                                                                 'subscribe': False, 
#                                                                 'bad_things': 'Не знайшов.', 
#                                                                 'good_things': 'Комфортний у використанні.', 
#                                                                 'user_experience': 5
#                                                                 }, 'status': 2, 
#                                                                 'text': 'Дуже хороший телефон.', 
#                                                                 'top_answer': {
#                                                                     'counters': {
#                                                                         'answers': 0, 
#                                                                         'complains': 0, 
#                                                                         'dislikes': 0, 
#                                                                         'likes': 0
#                                                                         }, 
#                                                                         'created_at': 1636983914, 
#                                                                         'id': 147358, 
#                                                                         'is_complained': False, 
#                                                                         'is_disliked': False, 
#                                                                         'is_liked': False, 
#                                                                         'status': 2, 
#                                                                         'text': 'Дякуємо за відгук! Приємного користування :)', 
#                                                                         'user_data': {
#                                                                             'avatar': 'https://i.citrus.world/uploads/avatar/dd9d8f7940873d10e61f61bd6e481155.jpg', 
#                                                                             'name': 'Щукина Ника'
#                                                                             }
#                                                                         }, 
#                                                                         'user_data': {
#                                                                             'avatar': 'https://i.citrus.world/uploads/avatar/1ceb1faaf5512567cfba90ff4b8d33cb.jpg', 
#                                                                             'name': 'Левицький Михайло Іванович'
#                                                                             }
#                                                                         }
#     ], 
# 'meta': {
#     'pagination': {
#         'per_page': 3, 
#         'from': 1, 
#         'to': 3, 
#         'current_page': 1, 
#         'last_page': 5, 
#         'total': 15}
#     }
# }, 
# 'meta': []}



# def data_tv_photo_video(link):
#     pass


# def data_audio(link):
#     pass