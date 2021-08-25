# Testing the app.py file
import unittest
from app import app


class ApiTest(unittest.TestCase):

    # check if responses is 200
    def test_user_register(self):
        test = app.test_client(self)
        response = test.get('/patient-registration/')
        status = response.status_code
        self.assertEqual(status, 404)

    # check if response is 200
    def test_user_id(self):
        test = app.test_client(self)
        response = test.get('/view-illness/3')
        status = response.status_code
        self.assertEqual(status, 200)

    # check if responses is 200
    def test_products(self):
        test = app.test_client(self)
        response = test.get('/view-appointment/')
        status = response.status_code
        self.assertEqual(status, 200)

    # check if responses is 200
    def test_product_id(self):
        test = app.test_client(self)
        response = test.get('/edit-patient/3/')
        status = response.status_code
        self.assertEqual(status, 404)

    # check content type
    def test_type(self):
        test = app.test_client(self)
        response = test.get('/view-patient/')
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()

