# text = '''SAMSUNG Galaxy S20 FE 6/128GB Dual Sim ZBD Cloud Navy (SM-G780GZBDSEK)
#         OPPO A74 4/128 GB Prism Black
# APPLE iPhone 11 128GB White (M'''

# print(' '.join(text.split(' ')[:6]).replace('/', '-'))

list_ = []

some = 'a','b','a'


for item in some:
    if item in list_:
        list_.append(item)
        print(list_)

    else:
        continue


