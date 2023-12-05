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

def newSale(collection):
    current_datetime = datetime.now()
    orderTime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = input("Where is this sale shipping to? ")
    howMany = input("How many items are being shipped in this shipment?")
    for i in range(howMany):
        if i == 1:
            name = input("Whats the name of the item?")
            quantity = int(input("How many of these items are being shipped? "))
            pridePaid = float(input("What is the total price for the order? "))
            itemsClass = saleItem
        if i > 1:
            
    document = {
        'arrivalDate': orderTime,
        'Items': [],
        'storageLocation': location
    }
    collection.insert_one(document)
    print("Document created successfully.")