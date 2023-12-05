from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

path_to_certificate = '/home/hectorramirez/gitHub/X509-\
cert-1147331512641107939.pem'

uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource\
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=\
majority'

client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))

class saleItem:
    def __init__(self, name, tags, pricePaid, quantity):
        self.name = name
        self.tags = tags
        self.priceSold = pricePaid
        self.quantity = quantity

def get_next_order_number(collection):
    result = collection.find_one(sort=[("Order Number", -1)], projection={"Order Number": 1})
    #help from online resources
    return (result["Order Number"] + 1) if result else 1

def newSale(collection):
    current_datetime = datetime.now()
    orderTime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = input("Where is this sale shipping to? ")
    howMany = int(input("How many items are being shipped in this shipment?"))
    items = []
    for i in range(howMany):
        name = input("Whats the name of the item?")
        quantity = int(input("How many of these items are being shipped? "))
        pricePaid = float(input("What is the total price for the order? "))
        item_temp = saleItem(name, [], pricePaid, quantity)
        items.append(item_temp)
    order_number = get_next_order_number(collection)        
    document = {
        'DatePlaceedOrder': orderTime,
        'Items': items,
        'Shipping Address': location,
        'Order Number' : order_number
    }
    collection.insert_one(document)
    print("Document created successfully.")

def updateShippingLocation(collection):
    order_num = int(input("Please enter your order number: "))
    new_address = input("Please enter new shipping address: ")

    search = {"Order Number": order_num}
    order = collection.find_one(search)
    if order:
        collection.update_one(search, {"$set": {"Shipping Address": new_address}})
        print(f"Shipping address for order {order_num} updated successfully.")
    else:
        print("No Order found with order number.")
    