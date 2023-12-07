from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
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
doc_count = collection.count_documents({})
print(doc_count)

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
