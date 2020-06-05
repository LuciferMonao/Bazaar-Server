import requests, json, pythonping, datetime, dotenv, os, concurrent.futures as future, time, colorama

class item:
    def __init__(self, productID):
        self.productID = productID
        self.price = {"buy": 0, "sell": 0}
    
    def refresh_price(self):
        data = get_product_price(self.productID)
        if not data["success"] == False: self.price = data["prices"]

def get_product_price(itemID):
    if not itemID == False and not itemID == True and not itemID == None:
        dotenv.load_dotenv()
        TOKEN = os.getenv("HYPIXEL_API_TOKEN")
        data = requests.get(f"https://api.hypixel.net/skyblock/bazaar/product?key={TOKEN}&productId=" + itemID).json()
        if data["success"] == False:
            success = False
            prices = [0, 0]
            print("A problem occured while Loading the prices of {}, cause: {}, time: {}".format(itemID,data["cause"], datetime.datetime.now()))
            with open("err.log", "a") as f: f.write("time: {}, cause: {}, itemID: {}\n".format(datetime.datetime.now(), data["cause"], itemID))
        else:
            success = True
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

            with open("npc_prices.txt", "r") as f:
                try:
                    npc_price = json.load(f)[itemID]
                    if npc_price > sell_price:
                        sell_price = npc_price
                except KeyError:
                    pass

            prices = {"buy": buy_price, "sell": sell_price}
            return({"success": success, "prices": prices})
    else:
        return({"success": False, "prices": {"buy":0, "sell": 0}})

def get_product_list():
    with open("minion_data.txt", "r") as f: data = json.load(f)
    products = []
    for key in data:
        for product in data[key]["Products"]:
            products.append(product["Name"])
    return(products)



WAIT = 200

print(colorama.Fore.RED, "main", colorama.Fore.WHITE, "Successfully started the main_function.")
product_prices = {}
products = []
for number, product in enumerate(get_product_list()):
    products.append(item(product))
    print(colorama.Fore.RED,f"main", colorama.Fore.WHITE, f"Created Object for item {product}, {number}/{len(get_product_list())}")
while True:
    for number, item in enumerate(products):
        print(colorama.Fore.RED, f"main", colorama.Fore.WHITE, f"Refreshing price of {item.productID}, {number}/{len(products)}")
        item.refresh_price()
        product_prices[item.productID] = item.price["sell"]
        
    dotenv.load_dotenv()
    URL = "http://infagsuso.bplaced.net/project/getdata.php"
    TOKEN = os.getenv("SUSO_DATABASE_API_TOKEN")

    print(product_prices)
    PARAMS = {
        "tkn": TOKEN,
        "data": json.dumps(product_prices)
    }

    r = requests.post(url=URL, params=PARAMS) 
    data = r.text
    print(data)
    
    for waited in range(WAIT): time.sleep(1); print(colorama.Fore.RED, "main", colorama.Fore.WHITE, f"{waited}/{WAIT}")
