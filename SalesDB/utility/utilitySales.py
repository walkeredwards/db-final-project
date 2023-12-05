from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi

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

def test_push(collection):
    current_datetime = datetime.now()
    order_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = "Denver"
    how_many = 2
    items = []
    for i in range(how_many):
        name = "Pen"
        price_paid = 2
        quantity = 10
        item_temp = saleItem(name, price_paid, quantity)
        items.append(item_temp)
    order_number = 1
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

def update_item(collection):
    order_num = int(input("Please enter your order number: "))
    old_name = input("Please enter the name of the item to change: ")

    search = {"Order Number": order_num, "Items.name": old_name}
    order = collection.find_one(search)

    if order:
        new_item = input("Please enter name of new item: ")
        new_price = float(input("What is the price of the new item: "))
        new_quantity = int(input("How many of the new items: "))

        item_index = next((index for (index, item) in enumerate(order['Items']) if item['name'] == old_name), None)
        #help from online resources ^

        if item_index is not None:
            collection.update_one(
                {"Order Number": order_num, "Items.name": old_name},
                {
                    "$set":{
                        f"Items.{item_index}.name": new_item,
                        f"Items.{item_index}.price_paid": new_price,
                        f"Items.{item_index}.quantity": new_quantity
                    }
                }
            )
            print("Item successfully updated")
        else:
            print("Item not found in order number")
    else:
        print("No order found with given order number") 

def update_date_and_time(collection):
    order_num = int(input("Please enter your order number: "))

    search = {"Order Number": order_num}
    order = collection.find_one(search)

    if order:
        current_time = datetime.now()
        new_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        collection.update_one({"Order Number": order_num}, {"$set": {"DatePlacedOrder": new_time}})
        print("Date and Time updated to current date and time")
    else:
        print("No order found with given order number")

def look_up(collection):
    order_num = int(input("Please enter your order number: "))
    search = {"Order Number": order_num}
    return collection.find_one(search)
    