from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure
import pymongo
path_to_certificate = '/home/hectorramirez/gitHub/X509-cert-1147331512641107939.pem'
uri = "mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=path_to_certificate,
                     server_api=ServerApi('1'))

"""
Create database called myDatabase
    db = client.myDatabase
create a collection named 'recipes'
collection is equivalent to table
    my_collection = db.recipes
"""
# connects to database
db = client['testDB']
# selects a table == collection
collection = db['testCol']
# creates variable doc count and assignes it a value returned by the
# fuction count documents
doc_count = collection.count_documents({})
# prints
print(doc_count)  # Should print 0 as the testDB doesn't exist

# let's connect to sample_mflix database
# this database is generated when you load sample data
db = client['sample_mflix']
# selects table movies
collection = db['movies']
doc_count = collection.count_documents({})
print(doc_count)

#Beautify output using pip rich