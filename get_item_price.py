import requests
import json
import npc_price
from products import get_products
from dotenv import load_dotenv
import os


def request(itemID, amount=1, arg1=1, checknpcprice=True):
    try:
        load_dotenv()
        TOKEN = os.getenv("HYPIXEL_API_TOKEN")
        data = requests.get(f"https://api.hypixel.net/skyblock/bazaar/product?key={TOKEN}&productId=" + itemID).json()
    except TypeError:
        return({"success": False, "cause": "TypeError"})
    if data["success"] == False:
        success = False
        prices = [0, 0]
    else:
        success = True
        if arg1 == 0:
            quick_sell = data["product_info"]["quick_status"]["buyPrice"]
            quick_buy = data["product_info"]["quick_status"]["sellPrice"]
            prices = {"sell": quick_sell, "buy": quick_buy}
        else:
            buy_data = data["product_info"]["buy_summary"]
            highest = 0
            for element in buy_data:
                if float(element["pricePerUnit"]) >= highest:
                    highest = float(element["pricePerUnit"])
            buy_price = highest

            sell_data = data["product_info"]["sell_summary"]
            lowest = 1_000_000_000
            for element in sell_data:
                if float(element["pricePerUnit"]) <= lowest:
                    lowest = float(element["pricePerUnit"])
            sell_price = lowest

        if npc_price.get_item_price(itemID) > sell_price and checknpcprice and (itemID in get_products()):
            sell_price = npc_price.get_item_price(itemID)

        prices = {"buy": amount * buy_price, "sell": amount * sell_price}
            
            
    return({"success": success, "prices": prices})


if __name__ == "__main__":
    print(request("CLAY_BALL"))