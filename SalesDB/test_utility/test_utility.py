import unittest
from datetime import datetime
from pymongo import MongoClient
from unittest.mock import patch, Mock
from utility import utilityInventory
from utility import utilitySales

class TestDB(unittest.TestCase):
    def setUp(self) -> None:
        """Setup
        """
        path_to_certificate = 'SalesDB/X509-cert-1147331512641107939.pem'
        uri = 'mongodb+srv://cluster0.j1hw0tj.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority'

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCertificateKeyFile=path_to_certificate
        )

    def tearDown(self) -> None:
        """Teardown
        """
        # Add any cleanup code if needed

    @patch('your_module_name.datetime')
    def test_new_shipment(self, mock_datetime):
        # Mocking the current datetime to ensure consistent results
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)

        # Mocking user input
        user_inputs = [
            "Location1", "Supplier1", "2", "Item1", "10", "5.0", "Y", "2", "Tag1", "Tag2", "Item2", "8", "7.0", "N"
        ]

        with patch('builtins.input', side_effect=user_inputs):
            # Mocking database collections
            mock_ship_collection = Mock()
            mock_inv_collection = Mock()

            # Call the function to test
            utilityInventory.newShipment(mock_ship_collection, mock_inv_collection)

            # Assertions
            mock_ship_collection.insert_one.assert_called_once()
            mock_inv_collection.update_one.assert_called_once()

    # Add similar test cases for other functions
    # ...


if __name__ == '__main__':
    unittest.main()
