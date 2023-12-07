import pymongo
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
from datetime import datetime
from utility import utilitySales


class InventoryItem:
    def __init__(self, name, tags, pricePaid, quantity):
        self.name = name
        self.tags = tags
        self.pricePaid = pricePaid
        self.quantity = quantity


def newShipment(collectionShip, collectionInv):
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
            shipment_document = {"arrivalDate": arrival_time,
                                 "Items": [{"name": items[0].name,
                                            "tags": items[0].tags,
                                            "pricePaid": items[0].pricePaid,
                                            "quantity": items[0].quantity}],
                                 "storageLocation": location,
                                 "supplier": supplier}
            try:
                collectionShip.insert_one(shipment_document)
                collectionInv.update_one(
                    {"item": items[0].name},
                    {
                        '$set': {
                            "item": items[0].name,
                            "quantity": items[0].quantity + utilitySales.check_main_inv(collectionInv, items[0].name)
                        }
                    },
                    upsert=True
                )
                print("Document created successfully.")
            except OperationFailure as ex:
                raise ex
        if _ > 0:
            items.append(InventoryItem(name, tags, price_paid, quantity))
            item_document = {"arrivalDate": arrival_time,
                             "Items": [{"name": items[_].name,
                                        "tags": items[_].tags,
                                        "pricePaid": items[_].pricePaid,
                                        "quantity": items[_].quantity}],
                             "storageLocation": location,
                             "supplier": supplier}
            try:
                collectionShip.update_one(
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
                collectionInv.update_one(
                    {"item": items[_].name},
                    {
                        '$set': {
                            "item": items[_].name,
                            "quantity": items[_].quantity + utilitySales.check_main_inv(collectionInv, items[_].name)
                        }
                    },
                    upsert=True
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
                        print(
                            f"{item['quantity']} {itemName} in shipment with ID {doc['_id']}")
            print(f"A total of {total} {itemName} are in storage right now.")
        else:
            print(
                f"No shipments found with '{itemName}' in the 'Items' array.")
    except OperationFailure as ex:
        raise ex


def returnItemCount(collection, itemName) -> int:
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
            option = int(
                input(f'Which shipment would you like to edit? 1 - {i-1} '))
            for foundIT in result_list:
                if result_list == option - 1:
                    stamp = foundIT['_id']
            try:
                new_supplier = input("Enter the new supplier: ")
                updatedCollection = collection.find_one_and_update(
                    {"_id": stamp},
                    {"$set": {"supplier": new_supplier}},
                    new=True
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
                    new=True
                )

                print("Shipment updated successfully.")
                print(updatedCollection)
            except OperationFailure as ex:
                raise ex
        else:
            print("No records found that have that supplier.")
    except OperationFailure as ex:
        raise ex


def updateItemAmount(collectionShip, collectionInv) -> None:
    print("To change a specific item amount in a shipment provide the following info.")
    dates = input(
        "Enter year, month, day and hour of when this shipment arrived: yyyy mm dd hh ").split()
    date_to_search = f"{dates[0]}-{dates[1]}-{dates[2]}T{dates[3]}:"
    print(date_to_search)

    query = {"arrivalDate": {"$regex": f"^{date_to_search}"}}

    try:
        results = collectionShip.find(query)

        result_list = list(results)
        result_count = len(result_list)

        if result_count > 0:
            print("Shipments found:")
            for shipment in result_list:
                print(shipment)
        else:
            print("No shipments found for the given time.")
            return
    except OperationFailure as ex:
        raise ex

    itemName = input("What's the item you are looking for? ")

    try:
        for doc in result_list:
            for item in doc['Items']:
                if item['name'] == itemName:
                    old_quantity = item['quantity']
                    new_quantity = int(
                        input(f"Enter the new quantity for {itemName}: "))
                    currentInv = utilitySales.check_main_inv(
                        collectionInv, itemName)
                    if new_quantity < old_quantity:
                        if (old_quantity - new_quantity) > currentInv:
                            print('Error setting new quantity to negatives')
                            return
                        else:
                            collectionShip.update_one(
                                {"_id": doc["_id"], "Items.name": itemName},
                                {"$set": {"Items.$.quantity": new_quantity}}
                            )
                            print(
                                f"Quantity of {itemName} updated in Shipment successfully.")
                            collectionInv.update_one(
                                {"item": itemName},
                                {
                                    '$set': {
                                        "item": itemName,
                                        "quantity": (currentInv - (old_quantity - new_quantity))
                                    }
                                },
                                upsert=False
                            )
                            print(
                                f"Quantity of {itemName} updated in Inventory successfully.")
                    else:
                        collectionShip.update_one(
                            {"_id": doc["_id"], "Items.name": itemName},
                            {"$set": {"Items.$.quantity": new_quantity}}
                        )
                        print(
                            f"Quantity of {itemName} updated in Shipment successfully.")
                        collectionInv.update_one(
                            {"item": itemName},
                            {
                                '$set': {
                                    "item": itemName,
                                    "quantity": (currentInv + (new_quantity - old_quantity))
                                }
                            },
                            upsert=False
                        )
                        print(
                            f"Quantity of {itemName} updated in Inventory successfully.")
    except OperationFailure as ex:
        raise ex


def deleteShipment(collectionShip, collectionInv):
    print("To delete a shipment, provide the following info.")
    dates = input(
        "Enter year, month, day and hour of when this shipment arrived: yyyy mm dd hh ").split()
    date_to_search = f"{dates[0]}-{dates[1]}-{dates[2]}T{dates[3]}:"
    print(date_to_search)

    query_shipment = {"arrivalDate": {"$regex": f"^{date_to_search}"}}

    try:
        result_shipments = collectionShip.find(query_shipment)
        result_list_shipments = list(result_shipments)
        result_count_shipments = len(result_list_shipments)

        if result_count_shipments > 0:
            print("Shipments found:")
            for shipment in result_list_shipments:
                print(shipment)
        else:
            print("No shipments found for the given time.")
            return
    except OperationFailure as ex:
        raise ex

    # Assuming you have a unique identifier for each item in the inventory,
    # e.g., 'name'
    item_name = input(
        "Enter the name of the item to update in the inventory: ")

    try:
        for shipment in result_list_shipments:
            for item in shipment['Items']:
                if item['name'] == item_name:
                    old_quantity = utilitySales.check_main_inv(
                        collectionInv, item_name)
                    updated_quantity = item['quantity']
                    if (old_quantity - updated_quantity) < 0:
                        print("Error.\nDelteting would make inventory negative.")
                    else:
                        collectionShip.delete_one(query_shipment)
                        print("Shipment deleted successfully.")
                        collectionInv.update_one(
                            {"item": item_name},
                            {"$set": {"quantity": (old_quantity - updated_quantity)}}
                        )
                        print(
                            f"Inventory updated for {item_name}. Quantity decreased by {updated_quantity}.")
    except OperationFailure as ex:
        raise ex
#name