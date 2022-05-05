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

        correction_title = ' '.join(title_product.split(' ')[:6]).replace('/', ' ')

        find_element_coment = soup.find('div', {'class':'product-menu__card-review product-menu__card-review_static'}).find('a', {'class':'product-menu__card-comments'}).get('href')

        if 'otzyvy.html' in find_element_coment:
            links_otzyvy = 'https://www.foxtrot.com.ua' + find_element_coment
            link_type_otzyvy[title_product] = links_otzyvy
            
        elif '#anchor-3' in find_element_coment:
            links_anchor = links_for_scraping + find_element_coment
            links_type_anchor[correction_title] = links_anchor


#TODO Collect feedback from links with the type otzyvy


# Collect feedback from links with the type anchor
def open_links_type_anchor():
    reviews = {}
    pluses_and_moins = {}

    for title, link in links_type_anchor.items():
        try:
            response = requests.get(url=link, headers=config.HEADERS).text

            with open(f'/home/vladyslav/parser_eldorado/parser/html_files/{title}.html', 'w', encoding='utf-8') as file:
                file.write(str(response))
                file.close()

            with open(f'/home/vladyslav/parser_eldorado/parser/html_files/{title}.html', 'r') as file:
                file = file.read()

            soup = bs4.BeautifulSoup(file, 'html.parser')

        except Exception as ex:
            print(ex)

        find_block_reviews = soup.find('section', {'class':'main-reviews container'})

        element_all_reviews = find_block_reviews.find_all('div', {'class':'main-reviews__body js-toggle-body'})
        
        # Getting the name reviewer
        for basic_block_with_review in element_all_reviews:
            get_basic_block_with_review = basic_block_with_review.find_all('div', {'class':'main-reviews_comments-block-scroll smooth-scroll'})

            for subblock_with_review in get_basic_block_with_review:
                get_subblock_with_review = subblock_with_review.find_all('div', {'class':'product-comment__item'})

                for element_with_name in get_subblock_with_review:
                    get_text_name = element_with_name.find('div', {'class':'product-comment__item-title'}).text.strip()
                    
            # Getting the date the review was posted
                for element_with_data in get_subblock_with_review:
                    get_element_with_data = element_with_data.find_all('div', {'class':'product-comment__item-col'})

                    for element_with_text_date in get_element_with_data:
                        get_element_text_date = element_with_text_date.find('div', {'class':'product-comment__item-date'})

                        if get_element_text_date == None:
                            continue

                        correction_text_data = get_element_text_date.text
                        
            # Getting the review
                for element_with_review in get_subblock_with_review:
                    get_element_with_review = element_with_review.find_all('div', {'class':'product-comment__item-col product-comment__item-col_content'})

                    for text_review in get_element_with_review:
                        get_text_review = text_review.find('div', {'class':'product-comment__item-text'}).text.strip()

            # Getting pluses and moins products
                for basic_block_pluses_moins in get_subblock_with_review:
                    get_basic_block_pluses_moins = basic_block_pluses_moins.find_all('div', {'class':'product-comment__item-col'})

                    for block_pluses_moins in get_basic_block_pluses_moins:
                        get_block_pluses_moins = block_pluses_moins.find('ul', {'class':'product-comment__item-info'})
                        
                        if get_block_pluses_moins == None:
                            continue

                        get_subblock_pluses_moins = get_block_pluses_moins.find_all('li')
                        
                        for block_pluses in get_subblock_pluses_moins:
                            lable_pluses = block_pluses.find('label').text

                            text_pluses = block_pluses.find('p').text                        


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
