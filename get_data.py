import pickle
from products import get_products


def load_obj(name ):
    with open('products/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_product_prices():
    item_prices = {}
    itemIDs = get_products()

    for itemID in itemIDs:
        item_prices[itemID] = load_obj(itemID)

    return(item_prices)

def get():
    return(get_product_prices())

def get_item_price(itemID):
    return(load_obj(itemID))