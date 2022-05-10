import bs4
import requests
import json

import config


# Basic page save to file html
def request_basic_page():
    try:
        response = requests.get(url=config.URL_BASIC_PAGE, headers=config.HEADERS).text

        with open(f'{config.HTML_FILES}basic_page.html', 'w', encoding='utf-8') as file:
            file.write(str(response))
            file.close()

    except Exception as ex:
        print(ex)


# Get all elements from the catalog
def categories():
    links_type_products = {}

    with open(f'{config.HTML_FILES}basic_page.html', 'r') as file:
        file = file.read()

    try:
        soup = bs4.BeautifulSoup(file, 'html.parser')

    except Exception as ex:
        print(ex)

    get_block_catalog = soup.find('div', {'class':'catalog__wrap'}).find('ul').find_all('li')

    for type_product in get_block_catalog[1:]:

        text_type_products = type_product.find('div').find('a').find('p').text

        url_type_products = type_product.find('div').find('a').get('href')

        if 'https://www.foxtrot.com.ua' not in url_type_products:
            _create_full_link = 'https://www.foxtrot.com.ua' + url_type_products

        links_type_products[text_type_products] = _create_full_link

    with open(f'{config.JSON_FILES}catalog_with_type_products.json', 'w') as file:
        json.dump(links_type_products, file, indent=4, ensure_ascii=False)


# Select multiple categories products.
# Send request to page Categories and save to html file
def category_page_request():
    title_sub_categies = []

    with open(f'{config.JSON_FILES}catalog_with_type_products.json') as file:
        json_file = json.load(file)

    for title_category, url_category in json_file.items():
        if title_category in ['Cмартфоны', 'Ноутбуки, ПК, планшеты', 'Телевизоры, аудиотехника']:
            
            try:
                response_categories = requests.get(url=url_category, headers=config.HEADERS)

                soupe_categories = bs4.BeautifulSoup(response_categories.text, 'html.parser')

            except Exception as ex:
                print(ex)
            
            get_title_sub_category = soupe_categories.find('div', {'class':'category'}).find('div').find('div', {'class':'category__item-body'}).find('a').text
            title_sub_categies.append(get_title_sub_category)

            get_url_sub_category = config.URL_BASIC_PAGE + soupe_categories.find('div', {'class':'category'}).find('div').find('a').get('href')
            
            response_subcategories = requests.get(url=get_url_sub_category, headers=config.HEADERS).text

            with open(f'{config.HTML_FILES}{get_title_sub_category}.html', 'w', encoding='utf-8') as file:
                file.write(str(response_subcategories))
                file.close()

    return title_sub_categies


# Getting product links to collect feedback
def collect_links_reviewes(title):
    links_for_collect_feedback = []

    mobile_phone_links = []
    televizory_links = []
    noutbuki_links = []

    for item in title:
        with open(f'{config.HTML_FILES}{item}.html', 'r') as file:
            file = file.read()

        soup = bs4.BeautifulSoup(file, 'html.parser')

        conteiner_block = soup.find_all('div', {'class':'container'})

        for general_blocks in conteiner_block:
            getting_general_blocks = general_blocks.find('div', {'class':'listing__body'})

            if getting_general_blocks == None:
                continue

            getting_sub_block = getting_general_blocks.find('div', {'class':'listing__body-wrap image-switch'})

            if getting_sub_block == None:
                continue

            getting_block_article = getting_sub_block.find('section').find_all('article')

            if getting_block_article == None:
                continue

            for blocks_products in getting_block_article:
                check_comments = blocks_products.find('div', {'class':'card js-card sc-product'}).find('div', {'class':'card__body'}).find('div', {'class':'card__col-info'}).find('a', {'class':'card__comments'}).find('p')

                if check_comments == None:
                    continue

                get_url_product = config.URL_BASIC_PAGE + blocks_products.find('div', {'class':'card js-card sc-product'}).find('div', {'class':'card__body'}).find('div', {'class':'card__col-info'}).find('a', {'class':'card__comments'}).get('href')

                if 'mobilnye_telefony' in get_url_product and len(mobile_phone_links) != 3:
                    mobile_phone_links.append(get_url_product)

                if 'led_televizory' in get_url_product and len(televizory_links) != 3:
                    televizory_links.append(get_url_product)

                if 'noutbuki' in get_url_product and len(noutbuki_links) != 3:
                    noutbuki_links.append(get_url_product)

    links_for_collect_feedback = [*mobile_phone_links, *televizory_links, *noutbuki_links]

    return links_for_collect_feedback


# Collecting data (Name user, Date, Review, Number of Stars placed, Pros, Minuses and Answer (if there))
def collecting_data_from_reviews(feedback_links):
    for links in feedback_links:
        try:
            response = requests.get(url=links, headers=config.HEADERS)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')

        except Exception as ex:
            print(ex)

        get_title_product = soup.find('section', {'class':'main-reviews container'}).find('h2', {'class':'page__title nowrap js-toggle-card-box'}).find('label').text
        print(get_title_product)

        #TODO Create new title product

        get_block_comment = soup.find('section', {'class':'main-reviews container'}).find('div', {'class':'main-reviews__body js-toggle-body'}).find('div').find_all('div', {'class':'product-comment__item-title'})

        for text in get_block_comment:
            print(text.text)
        
        

def main():
    # request_basic_page()
    # categories()
    title = category_page_request()
    links_for_scraping = collect_links_reviewes(title=title)
    collecting_data_from_reviews(feedback_links=links_for_scraping)


if __name__ == '__main__':
    main()
