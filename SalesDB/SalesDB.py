import os
import time
from typing import Tuple
from utility import utility
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from pymongo.errors import OperationFailure

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

def read_documents():
    # Implement logic to read documents
    # Example:
    documents = collection.find()
    for doc in documents:
        print(doc)

def update_document():
    # Implement logic to update a document
    # Example:
    filter_criteria = {'storageLocation': 'Denver'}
    update_values = {'$set': {'supplier': 'Updated Supplier'}}
    collection.update_one(filter_criteria, update_values)
    print("Document updated successfully.")

def delete_document():
    # Implement logic to delete a document
    # Example:
    filter_criteria = {'storageLocation': 'Denver'}
    collection.delete_one(filter_criteria)
    print("Document deleted successfully.")
    
def show_menu() -> int:
    """Displays menu for working in wich table .
        Must be changed later"""
    text = """
    Welcome to Fencemart Database
    =============

    Are you working in Sales or Inventory?:
    1. Working in Sales
    2. Working in Inventory
    3. Exit
    
    #Maybe add a both option or get rid of this after and make specific options to change tables
    """
    print(text)
    option = input('Enter an option: [1-3]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 3:
                return opt
        os.system('clear')
        option = input("Enter a valid option: ")
        
def show_menu() -> int:
    """Displays menu.
        Must be changed later"""
    text = """
    A+ Grade Book
    =============

    Select one of the following menu options:
    1. Setup Database
    2. Add a new student
    3. Add new grades for a student
    4. Display student
    5. Update student information
    6. Update student grades
    7. Delete student
    8. Exit the program
    """
    print(text)
    option = input('Enter an option: [1-8]: ')
    while True:
        if option.isdecimal():
            opt = int(option)
            if 1 <= opt <= 8:
                return opt
        os.system('clear')
        option = input("Enter a valid option: ")


def main() -> None:
    """Main function.
    """
    # Connect to database
    db = client["sample_supplies"]
    while True:
        option = show_table_menu()
        if option == 8:
            exit(0)
        elif option == 1:
            setup_database(db_file)
        elif option == 2:
            add_student(db_file)
        elif option == 3:
            add_grades(db_file)
        elif option == 4:
            read_student(db_file)
        elif option == 5:
            update_student(db_file)
        elif option == 6:
            update_grades(db_file)
        elif option == 7:
            delete_student(db_file)


if __name__ == "__main__":
    main()
