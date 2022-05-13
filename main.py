import base64
import bs4
import requests
import json
import pybase64

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


# Select of multiple categories products.
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


# Selection of multiple products to collect reviews
def collect_multiple_links(title):
    links_for_collect_reviewes = []

    mobile_phone_links = {}
    televizory_links = {}
    noutbuki_links = {}

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

                title_product = blocks_products.find('div', {'class':'card js-card sc-product'}).find('div', {'class':'card__body'}).find('a').text

                title_clipping = ' '.join(title_product.split(' ')[:6]).replace('/', '-')

                get_url_product = config.URL_BASIC_PAGE + blocks_products.find('div', {'class':'card js-card sc-product'}).find('div', {'class':'card__body'}).find('div', {'class':'card__col-info'}).find('a', {'class':'card__comments'}).get('href')

                if 'mobilnye_telefony' in get_url_product and len(mobile_phone_links) != 3:
                    mobile_phone_links[title_clipping] = get_url_product

                if 'led_televizory' in get_url_product and len(televizory_links) != 3:
                    televizory_links[title_clipping] = get_url_product

                if 'noutbuki' in get_url_product and len(noutbuki_links) != 3:
                    noutbuki_links[title_clipping] = get_url_product

    links_for_collect_reviewes = {**mobile_phone_links, **televizory_links, **noutbuki_links}

    return links_for_collect_reviewes


# Request and Save product page in HTML-file for collect reviews
def save_product_page(review_links):
    title_files = []

    for title_product, link in review_links.items():
        try:
            response = requests.get(url=link, headers=config.HEADERS)

            # with open(f'{config.HTML_FILES}{title_product}.html', 'w', encoding='utf-8') as file:
            #     file.write(str(response))
            #     file.close()

        except Exception as ex:
            print(ex)

        title_files.append(title_product)

    return title_files


# Collecting links with reviews
def collect_links_reviews(title_html_files):
    links_with_reviews = {}

    for title_file in title_html_files:
        with open(f'{config.HTML_FILES}{title_file}.html', 'r') as file:
            file = file.read()

        soup = bs4.BeautifulSoup(file, 'html.parser')

        convert_urls_to_byte = base64.b64decode(soup.find('div', {'id':'comment-list-popup'}).get('data-url'))
        convert_to_ascii = config.URL_BASIC_PAGE + convert_urls_to_byte.decode('utf-8')

        title_key = f'{title_file} page reviews'

        links_with_reviews[title_key] = convert_to_ascii

    return links_with_reviews


# Sending request to reviews links and saving to HTML-file
def request_links_reviews(reviewe_links):
    title_page_reviews = []

    for key, value in reviewe_links.items():
        try:
            response = requests.get(url=value, headers=config.HEADERS).text

            with open(f'{config.HTML_FILES}{key}.html', 'w', encoding='utf-8') as file:
                file.write(str(response))
                file.close()

        except Exception as ex:
            print(ex)

        title_page_reviews.append(key)

    return title_page_reviews


# Collecting data from reviewe links (Name user, Date, Review, Number of Stars placed, Pros, Minuses and Answer (if there))
def collecting_reviews(title_page_reviews):
    dignity_products = {}
    limitations_products = {}

    for title_file in title_page_reviews:
        with open(f'{config.HTML_FILES}{title_file}.html', 'r') as file:
            file = file.read()

        soup = bs4.BeautifulSoup(file, 'html.parser')

        get_blocks_with_data = soup.find('div', {'class':'popup-comment-list__body'}).find('div', {'class':'comments-container'}).find_all('article')

        for data in get_blocks_with_data:
            
            # User feedback
            name_reviewer = data.find('div', {'class':'product-comment__item'}).find('div', {'class':'product-comment__item-title'}).text.strip()

            date_review = data.find('div', {'class':'product-comment__item'}).find('div', {'class':'product-comment__item-col'}).text.strip()

            text_review = data.find('div', {'class':'product-comment__item'}).find('div', {'class':'product-comment__item-col_content'}).find('div').text.strip()


            block_dignities_and_limitations = data.find('div', {'class':'product-comment__item'}).select('div > div:nth-of-type(4)')

            for dignities_and_limitations in block_dignities_and_limitations:
                block_dignities = dignities_and_limitations.select('ul > li:nth-of-type(1)')

                for dignities in block_dignities:
                    title_dignities = dignities.find('label').text
                    text_dignities = dignities.find('p').text
                    
                    dignity_products[title_dignities] = text_dignities


                block_limitations = dignities_and_limitations.select('ul > li:nth-of-type(2)')

                for limitations in block_limitations:
                    title_limitations = limitations.find('label').text
                    text_limitations = limitations.find('p').text

                    limitations_products[title_limitations] = text_limitations

            # Response to user feedback
            name_responser = data.find('div', {'class':'product-comment__sub'}).find('div', {'class':'product-comment__item-title'}).text.strip()

            date_response = data.find('div', {'class':'product-comment__sub'}).find('div', {'class':'product-comment__item-title'}).find('div').text.strip()



def main():
    # request_basic_page()
    # categories()
    title_sub_category_products = category_page_request()
    links_for_scraping = collect_multiple_links(title=title_sub_category_products)
    page_product = save_product_page(review_links=links_for_scraping)
    get_links_reviews = collect_links_reviews(title_html_files=page_product)
    response_reviewe_links = request_links_reviews(reviewe_links=get_links_reviews)
    collecting_reviews(title_page_reviews=response_reviewe_links)


if __name__ == '__main__':
    main()





# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=8032&classId=60
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=8042&classId=60
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=7765&classId=60
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=4065&classId=977
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=3697&classId=977
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=4021&classId=977
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=20260&classId=58
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=21264&classId=58
# https://www.foxtrot.com.ua/ru/product/commentspopup?catalogObjectId=18124&classId=58
