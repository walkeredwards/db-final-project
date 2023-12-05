from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from datetime import datetime
# from pymongo.errors import OperationFailure
# from datetime import datetime

path_to_certificate = '/home/hectorramirez/gitHub/X509-\
cert-1147331512641107939.pem'
# path_to_certificate =''
uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource\
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=\
majority'

client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))


class InventoryItem:
    def __init__(self, name, tags, pricePaid, quantity):
        self.name = name
        self.tags = tags
        self.pricePaid = pricePaid
        self.quantity = quantity


def newShipment(collection):
    current_datetime = datetime.now()
    arrival_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = input("What warehouse location this shipment arrived? ")
    supplier = input("From wich suplier? ")
    item_count = int(input("How many items arrived in this shipment? "))

    items = []
    for _ in range(item_count):
        name = input("What is the name of the item? ")
        quantity = int(input("How many units arrived? "))
        price_paid = float(input("What is the price paid for this item? "))
        add_tags = input("Would you like to add tags? (Y/n) ").lower() == 'y'

        tags = []
        if add_tags:
            tag_count = int(input("How many tags would you like to add? "))
            for i in range(tag_count):
                tags.append(str(input(f"Enter tag #{i + 1}: ")))
        if _ == 0:
            items.append(InventoryItem(name, tags, price_paid, quantity))
            print(items[_].tags)
            shipment_document = {
                "arrivalDate": arrival_time,
                "Items": [{"name": items[0].name, "tags": items[0].tags, "pricePaid": items[0].pricePaid, "quantity": items[0].quantity}],
                "storageLocation": location,
                "supplier": supplier
            }

            try:
                collection.insert_one(shipment_document)
                print("Document created successfully.")
            except OperationFailure as ex:
                raise ex
        if _ > 0:
            items.append(InventoryItem(name, tags, price_paid, quantity))
            item_document = {
                "arrivalDate": arrival_time,
                "Items": [{"name": items[_].name, "tags": items[_].tags, "pricePaid": items[_].pricePaid, "quantity": items[_].quantity}],
                "storageLocation": location,
                "supplier": supplier
            }
            try:
                collection.update_one(
                    {"arrivalDate": arrival_time},
                    {"$push": {
                        "Items": {
                            "name": items[_].name,
                            "tags": items[_].tags,
                            "pricePaid": items[_].pricePaid,
                            "quantity": items[_].quantity
                        }
                    }}
                )
                print("Document appended successfully.")
            except OperationFailure as ex:
                raise ex

def findShipment(collection, supplier):#maybe select a diferent way of looking
    try:
        result = collection.find_one({"supplier": supplier})
        if result:
            print("Shipment found:")
            print(result)
        else:
            print("Shipment not found.")
    except OperationFailure as ex:
        raise ex

def updateSupplier(collection, supplier):
        try:
            new_supplier = input("Enter the new supplier: ")
        
            updatedCollection = collection.find_one_and_update(
                {"supplier": supplier},
                {"$set": {"supplier": new_supplier}},
                new = True
            )

            print("Shipment updated successfully.")
            print(updatedCollection)
        except OperationFailure as ex:
            raise ex

def deleteShipment(collection, supplier):
    try:
        collection.delete_one({"supplier": supplier})
        print("Shipment deleted successfully.")
    except OperationFailure as ex:
        raise ex

def updateShipment(collection, storageLocation):
    try:
        # Assuming you want to update the entire shipment
        new_location = input("Enter the new warehouse location: ")
        new_supplier = input("Enter the new supplier: ")
    
        collection.update_one(
            {"storageLocation": storageLocation},
            {"$set": {"storageLocation": new_location, "supplier": new_supplier}}
        )

        print("Shipment updated successfully.")
    except OperationFailure as ex:
        raise ex

def deleteShipment(collection, supplier):
    try:
        collection.delete_one({"supplier": supplier})
        print("Shipment deleted successfully.")
    except OperationFailure as ex:
        raise ex
