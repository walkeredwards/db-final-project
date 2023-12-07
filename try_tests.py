from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.errors import OperationFailure
# from datetime import datetime, timedelta
# import random
# from datetime import datetime

path_to_certificate = '/home/hectorramirez/gitHub/X509-\
cert-1147331512641107939.pem'
# path_to_certificate ='/Users/walkeredwards/CSCI/CS\
# CI_260/X509-cert-1147331512641107939.pem'
uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource\
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=\
majority'
# uri = ''
client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))

# let's connect to sample_supplies database
db = client["sample_supplies"]
# selects table movies
collection = db["shipment"]
collectionInv = db["inventory"]
doc_count = collection.count_documents({})
print(doc_count)


# This seccion of code reads all of the items created in shipmemt and pushes them into inventory
# def get_item_totals():
#     # Aggregate to get total quantity for each item
#     pipeline = [
#         {
#             "$unwind": "$Items"
#         },
#         {
#             "$group": {
#                 "_id": "$Items.name",
#                 "total_quantity": {"$sum": "$Items.quantity"}
#             }
#         }
#     ]

#     # Execute the aggregation pipeline
#     result = list(collection.aggregate(pipeline))
#     return result

# # Example usage
# totals = get_item_totals()
# for item in totals:
#     print(f"Item: {item['_id']}, Total Quantity: {item['total_quantity']}")
#     collectionInv.update_one(
#                     {"item": item['_id']},
#                     {
#                         '$set': {
#                             "item": item['_id'],
#                             "quantity": item['total_quantity']
#                         }
#                     },
#                     upsert=True
#                 )


# This seccion of code populates shipment with  random documents
# # Function to generate a random date
# def random_date(start_date, end_date):
#     return start_date + timedelta(
#         seconds=random.randint(0, int((end_date - start_date).total_seconds()))
#     )

# # Function to generate a random shipment item
# def generate_shipment_item():
#     item_name = random.choice(["book", "pens", "Pens", "Notebooks", "Stapler", "Desk Organizer",
#                                "Sticky Notes", "Paper Clips", "Whiteboard Markers", "Calculator",
#                                "File Folders", "Desk Lamp", "Mouse Pad", "Letter Opener", "Envelopes",
#                                "Highlighters", "USB Flash Drive", "Desk Chair", "Desk Calendar", "Scissors",
#                                "Tape Dispenser", "Laptop Stand"])

#     item_tags = random.sample(["writing", "paperwork", "organization", "stationery", "desktop essentials", "note-taking",
#                                "office supplies", "document management", "desk accessories", "office tools", "creative tools",
#                                "workplace efficiency", "corporate essentials", "meeting essentials", "professional tools"],
#                               k=random.randint(1, 3))

#     return {
#         "name": item_name,
#         "tags": item_tags,
#         "pricePaid": round(random.uniform(10.0, 200.0), 2),
#         "quantity": random.randint(1, 150),
#     }

# # Function to select a random supplier
# def get_random_supplier():
#     suppliers = ["Staples", "Office Depot", "Amazon Business", "W.B. Mason", "Quill"]
#     return random.choice(suppliers)

# # Generate 15 shipments
# shipments = []
# for _ in range(15):
#     shipment_date = random_date(datetime(2020, 1, 1), datetime(2023, 12, 31))
#     shipment_items = [generate_shipment_item() for _ in range(random.randint(1, 3))]
#     shipment = {
#         "arrivalDate": shipment_date.isoformat(),
#         "Items": shipment_items,
#         "storageLocation": 'Denver',
#         "supplier": get_random_supplier(),
#     }
#     shipments.append(shipment)

# # Insert shipments into MongoDB
# collection.insert_many(shipments)

# print("Data inserted successfully.")

# old coduments
# Print the updated document
updated_document = collection.find_one({})
print(updated_document)

# selects table movies
collection = db["sales"]
doc_count = collection.count_documents({})
print(doc_count)

# Print the updated document
updated_document = collection.find_one({})
print(updated_document)


# Beautify output using pip rich
