
import requests
import minion_list
import get_api_token

"""
def get_products():
    product_data = requests.get(f"https://api.hypixel.net/skyblock/bazaar/products?key={get_api_token.get(1)}").json()
    if not product_data["success"]:
        print("An Error occured while downloading the api data.")
        return(False)
    else:
        productIDs = product_data["productIds"]
        
    delete = []
    not_counted = [
        "ENCHANTED",
        "TARANTULA",
        "TOOTH",
        "REVENANT",
        "FRAGMENT",
        "SUMMONING_EYE",
        "GIFT",
        "CATALYST",
        "BLOCK",
        "COMPACTOR",
        "CANDY",
        "HOT_POTATO_BOOK",
        "PACKED",
        "SUPER",
        "STOCK_OF_STONKS"
    ]

    for productID in productIDs:
        for item in not_counted:
            if item.upper() in productID:
                append = True
                for todelete in delete:
                    if todelete == productIDs.index(productID):
                        append = False
                if append == True: delete.append(productIDs.index(productID))

    for element in delete:
        productIDs.pop(element - delete.index(element))
    
    productIDs.append("ENCHANTED_EGG")
    productIDs.append("ENCHANTED_GUNPOWDER")

    return(productIDs)
"""
def get_products():
    import minion_list
    minion_list = minion_list.get()[1]
    itemIDs = []
    for minion in minion_list:
        for product in minion_list[minion]["Products"]:
            if not product["Name"] == False:
                try:
                    pos = itemIDs.index(product["Name"])
                except ValueError:
                    itemIDs.append(product["Name"])
    return(itemIDs)

if __name__ == "__main__":
    print(get_products())