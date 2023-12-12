from rich.console import Console
from utility import utilityInventory
from utility import utilitySales
from pymongo import MongoClient
from pymongo.server_api import ServerApi

console = Console()

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
    text = """
[bold teal]Inventory Menu[/bold teal]
=============

Select one of the following menu options:
1. [chartreuse1]Add a New Shipment[/chartreuse1]
2. [chartreuse1]Look up Shipment by date[/chartreuse1]
3. [chartreuse1]Look up Item[/chartreuse1]
4. [chartreuse1]Look up Shipment by supplier[/chartreuse1]
5. [chartreuse1]Update Supplier[/chartreuse1]
6. [chartreuse1]Update Item Amount[/chartreuse1]
7. [red]Exit the program[/red]
"""
    console.print(text)
    console.print("[teal]Enter an option: [1-7]: [/teal]", end=" ")
    option = input(' ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 7:
                return opt
        console.print("[teal]Enter a valid option.[/teal]", end=" ")
        option = input(" ")

def show_tableMenu() -> int:
    text = """
[bold teal]Welcome to GJ-Market Database[/bold teal]
=============

Are you working in [chartreuse1]Sales[/chartreuse1] or [chartreuse1]Inventory[/chartreuse1]?
1. [chartreuse1]Working in Sales[/chartreuse1]
2. [chartreuse1]Working in Inventory[/chartreuse1]
3. [red]Exit[/red]
"""
    console.print(text)
    console.print("[teal]Enter an option: [1-3]: [/teal]", end=" ")
    option = input('')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 3:
                return opt
        console.print("[teal]Enter a valid option: [/teal]", end=" ")
        option = input('')

def show_salesMenu() -> int:
    text = """
[bold teal]Sales Menu[/bold teal]
=============

Select one of the following menu options:
1. [chartreuse1]Add a New Sale[/chartreuse1]
2. [chartreuse1]Update Shipping Location[/chartreuse1]
3. [chartreuse1]Update Item and Price[/chartreuse1]
4. [chartreuse1]Update Date and Time[/chartreuse1]
5. [chartreuse1]Look up Sale[/chartreuse1]
6. [chartreuse1]Cancel Order[/chartreuse1]
7. [red]Exit the program[/red]
"""
    console.print(text)
    console.print("[teal]Enter an option: [1-7]: [/teal]", end=" ")
    option = input('')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 7:
                return opt
        console.print("[teal]Enter a valid option: [/teal]", end=" ")
        option = input("")

def main() -> None:
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
                elif option == 2:
                    utilitySales.update_shipping_location(collection)
                elif option == 3:
                    utilitySales.update_item(
                        collection, collection2)  # item and price
                elif option == 4:
                    utilitySales.update_date_and_time(collection)
                elif option == 5:
                    utilitySales.look_up(collection)
                elif option == 6:
                    utilitySales.delete_by_order_num(collection, collection2)
        elif option == 2:
            collectionShip = db["shipment"]
            collectionInv = db["inventory"]
            while True:
                option = show_inventoryMenu()
                if option == 7:
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
