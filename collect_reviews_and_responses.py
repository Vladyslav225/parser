# Scraping reviwes and save to fila

import base64
import bs4
import requests
import json

import config


def parsing_type_links_otzyvy(title_file, full_links):
    print(title_file)
    try:
        response = requests.get(url=full_links, headers=config.HEADERS)

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

    except Exception as ex:
        print(ex)

    # Getting general block with reviews and reply to reviews
    blocks_data = soup.find('div', {'class':'review-cart__comment-list__body'}).find('div', {'class':'comments-container'}).find_all('article')

    for block in blocks_data:

        # Getting data reviews (name, number stars, date and content reviews)
        block_review = block.find('div', {'class':'product-comment__item'})

        name_reviewer = block_review.find('div', {'class':'product-comment__item-title'}).text.strip()

        raiting_review = len(block_review.find('div', {'class':'product-comment__item-col'}).find_all('i', {'class':'icon_orange'}))

        date_review = block_review.find('div', {'class':'product-comment__item-col'}).find('div', {'class':'product-comment__item-date'}).text.strip()
        
        contentreview = block_review.find('div', {'class':'product-comment__item-col_content'}).find('div', {'class':'product-comment__item-text'}).text.strip()
        

        # Getting data reply to reviews (name, number stars, date and content reviews)
        general_block_reply = block.find('div', {'class':'product-comment__sub'})
        
        if not general_block_reply:
            not_reply = 'This reviewer has`t responses to reviews'
            continue
        
        sub_block_reply = general_block_reply.find('div', {'class':'product-comment__item'})

        name_replier = sub_block_reply.find('div', {'class':'product-comment__item-title'}).text.strip()

        date_reply = sub_block_reply.find('div', {'class':'product-comment__item-col'}).find('div').text.strip()

        content_reply = sub_block_reply.find('div', {'class':'product-comment__item-col_content'}).find('div').text.strip()
        print(content_reply)



        
        



# https://www.foxtrot.com.ua/ru/shop/mobilnye_telefony_oppo_a74-4-128gb-0/otzyvy.html
# https://www.foxtrot.com.ua/ru/shop/led_televizory_hisense_32a5600f/otzyvy.html
# https://www.foxtrot.com.ua/ru/shop/led_televizory_lg_43up75006lf-0/otzyvy.html
# https://www.foxtrot.com.ua/ru/shop/noutbuki_lenovo_ideapad_gaming_3_15imh05_81y400emra/otzyvy.html
# https://www.foxtrot.com.ua/ru/shop/noutbuki_lenovo_l340-15irh-gaming-81lk01d1ra/otzyvy.html
