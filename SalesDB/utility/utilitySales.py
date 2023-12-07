"""All the functions for the sale/shipping
side of the database
"""
from datetime import datetime
from rich import Console


def get_next_order_number(collection) -> None:
    """Checks the data base for the highest order number and adds 1 to it
    If no order number start at 1

    Args:
        collection: sales db collection
    """
    result = collection.find_one(
        sort=[("orderNumber", -1)], projection={"orderNumber": 1})
    # help from online resources
    return (result["orderNumber"] + 1) if result else 1


def new_sale(collection, collection2) -> None:
    """Creates New sale. Checks for inventory. removes from inventory
    and inserts sale.

    Args:
        collection: sales db collection
        collection2: inventory db
    """
    try:
        order_success = True
        current_datetime = datetime.now()
        order_time = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        how_many = int(
            input("How many items are being shipped in this shipment? "))
        items = []
        total_price = 0
        for _ in range(how_many):
            name = input("Whats the name of the item: ")
            price_paid = float(input("How much is the item: "))
            quantity = int(input("How many of these items were bought: "))

            inventory_count = check_main_inv(collection2, name)
            if inventory_count < quantity:
                print(f"Sorry we only have {inventory_count}, of {name}")
                order_success = False
                return
            total_price += price_paid * quantity
            item_temp = {
                'name': name,
                'pricePaid': price_paid,
                'quantity': quantity
            }
            items.append(item_temp)

        if order_success:
            for item in items:
                take_inv(collection2, item['name'], item['quantity'])
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


def update_shipping_location(collection) -> None:
    """Updates shipping location given order number

    Args:
        collection: sales db collection
    """
    try:
        order_num = int(input("Please enter your order number: "))
        new_address = input("Please enter new shipping address: ")

        search = {"orderNumber": order_num}
        order = collection.find_one(search)
        if order:
            collection.update_one(search,
                                  {"$set": {"shippingAddress": new_address}})
            print(f"Shipping address for order "
                  f"{order_num} updated successfully.")
        else:
            print("No Order found with order number.")
    except ValueError as err:
        print(f"Error: {err}")


def update_item(collection, collection2) -> None:
    """Updates an item. checks inventory for new item. Gains changed inventory.
    Deletes new item inventory

    Args:
        collection: sales db
        collection2: inventory db
    """
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
                    current_count = check_main_inv(collection2, new_item)

                    if current_count > new_quantity:
                        update_main_inv(
                            collection2, old_name,
                            order['items'][item_index]['quantity'])
                        take_inv(collection2, new_item, new_quantity)
                    else:
                        print("Out of stock of requested item")
                        return
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


def update_date_and_time(collection) -> None:
    """Updates date and time given order number
    Args:
        collection: sales db collection
    """
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


def look_up(collection) -> None:
    """Looks up and prints order given order number

    Args:
        collection: sales db collection
    """
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


def delete_by_order_num(collection, collection2) -> None:
    """deletes order by order number and adds product back to inventory

    Args:
        collection: sales db collection
        collection2: inventory db collection
    """
    try:
        order_num = int(input("Please enter your order number: "))
        search = {"orderNumber": order_num}
        order = collection.find_one(search)
        if order:
            option = input("Are you sure you want to delete this order? y|n :")
            if option.lower() == "y":
                for item in order['items']:
                    update_main_inv(
                        collection2, item['name'], item['quantity'])
                collection.delete_one(search)
                print("Record Deleted")
            else:
                print("Record Not Deleted")
        else:
            print("No record found with given order number")
    except ValueError as err:
        print(f"Error: {err}")


def update_main_inv(collection, item_name, count) -> None:
    """adds the new quantity to the old one and updates it

    Args:
        collection: sales db collection
        item_name: item to check for
        count: how many items there are
    """
    search = {"item": item_name}
    in_stock = collection.find_one(search)
    # get the amount linked with item name then add count and update db
    if in_stock:
        item_count = in_stock.get("quantity")
        new_count = item_count + count

        collection.update_one(search, {"$set": {"quantity": new_count}})


def take_inv(collection, item_name, count) -> None:
    """removes items from main inventory

    Args:
        collection: inventory db collection
        item_name: item in inventory
        count: how much of the item in inventory
    """
    search = {"item": item_name}
    in_stock = collection.find_one(search)
    # get the amount linked with item name then add count and update db
    if in_stock:
        item_count = in_stock.get("quantity")
        new_count = item_count - count

        collection.update_one(search, {"$set": {"quantity": new_count}})


def check_main_inv(collection2, item_name) -> int:
    """Checks the main invetory

    Args:
        collection2: inventory db collection
        item_name (_type_): name of item getting checked in inventory

    Returns:
        int: amount of given item
    """
    search = {"item": item_name}
    in_stock = collection2.find_one(search)
    if in_stock:
        item_count = in_stock.get("quantity", 0)
        return item_count
    return 0


def print_order(collection) -> None:
    """Prints order details

    Args:
        collection: sales db collection
    """
    try:
        order_num = int(input("Please enter your order number: "))
        search = {"orderNumber": order_num}
        order = collection.find_one(search)
        if order:
            console = Console()
            console.print("[bold]Order Details:[/bold]")
            console.print(f"[bold]Order Number:[/bold] {order['orderNumber']}")
            console.print(f"[bold]Shipping Address:[/bold] {order['shippingAddress']}")
            console.print(f"[bold]Order Date:[/bold] {order['dateOrderPlaced']}")
            
            console.print("[bold]Items: [/bold]")
            for item in order['items']:
                console.print(f"[bold]Item Name:[/bold] {item['name']}")
                console.print(f"[bold]Price:[/bold] [green]{item['pricePaid']}[/green]")
                console.print(f"[bold]Quantity:[/bold] [blue]{item['quantity']}[/blue]")
                console.print(f"[bold]Total Price:[/bold] [green]{item['totalPrice']}[/green]\n")
        else:
            console = Console()
            console.print("No shipments found.[/red]")
    except Exception as ex:
        console = Console()
        console.print(f"Error: {ex}")

