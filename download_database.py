import requests
import json
import get_item_price
import pickle
from datetime import datetime
import time
from products import get_products
import time
import get_api_token

def save_obj(obj, name ):
    with open('products/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def download_prices():
    prices = {}
    productIDs = get_products()
    item_prices = {}
    lowest_download = {"time": 1000000.0, "item": "None"}
    highest_download = {"time": 0.0, "item": "None"}

    lowest_save = {"time": 1000000.0, "item": "None"}
    highest_save = {"time": 0.0, "item": "None"}


    for number, item in enumerate(productIDs):
        item_time = time.perf_counter()
        item_price = get_item_price.request(item)
        if item_price["success"] == True:
            item_prices[item] = item_price["prices"]["sell"]
            downloaded_time = time.perf_counter()
        else:
            print("Occurred Error while loading the price of {}. Errortype: {}.".format(item, item_price))
            exit()
        print(f"Got price for {item}".format(item=item))
        save_time_start = time.perf_counter()
        try: 
            save_obj(item_prices[item], item)
            prices[item] = item_prices[item]
        except KeyError:
            pass
        save_time_stop = time.perf_counter()
        
        if downloaded_time - item_time < lowest_download["time"]:
            lowest_download["time"] = downloaded_time - item_time
            lowest_download["item"] = item
        if downloaded_time - item_time > highest_download["time"]:
            highest_download["time"] = downloaded_time - item_time
            highest_download["item"] = item
        if save_time_stop - save_time_start < lowest_save["time"]:
            lowest_save["time"] = save_time_stop - save_time_start
            lowest_save["item"] = item
        if save_time_stop - save_time_start > highest_save["time"]:
            highest_save["time"] = save_time_stop - save_time_start
            highest_save["item"] = item
        
    return([number, lowest_download, highest_download, lowest_save, highest_save, prices]) 
    


def upload_data(data):
    
    URL = "http://infagsuso.bplaced.net/project/getdata.php"

    PARAMS = {
    "tkn":get_api_token.get(0),
    "data":str("'" + str(data[5]) + "'")
    }

    print(PARAMS)

    r = requests.post(url=URL, params=PARAMS) 
    data = r.text
    print(data)



UPLOAD_TO_DATABASE = False

if __name__ == "__main__":
    while True:
        try:
            Minutes = float(input("What should be the intervall of Download? "))
            main = True
        except ValueError:
            print("Please enter a valid Number.")
            main = False
        while main == True:

            download_start = time.perf_counter()
            print("Downloading prices via the API Socket.")
            items_loaded = download_prices()
            print("Download of {} items successfull. It took {} seconds. \nDownload: Thats an average of about {} seconds per Download.\n          The item that took the shortest was {} with {} seconds and the longest {} with {} seconds.\nSave: The item that took the shortest was {} with {} seconds and the longest {} with {} seconds.".format(items_loaded[0], time.perf_counter() - download_start, (time.perf_counter() - download_start) / items_loaded[0], str(items_loaded[1]["item"]), str(items_loaded[1]["time"]), str(items_loaded[2]["item"]), str(items_loaded[2]["time"]), str(items_loaded[3]["item"]), str(items_loaded[3]["time"]), str(items_loaded[4]["item"]), str(items_loaded[4]["time"])))

            if UPLOAD_TO_DATABASE: upload_data(items_loaded)

            Seconds = Minutes * 60
            for second in range(0, int(Seconds)):
                time.sleep(1)
                print(str(f"Right now: {second} / {int(Seconds)}"))
            