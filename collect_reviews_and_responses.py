import base64
import bs4
import requests
import json

import config


def parsing_type_links_otzyvy(title_file, full_links):
    try:
        response = requests.get(url=full_links, headers=config.HEADERS)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

    except Exception as ex:
        print(ex)

    block_data = soup.find('div', {'class':'review-cart__comment-list__body'})

    # block_reviews = block_data