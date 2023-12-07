from utility import utilityInventory
from utility import utilitySales
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.errors import OperationFailure

path_to_certificate = 'SalesDB/X509-cert-1147331512641107939.pem'
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
    2. Look up Shipment by date
    3. Look up Item
    4. Look up Shipment by supplier
    5. Update Supplier
    6. Update Item Amount
    7. Delete Shipment
    8. Exit the program
    """
    print(text)
    option = input('Enter an option: [1-10]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 10:
                return opt
        option = input("Enter a valid option: ")


def show_tableMenu() -> int:
    """Displays menu for working in with diferent collections."""
    text = """
    Welcome to GJ-Market Database
    =============

    Are you working in Sales or Inventory?:
    1. Working in Sales
    2. Working in Inventory
    3. Exit
    """
    print(text)
    option = input('Enter an option: [1-3]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 3:
                return opt
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
            if 1 <= opt <= 7:
                return opt
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
        elif option == 1:
            collection = db["sales"]
            collection2 = db["inventory"]
            while True:
                option = show_salesMenu()
                if option == 7:
                    break
                elif option == 1:
                    utilitySales.new_sale(collection, collection2)
                    break
                elif option == 2:
                    utilitySales.update_shipping_location(collection)
                    break
                elif option == 3:
                    utilitySales.update_item(
                        collection, collection2)  # item and price
                    break
                elif option == 4:
                    utilitySales.update_date_and_time(collection)
                    break
                elif option == 5:
                    utilitySales.look_up(collection)
                    break
                elif option == 6:
                    utilitySales.delete_by_order_num(collection, collection2)
                    break
        elif option == 2:
            collectionShip = db["shipment"]
            collectionInv = db["inventory"]
            while True:
                option = show_inventoryMenu()
                if option == 9:
                    break
                elif option == 1:
                    utilityInventory.newShipment(collectionShip, collectionInv)
                elif option == 2:
                    utilityInventory.findShipmentDate(collectionShip)
                elif option == 3:
                    utilityInventory.findShipmentItem(collectionShip)
                elif option == 4:
                    supplier = input(
                        "What supplier shipments would you like to look for? ")
                    utilityInventory.findShipmentSupplier(
                        collectionShip, supplier)
                elif option == 5:
                    supplier = input(
                        "What is the supplier you would like to update? ")
                    utilityInventory.updateSupplier(collectionShip, supplier)
                elif option == 6:
                    utilityInventory.updateItemAmount(
                        collectionShip, collectionInv)
                elif option == 7:
                    utilityInventory.deleteShipment(
                        collectionShip, collectionInv)


if __name__ == "__main__":
    main()
