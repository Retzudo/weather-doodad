#!./env/bin/python3
import app
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_root(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_city(self):
        response = self.app.get('/wien/Wien+Innere+Stadt')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/salzburg/Lofer')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/kAeRnTeN/Millstatt')
        self.assertEqual(response.status_code, 200)

    def test_invalid(self):
        response = self.app.get('/nowhere/nowhere/')
        self.assertEqual(response.status_code, 404)
        response = self.app.get('/asdf')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
