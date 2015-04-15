#!./env/bin/python3
import app
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_root(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_city(self):
        response = self.app.get('/wien/Wien+Innere+Stadt')
        assert response.status_code == 200
        response = self.app.get('/salzburg/Lofer')
        assert response.status_code == 200
        response = self.app.get('/kAeRnTeN/Millstatt')
        assert response.status_code == 200

    def test_invalid(self):
        response = self.app.get('/nowhere/nowhere/')
        assert response.status_code == 404
        response = self.app.get('/asdf')
        assert response.status_code == 404


if __name__ == '__main__':
    unittest.main()
