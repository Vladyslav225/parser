import bs4
import requests
from urllib.request import urlopen
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
    
    link = links_for_parser[2]

    response_link_review = urlopen(link)

    data_json = json.loads(response_link_review.read())
    print(data_json)

    # response_link_review = requests.get('https://api.ctrs.com.ua/products/685028/reviews?page=1&productId=685028')
    # convert_to_json = response_link_review.json()

    # json_review = convert_to_json['data']['reviews']

    # for review in json_review:

    
    

# def data_tv_photo_video(link):
#     pass


# def data_audio(link):
#     pass