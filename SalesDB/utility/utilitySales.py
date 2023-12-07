from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utility import utilityInventory


def get_next_order_number(collection):
    """Checks the data base for the highest order number and adds 1 to it
    If no order number start at 1

    Args:
        collection (_type_): _description_

    Returns:
        _type_: _description_
    """
    result = collection.find_one(
        sort=[("orderNumber", -1)], projection={"orderNumber": 1})
    # help from online resources
    return (result["orderNumber"] + 1) if result else 1


def newSale(collection, collection2):
    try:
        current_datetime = datetime.now()
        order_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        how_many = int(
            input("How many items are being shipped in this shipment? "))
        items = []
        total_price = 0
        for i in range(how_many):
            name = input("Whats the name of the item: ")
            price_paid = float(input("How much is the item: "))
            quantity = int(input("How many of these items were bought: "))

            inventory_count = check_main_inv(collection2, name)
            if inventory_count < quantity:
                print(f"Sorry we only have {inventory_count}, of {name}")
                return
            total_price += price_paid * quantity
            item_temp = {
                'name': name,
                'pricePaid': price_paid,
                'quantity': quantity
            }
            items.append(item_temp)
            update_main_inv(collection2, name, quantity)
        order_number = get_next_order_number(collection)
        location = input("Where is this sale shipping to? ")
        document = {
            'dateOrderPlaced': order_time,
            'items': items,
            'shippingAddress': location,
            'orderNumber': order_number,
            'totalPrice': total_price
        }
        collection.insert_one(document)
        print("Document created successfully.")
        print(f"Your Order Number is {order_number}")

    except ValueError as err:
        print(f"Error: {err}")


def update_shipping_location(collection):
    try:
        order_num = int(input("Please enter your order number: "))
        new_address = input("Please enter new shipping address: ")

        search = {"orderNumber": order_num}
        order = collection.find_one(search)
        if order:
            collection.update_one(search,
                                  {"$set": {"shippingAddress": new_address}})
            print(
                f"Shipping address for order {order_num} updated successfully.")
        else:
            print("No Order found with order number.")
    except ValueError as err:
        print(f"Error: {err}")


def update_item(collection):
    try:
        order_num = int(input("Please enter your order number: "))

        search1 = {"orderNumber": order_num}
        check1 = collection.find_one(search1)
        if check1:
            old_name = input("Please enter the name of the item to change: ")
            search = {"orderNumber": order_num, "items.name": old_name}
            order = collection.find_one(search)

            if order:
                new_item = input("Please enter name of new item: ")
                new_price = float(input("What is the price of the new item: "))
                new_quantity = int(input("How many of the new items: "))

                item_index = next(
                    (index for (
                        index,
                        item) in enumerate(
                        order['items']) if item['name'] == old_name),
                    None)
                # help from online resources^
                if item_index is not None:
                    update_document = {
                        "$set": {
                            f"items.{item_index}.name": new_item,
                            f"items.{item_index}.pricePaid": new_price,
                            f"items.{item_index}.quantity": new_quantity
                        }
                    }
                    collection.update_one(search1, update_document)
                    updated_order = collection.find_one(search1)
                    new_total_price = 0
                    for item in updated_order['items']:
                        new_total_price += (item['pricePaid']
                                            * item['quantity'])
                    collection.update_one(
                        search1, {
                            "$set": {
                                "totalPrice": new_total_price}})
                    print("Item successfully updated")
            else:
                print("Item not found in order number")
        else:
            print("No order found with given order number")
    except ValueError as err:
        print(f"Error: {err}")


def update_date_and_time(collection):
    try:
        order_num = int(input("Please enter your order number: "))

        search = {"orderNumber": order_num}
        order = collection.find_one(search)

        if order:
            current_time = datetime.now()
            new_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

            collection.update_one({"orderNumber": order_num}, {
                                  "$set": {"dateOrderPlaced": new_time}})
            print("Date and Time updated to current date and time")
        else:
            print("No order found with given order number")
    except ValueError as err:
        print(f"Error: {err}")


def look_up(collection):
    order_num = int(input("Please enter your order number: "))
    search = {"orderNumber": order_num}
    order = collection.find_one(search)
    if order:
        print("Order Details:")
        print(f"Order Number: {order['orderNumber']}")
        print(f"Shipping Address: {order['shippingAddress']}")
        print(f"Order Date: {order['dateOrderPlaced']}")
        print("Items: ")
        for item in order['items']:
            print(f"Name: {item['name']}")
            print(f"Price: {item['pricePaid']}")
            print(f"Quantity: {item['quantity']}")
        print(f"Total Price: {order['totalPrice']}")
    else:
        print("No order found with given order number")


def delete_by_order_num(collection):
    try:
        order_num = int(input("Please enter your order number: "))
        search = {"orderNumber": order_num}
        order = collection.find_one(search)
        if order:
            option = input("Are you sure you want to delete this order? y|n :")
            if option.lower() == "y":
                collection.delete_one(search)
                print("Record Deleted")
            else:
                print("Record Not Deleted")
        else:
            print("No record found with given order number")
    except ValueError as err:
        print(f"Error: {err}")


def update_main_inv(collection, item_name, count):
    search = {"item": item_name}
    in_stock = collection.find_one(search)
    # get the amount linked with item name then add count and update db
    if in_stock:
        item_count = in_stock.get("quantity")
        new_count = item_count + count

        collection.update_one(search, {"$set": {"quantity": new_count}})


def check_main_inv(collection2, item_name) -> int:
    search = {"item": item_name}
    in_stock = collection2.find_one(search)
    if in_stock:
        item_count = in_stock.get("quantity", 0)
        return item_count
    return 0


def test_push(collection):
    current_datetime = datetime.now()
    order_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    location = "Denver"
    how_many = 1
    items = []
    for i in range(how_many):
        name = "Pen"
        price_paid = 2
        quantity = 10
        # item_temp = saleItem(name, price_paid, quantity)
        item_temp = {
            'name': name,
            'pricePaid': price_paid,
            'quantity': quantity
        }
        items.append(item_temp)
    order_number = 1
    total_price = 10000
    document = {
        'orderDate': order_time,
        'items': items,
        'shippingAddress': location,
        'orderNumber': order_number,
        'totalPrice': total_price
    }
    collection.insert_one(document)
    print("Document created successfully.")
    print(f"Your Order Number is {order_number}")
