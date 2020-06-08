# Technical Informations

To use the upload_data.py file, there has to be a .env file in the directory.
The file has to have to following content:  

    # .env
    HYPIXEL_API_TOKEN = Token for the Hypixel Api [Obtainable by issuing the command "/api new" on the hypixel network] 
    DATABASE_API_TOKEN = Token for the database, set to None to leave out the upload
    DATABASE_URL = Url for the database, set to None to leave out the upload
    FILE_PATH = .programm_data/
    WAIT = time in seconds
    SAVE_TO_FILE = bool (True or False)
    UPLOAD_MINION_DATA = bool (True or False)

Every WAIT seconds, the programm refreshes the product prices via the hypixel bazaar api. After that it continues on to upload the prices to the DATABASE_URL with the database token DATABASE_API_TOKEN. The upload post has the PARAMS in form of a dictionary containing the api token under "tkn" and the data under "data" in a json dictionary with the item ID as name and the item price as value. Optionally you can change the programm to save the programm prices to a file in the programm_data/ folder, for that set SAVE_TO_FILE to True. If UPLOAD_MINION_DATA is true, the minion list in programm_data/minion_data.txt will be appended to the product_prices before the upload.

If there are questions remaining contact me at lucifermonao@gmx.de.
