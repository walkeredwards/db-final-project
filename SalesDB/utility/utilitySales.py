from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

path_to_certificate = '../X509-cert-1147331512641107939.pem'

uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource\
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=\
majority'

client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))

class saleItem:
    def __init__(self, name, price_paid, quantity):
        self.name = name
        self.price_paid = price_paid
        self.quantity = quantity

def get_next_order_number(collection):
    result = collection.find_one(sort=[("Order Number", -1)], projection={"Order Number": 1})
    #help from online resources
    return (result["Order Number"] + 1) if result else 1

def newSale(collection):
    current_datetime = datetime.now()
    order_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = input("Where is this sale shipping to? ")
    how_many = int(input("How many items are being shipped in this shipment?"))
    items = []
    for i in range(how_many):
        name = input("Whats the name of the item: ")
        price_paid = float(input("How much is the item: "))
        quantity = int(input("How many of these items were bought: "))
        item_temp = saleItem(name, price_paid, quantity)
        items.append(item_temp)
    order_number = get_next_order_number(collection)
    total_price = price_paid * quantity
    document = {
        'DatePlaceedOrder': order_time,
        'Items': items,
        'Shipping Address': location,
        'Order Number' : order_number,
        'Total Price' : total_price
    }
    collection.insert_one(document)
    print("Document created successfully.")
    print(f"Your Order Number is {order_number}")

def update_shipping_location(collection):
    order_num = int(input("Please enter your order number: "))
    new_address = input("Please enter new shipping address: ")

    search = {"Order Number": order_num}
    order = collection.find_one(search)
    if order:
        collection.update_one(search, {"$set": {"Shipping Address": new_address}})
        print(f"Shipping address for order {order_num} updated successfully.")
    else:
        print("No Order found with order number.")

def update_item_(collection):
    order_num = int(input("Please enter your order number: "))
    old_name = input("Please enter the name of the item to change: ")

    search = {"Order Number": order_num,}

    new_item = input("Please enter name of new item: ")
    new_price = input("What is the price of the new item")




def look_up(collection):
    order_num = int(input("Please enter your order number: "))
    search = {"Order Number": order_num}
    return collection.find_one(search)
    