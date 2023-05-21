def shopping(shop_file):
    shop_dict = {} # 생성할 사전 객체
    
    with open(f"data/{shop_file}") as f:
        for line in f:
            try:
                product, price = line.strip().split()
            except:
                continue
        
            if '원' not in price:
                continue
            shop_dict[product] = int(price.replace('원', ''))

    return shop_dict

def item_price(shop_file, item):
    shoppingDict = shopping(shop_file)
    return shoppingDict[item]