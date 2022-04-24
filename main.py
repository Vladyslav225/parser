import bs4
import requests

import config


links_type_products = []
links_subtype_products = []
product_links_for_get_reviews = []


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
    all_product_links = []

    for links in links_subtype_products:
        try:
            response = requests.get(url=links, headers=config.HEADERS)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)

        product_blocks = soup.find('div', {'class':'listing__body-wrap image-switch'}).find('section').find_all('article')
        
        for product_links in product_blocks:
            url_products = product_links.find('div', {'class': 'card js-card sc-product'}).find('div', {'class':'card__body'}).find('a', {'class':'card__title'}).get('href')

            if 'https://www.foxtrot.com.ua' not in url_products:
                _create_full_link = 'https://www.foxtrot.com.ua' + url_products
                all_product_links.append(_create_full_link)

            for _new_list in all_product_links:
                product_links_for_get_reviews.append(_new_list)

                print(product_links_for_get_reviews)


# def get_link_products():
#     with open(config.ALL_PRODUCTS_HTML, 'r') as file:
#         file = file.read()
        
#     soup = bs4.BeautifulSoup(file, 'html.parser')

    # print(block)


        




        

def main():
    index_page()

    with open(config.INDEX_PAGE_HTML, 'r') as file:
        file = file.read()
        
    catalog_with_product(file)

    open_links_type_products()

    blocks_with_products()

    # get_link_products()


if __name__ == '__main__':
    main()
