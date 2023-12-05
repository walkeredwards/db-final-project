import os
import time
from typing import Tuple
from utility import utilityInventory
from utility import utilitySales
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.errors import OperationFailure

path_to_certificate = './X509-\
cert-1147331512641107939.pem'
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
    1. Add a New Shipment
    2. Update Suplier
    3. Update Item Name
    4. Update Item Amount
    5. Update Date and Time
    6. Delete Shipment
    7. Exit the program
    """
    print(text)
    option = input('Enter an option: [1-7]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 7:
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
    1. Setup Database
    2. Add a New Sale
    3. Update Shipping Location
    4. Update Item and Price
    5. Update Date and Time
    6. Look up Sale
    7. Cancel Order
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
            option = show_salesMenu()
            while True:
                if option == 8:
                    break
                elif option == 1:
                    setup_database(collection)
                elif option == 2:
                    utilitySales.newSale(collection)
                elif option == 3:
                    utilitySales.update_shipping_location(collection)
                elif option == 4:
                    update_name(collection)#item and price
                elif option == 5:
                    update_time(collection)#date and time
                elif option == 6:
                    utilitySales.look_up(collection)#look up
                elif option == 7:
                    delete_sale(collection) #delete sale
            
        if option == 2:
            collection = db["inventory"]
            option = show_inventoryMenu()
            while True:
                if option == 7:
                    break
                elif option == 1:
                    utilityInventory.newShipment(collection)
                elif option == 2:
                    supplier = input("What is the supplier you would like to update")
                    utilityInventory.updateSupplier(collection, supplier)
                elif option == 3:
                    utilityInventory.updateItemName(collection)
                elif option == 4:
                    utilityInventory.updateItemAmout(collection)
                elif option == 5:
                    utilityInventory.UpdateDateTime(collection)
                elif option == 6:
                    utilityInventory.deleteShipment(collection)

                    
            
            
            
    


if __name__ == "__main__":
    main()
