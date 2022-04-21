import bs4
import requests

import config
import collect_data_products


all_type_product = {}


def main_page(url):
    try:
        response = requests.get(url, headers=config.HEADERS).text

    except Exception as ex:
        print(ex)

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(str(response))
        file.close()


def type_product(file):
    try:
        soup = bs4.BeautifulSoup(file, 'html.parser')

    except Exception as ex:
        print(ex)

    block_type_elements = soup.find('div', {'class': 'df l0 full-width'}).find('ul', {'class': 'menu-0-2-51'}).find_all('li')

    for elements in block_type_elements:
        title = elements.find('a', {'class':'df aic jcsb'}).find('div', {'class':'df aic'}).text
        link = elements.find('a', {'class':'df aic jcsb'}).get('href')
        
        if 'https://www.ctrs.com.ua' not in link:
            full_link = 'https://www.ctrs.com.ua' + link
        
        all_type_product[title] = full_link


def data_products():
    for key, link in all_type_product.items():
        if key == 'Смартфоны':
            get_data_smartfony = collect_data_products.data_smartfony(link)

        # if key == 'Телевизоры, фото, видео':
        #     get_data_tv_photo_video = collect_data_products.data_tv_photo_video(link)

        # if key == 'Аудио':
        #     get_data_tv_photo_video = collect_data_products.data_audio(link)

        

def main():
    main_page(config.ONLINE_STORE)

    with open('index.html', 'r') as file:
        file = file.read()
    type_product(file)

    data_products()





if __name__ == '__main__':
    main()


# with open(PC_PRODUCTS_JSON, 'w') as file:
#         json.dump(list_product, file, indent=4, ensure_ascii=False)
