from pymongo import MongoClient
from pymongo.server_api import ServerApi
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

class inveventoryItem:
    def __init__(self, name, tags, pricePaid, quantity):
        self.name = name
        self.tags = tags
        self.pricePaid = pricePaid
        self.quantity = quantity


def newShipment(collection):
    current_datetime = datetime.now()
    arrivalTime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = input("What warehouse location this shipment arrived?")
    suplier = input("From wich suplier?")
    howMany = int(input("How many items arrived in this shipment?"))
    print(howMany)
    howMany = howMany-1
    print(howMany)
    itemClass = []
    for i in range(howMany):
        print(i)
        if i == 0:
            name = input("Whats the name of the item?")
            quantity = int(input("How many arrived?"))
            pridePaid = float(input("Whats the price paid for this shipment?"))
            tagsBool = input("Would you like to add tags?(Y/n)")
            if tagsBool == "Y" or tagsBool == "y":
                tagsBool = 1
            else:
                tagsBool = 0
            if tagsBool:
                tags = []
                x = int(input("How many would you like to add:"))
                for i in range(x):
                    if i == 0:
                        tags.append(str(input("")))
                    else:
                        tags.append(str(input(",")))
            itemClass.append(inveventoryItem(name, tags, pridePaid, quantity))
            
            document = {
            "arrivalDate": arrivalTime,
            "Items": itemClass,
            "storageLocation": location,
            "supplier": suplier
            }
            collection.insert_one(document)
            print("Document created successfully.")
            
        if i > 1:
            name = input("Whats the name of the item?")
            quantity = int(input("How many arrived?"))
            pridePaid = float(input("Whats the price paid for this shipment?"))
            tagsBool = input("Would you like to add tags?(Y/n)")
            if tagsBool == "Y" or tagsBool == "y":
                tagsBool = 1
            else:
                tagsBool = 0
            if tagsBool:
                tags = []
                x = int(input("How many would you like to add:"))
                for i in range(x):
                    if i == 0:
                        tags.append(str(input("")))
                    else:
                        tags.append(str(input(",")))
            itemClass.append(newShipment(name, tags, pridePaid, quantity))
            print(itemClass[i])
            try:
                collection.update_one({"arrivalDate": arrivalTime}, {"$push": {"Items": itemClass[i]}})
                print("Item pushed sucssecfully.")
            except:
                print("Item push failed")
            

   
