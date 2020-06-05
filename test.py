import requests, json, dotenv, os


data = requests.get("http://infagsuso.bplaced.net/project/")


product_prices = {}
iterator = 0
for line in data.iter_lines():
    iterator += 1
    if iterator == 1:
        pass
    elif iterator == 2:
        product_prices[str(line.decode("utf-8").strip("[]"))] = 0
        product = str(line.decode("utf-8").strip("[]"))
    elif iterator == 3:
        product_prices[product] = float(line.decode("utf-8").strip("[]"))
        iterator = 0


print(json.dumps(product_prices))
