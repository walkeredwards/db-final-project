import pymongo
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from datetime import datetime

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

def findShipmentDate(collection):
    print("Would you like to look for a Shipment made in a specific year, month or day? ")
    option = int(input("1. Year\n2. Month\n3. Day :"))
    if option == 3:
        year_to_search = input("Enter the year (e.g., 2018): ")
        month_to_search = input("Enter the month (e.g., 07): ")
        day_to_search = input("Enter the day (e.g., 18): ")

        date_to_search = f"{year_to_search}-{month_to_search}-{day_to_search}"

        query = {"arrivalDate": {"$regex": f"^{date_to_search}T"}}
        try:
            results = collection.find(query)

            result_list = list(results)
            result_count = len(result_list)

            if result_count > 0:
                print("Shipments found:")
                for shipment in result_list:
                    print(shipment)
            else:
                print("No shipments found for the given supplier.")
        except OperationFailure as ex:
            raise ex
            
    elif option == 2:
        year_to_search = input("Enter the year (e.g., 2018): ")
        month_to_search = input("Enter the month (e.g., 07): ")

        date_to_search = f"{year_to_search}-{month_to_search}"

        query = {"arrivalDate": {"$regex": f"^{date_to_search}-"}}

        try:
            results = collection.find(query)

            result_list = list(results)
            result_count = len(result_list)

            if result_count > 0:
                print("Shipments found:")
                for shipment in result_list:
                    print(shipment)
            else:
                print("No shipments found for the given supplier.")
        except OperationFailure as ex:
            raise ex
    elif option == 1:
        year_to_search = input("Enter the year (e.g., 2018): ")

        query = {"arrivalDate": {"$regex": f"^{year_to_search}-"}}

        try:
            results = collection.find(query)

            result_list = list(results)
            result_count = len(result_list)

            if result_count > 0:
                print("Shipments found:")
                for shipment in result_list:
                    print(shipment)
            else:
                print("No shipments found for the given supplier.")
        except OperationFailure as ex:
            raise ex

def findShipmentSupplier(collection, supplier):
    try:
        result = collection.find({"supplier": supplier})

        result_list = list(result)
        result_count = len(result_list)

        if result_count > 0:
            print("Shipments found:")
            for shipment in result_list:
                print(shipment)
        else:
            print("No shipments found for the given supplier.")
    except OperationFailure as ex:
        raise ex

def findShipmentItem(collection):
    itemName = input("What's the item you are looking for? ")
    try:
        result = collection.find({"Items": {"$elemMatch": {"name": itemName}}})

        result_list = list(result)
        result_count = len(result_list)
        total = 0
        if result_count > 0:
            print(f'{result_count} shipments were found.')
            for doc in result_list:
                for item in doc['Items']:
                    if item['name'] == itemName:
                        total += int(item['quantity'])
                        print(f"{item['quantity']} {itemName} in shipment with ID {doc['_id']}")
            print(f"A total of {total} {itemName} are in storage right now.")
        else:
            print(f"No shipments found with '{itemName}' in the 'Items' array.")
    except OperationFailure as ex:
        raise ex

def returnItemCount(collection, itemName) -> int :
    try:
        result = collection.find({"Items": {"$elemMatch": {"name": itemName}}})

        result_list = list(result)
        result_count = len(result_list)
        total = 0
        if result_count > 0:
            for doc in result_list:
                for item in doc['Items']:
                    if item['name'] == itemName:
                        total += int(item['quantity'])
            return total
        else:
            return 0
    except OperationFailure as ex:
        raise ex
    
def updateSupplier(collection, supplier):
        try:
            foundIT = collection.find({"supplier": supplier})
            result_list = list(foundIT)
            result_count = len(result_list)
            if result_count > 1:
                print(f'{result_count} shipments were found with {supplier} as supplier.')
                i = 1
                for foundIT in result_list:
                    print(f'{i}.-')
                    print(foundIT)
                    i += 1
                option = int(input(f'Which shipment would you like to edit? 1 - {i-1} '))
                for foundIT in result_list:
                    if result_list == option - 1:
                        stamp = foundIT['_id'] 
                try:
                    new_supplier = input("Enter the new supplier: ")
                    updatedCollection = collection.find_one_and_update(
                        {"_id": stamp},
                        {"$set": {"supplier": new_supplier}},
                        new = True
                    )

                    print("Shipment updated successfully.")
                    print(updatedCollection)
                except OperationFailure as ex:
                    raise ex
            elif result_count == 1:     
                print(f'{result_count} shipment was found by {supplier}.')
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
            else:
                print("No records found that have that supplier.")
        except OperationFailure as ex:
            raise ex

def updateItemName(collection):
    itemName = input("What's the item you want to update? ")
    try:
        result = collection.find({"Items": {"$elemMatch": {"name": itemName}}})
        result_list = list(result)
        result_count = len(result_list)
        
        if result_count > 0:
            print(f'{result_count} shipments were found with {itemName}.')
            
            newItemName = input(f"What's the new name for {itemName}? ")
            for doc in result_list:
                for item in doc['Items']:
                    if item['name'] == itemName:
                        item['name'] = newItemName
                        print(f"Updated item name in shipment with ID {doc['_id']}")
            
            for doc in result_list:
                collection.update_one(
                    {"_id": doc['_id']},
                    {"$set": {"Items": doc['Items']}}
                )
            
            print(f"Item name updated to {newItemName} in all matching shipments.")
        else:
            print(f"No shipments found with '{itemName}' in the 'Items' array.")
    
    except OperationFailure as ex:
        raise ex

def updateShipment(collection, storageLocation):
    try:
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

