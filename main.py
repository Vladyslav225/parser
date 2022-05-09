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



            

# Get products
def products(title):
    for item in title:
        with open(f'{config.HTML_FILES}{item}.html', 'r') as file:
            file = file.read()

        soup = bs4.BeautifulSoup(file, 'html.parser')

        conteiner_block = soup.find_all('div', {'class':'container'})

        for some in conteiner_block:
            get_ = some.find('div', {'class':'listing__body'}).find('div').find('div', {'class':'listing__body-wrap image-switch'})
            print(get_)

        


#TODO Collect feedback from links with the type otzyvy
#TODO Collect feedback from links with the type anchor


def main():
    # request_basic_page()
    # categories()
    title = category_page_request()
    products(title=title)

if __name__ == '__main__':
    main()
