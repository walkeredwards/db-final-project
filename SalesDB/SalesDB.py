import os
import time
from typing import Tuple
from utility import utilityInventory
from utility import utilitySales
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.errors import OperationFailure

path_to_certificate = 'SalesDB/cert.pem'

uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource\
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=\
majority'
client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))

def show_inventoryMenu() -> int:
    """Displays menu.
        Must be changed later"""
    text = """
    Inventory Menu
    =============

    Select one of the following menu options:
    1. Setup Database
    2. Add a New Shipment
    3. Update Suplier
    4. Update Item Name
    5. Update Date and Time
    6. Update Item Amount
    7. Delete Sale
    8. Exit the program
    """
    print(text)
    option = input('Enter an option: [1-8]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 8:
                return opt
        os.system('clear')
        option = input("Enter a valid option: ")
    
def show_tableMenu() -> int:
    """Displays menu for working in wich table .
        Must be changed later"""
    text = """
    Welcome to Fencemart Database
    =============

    Are you working in Sales or Inventory?:
    1. Working in Sales
    2. Working in Inventory
    3. Exit
    
    #Maybe add a both option or get rid of this after and make specific options to change tables
    """
    print(text)
    option = input('Enter an option: [1-3]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 3:
                return opt
        os.system('clear')
        option = input("Enter a valid option: ")
        
def show_salesMenu() -> int:
    """Displays menu.
        Must be changed later"""
    text = """
    Sales Menu
    =============

    Select one of the following menu options:
    1. Add a New Sale
    2. Update Shipping Location
    3. Update Item and Price
    4. Update Date and Time
    5. Look up Sale
    6. Cancel Order
    7. Exit the program
    """
    print(text)
    option = input('Enter an option: [1-7]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 8:
                return opt
        os.system('clear')
        option = input("Enter a valid option: ")


def main() -> None:
    """Main function.
    """
    # Connect to database
    db = client["sample_supplies"]
    while True:
        option = show_tableMenu()
        if option == 3:
            exit(0)
        if option == 1:
            collection = db["sales"]
            collection2 = db["inventory"]
            option1 = show_salesMenu()
            while True:
                if option1 == 7:
                    exit(0)
                elif option1 == 1:
                    utilitySales.new_sale(collection, collection2)
                    break
                elif option1 == 2:
                    utilitySales.update_shipping_location(collection)
                    break
                elif option1 == 3:
                    utilitySales.update_item(collection, collection2)#item and price
                    break
                elif option1 == 4:
                    utilitySales.update_date_and_time(collection)
                    break
                elif option1 == 5:
                    utilitySales.look_up(collection)
                    break
                elif option1 == 6:
                    utilitySales.delete_by_order_num(collection, collection2)
                    break
                
            
        if option == 2:
            collection = db["inventory"]
            option = show_inventoryMenu()
            while True:
                if option == 8:
                    exit(0)
                
                """
                elif option == 1:
                    setup_database(collection)
                elif option == 2:
                    add_student(collection)
                elif option == 3:
                    add_grades(collection)
                elif option == 4:
                    read_student(collection)
                elif option == 5:
                    update_student(collection)
                elif option == 6:
                    update_grades(collection)
                elif option == 7:
                    delete_student(collection)
                """
            
            
            
    


if __name__ == "__main__":
    main()
