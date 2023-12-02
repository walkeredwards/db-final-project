from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure

path_to_certificate = '/home/hectorramirez/gitHub/X509- \
cert-1147331512641107939.pem'
uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource \
=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=   \
majority'
client = MongoClient(
    uri,
    tls=True,
    tlsCertificateKeyFile=path_to_certificate,
    server_api=ServerApi("1"))

