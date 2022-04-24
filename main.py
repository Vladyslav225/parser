import bs4
import requests
import json

import config


links_type_products = []
links_subtype_products = []
product_links_for_get_reviews = []

link_type_otzyvy = {}
links_type_anchor = {}


def index_page():
    try:
        response = requests.get(url=config.ONLINE_STORE, headers=config.HEADERS).text

    except Exception as ex:
        print(ex)

    with open(config.INDEX_PAGE_HTML, 'w', encoding='utf-8') as file:
        file.write(str(response))
        file.close()


def catalog_with_product(file):
    all_links_type_products = {}

    try:
        soup = bs4.BeautifulSoup(file, 'html.parser')

    except Exception as ex:
        print(ex)

    catalog = soup.find('div', {'class':'catalog__wrap'}).find('ul').find_all('li')

    for type_product in catalog[1:]:
        try:
            text_type_products = type_product.find('div').find('a').find('p').text

            url_type_products = type_product.find('div').find('a').get('href')

        except Exception as ex:
            print(ex)

        if 'https://www.foxtrot.com.ua' not in url_type_products:
            _create_full_link = 'https://www.foxtrot.com.ua' + url_type_products

        all_links_type_products[text_type_products] = _create_full_link

    for title, link in all_links_type_products.items():
        if 'Cмартфоны' in title:
            links_type_products.append(link)

        if 'Телевизоры, аудиотехника' in title:
            links_type_products.append(link)


        if 'Для геймеров' in title:
            links_type_products.append(link)



def open_links_type_products():
    for data in links_type_products:
        try:
            response = requests.get(url=data, headers=config.HEADERS)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)

        block_container = soup.find_all('div', {'class':'container'})

        for open_block in block_container:
            block_catalog = open_block.find('div', {'class':'wrapper'}).find('div', {'class':'category'})

            if block_catalog == None:
                continue

            open_block_catalog = block_catalog.find('div', {'class':'category__item'}).find('a').get('href')

            if 'https://www.foxtrot.com.ua' not in open_block_catalog:
                _create_full_link = 'https://www.foxtrot.com.ua' + open_block_catalog
                links_subtype_products.append(_create_full_link)


def blocks_with_products():
    links_phone = []
    links_tv = []
    links_noutbuki = []

    for links in links_subtype_products:
        try:
            response = requests.get(url=links, headers=config.HEADERS)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)

        product_blocks = soup.find('div', {'class':'listing__body-wrap image-switch'}).find('section').find_all('article')
        
        for product_links in product_blocks:
            url_products = product_links.find('div', {'class': 'card js-card sc-product'}).find('div', {'class':'card__body'}).find('a', {'class':'card__title'}).get('href')

            if 'mobilnye_telefony' in url_products and len(links_phone) != 3:
                links_phone.append('https://www.foxtrot.com.ua' + url_products)

            if 'led_televizory' in url_products and len(links_tv) != 3:
                links_tv.append('https://www.foxtrot.com.ua' + url_products)

            if 'noutbuki' in url_products and len(links_noutbuki) != 3:
                links_noutbuki.append('https://www.foxtrot.com.ua' + url_products)

    links_for_parsing  = [*links_phone, *links_tv, *links_noutbuki]

    return links_for_parsing


def get_links_reviews(links):
    for links_for_scraping in links:

        try:
            response = requests.get(url=links_for_scraping, headers=config.HEADERS)
            
            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)

        title_product = soup.find('h1', {'class':'page__title overflow'}).text.strip()

        find_element_coment = soup.find('div', {'class':'product-menu__card-review product-menu__card-review_static'}).find('a', {'class':'product-menu__card-comments'}).get('href')

        if 'otzyvy.html' in find_element_coment:
            links_otzyvy = 'https://www.foxtrot.com.ua' + find_element_coment
            link_type_otzyvy[title_product] = links_otzyvy
            
        elif '#anchor-3' in find_element_coment:
            links_anchor = links_for_scraping + find_element_coment
            links_type_anchor[title_product] = links_anchor


# def open_links_type_otzyvy():
#     for title, link in link_type_otzyvy.items():
#         try:
#             response = requests.get(url=link, headers=config.HEADERS)

#             soup = bs4.BeautifulSoup(response.text, 'html.parser')

#         except Exception as ex:
#             print(ex)


def open_links_type_anchor():
    for title, link in links_type_anchor.items():
        try:
            response = requests.get(url=link, headers=config.HEADERS)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)


        find_block_reviews = soup.find('section', {'class':'main-reviews container'})#.find('div', {'class':'main-reviews__body js-toggle-body'})
        # print(find_block_reviews)

        element_all_reviews = find_block_reviews.find('div', {'class':'main-reviews__item'}).find('div').find('a').get('href')
        
        # res = requests.get(url=element_all_reviews, headers=config.HEADERS)
        
        # jsonn = res.json()
        # print(jsonn)



        

def main():
    index_page()

    with open(config.INDEX_PAGE_HTML, 'r') as file:
        file = file.read()
        
    catalog_with_product(file)

    open_links_type_products()

    get_links_products =  blocks_with_products()

    get_links_reviews(links=get_links_products)

    # open_links_type_otzyvy()

    open_links_type_anchor()


if __name__ == '__main__':
    main()
