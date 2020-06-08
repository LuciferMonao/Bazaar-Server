import requests, json, pythonping, datetime, dotenv, os, time, colorama, sys; from progress.bar import Bar

dotenv.load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")

WAIT =  os.getenv("WAIT")

def delete_line(amount=1):
    for _ in range(amount): sys.stdout.write("\033[F"); sys.stdout.write("\033[K")

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
            with open(FILE_PATH + "err.log", "a") as f: f.write("type: Downloaderror, time: {}, cause: {}, itemID: {}\n".format(datetime.datetime.now(), data["cause"], itemID))
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

            with open(FILE_PATH + "npc_prices.txt", "r") as f:
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
    with open(FILE_PATH + "minion_data.txt", "r") as f: data = json.load(f)
    products = []
    for key in data:
        for product in data[key]["Products"]:
            products.append(product["Name"])
    return(products)

print(colorama.Fore.RED, "main", colorama.Fore.RESET, "Successfully started the main_function.")
product_prices = {}
products = []
for number, product in Bar("Creating item objects...", max=len(get_product_list())).iter(enumerate(get_product_list())):
    products.append(item(product))
delete_line()
while True:
    for number, item  in Bar("Refreshing itemprices...", max=len(get_product_list())).iter(enumerate(products)):
        print(f" - {item.productID}")
        item.refresh_price()
        product_prices[item.productID] = item.price["sell"]
        delete_line()
    delete_line()
        
    dotenv.load_dotenv()
    URL = str(os.getenv("DATABASE_URL"))
    UPLOAD_MINION_DATA = str(os.getenv("UPLOAD_MINION_DATA"))
    TOKEN = str(os.getenv("DATABASE_API_TOKEN"))

    if UPLOAD_MINION_DATA.upper() == "TRUE": 
        with open(FILE_PATH + "minion_data.txt", "r") as f: product_prices["minion_data"] = [i for i in f.readlines()]

    if not URL.upper() == "NONE" and not TOKEN.upper() == "NONE":
        PARAMS = {
            "tkn": TOKEN,
            "data": json.dumps(product_prices)
        }

        r = requests.post(url=URL, params=PARAMS) 
        data = r.text
        print(f"Successfully uploaded the product prices, returned data: '{data}'")
        if len(data) > 2: 
            print("")
            with open(FILE_PATH + "err.log", "a") as f: f.write("type: Uploadexception, time: {}, data: {}\n".format(datetime.datetime.now(), data))
        else: delete_line()

    if os.getenv("SAVE_TO_FILE").upper() == "TRUE":
        for key in product_prices:
            with open(FILE_PATH + f"product_prices/{key}.txt", "w") as f:
                f.write(str(product_prices[key]))
    
    for waited in Bar("Pausing upload...", max=WAIT).iter(range(int(WAIT))): time.sleep(1); print(colorama.Fore.RED, "main", colorama.Fore.RESET, f"{waited}/{WAIT}");delete_line()
    delete_line()