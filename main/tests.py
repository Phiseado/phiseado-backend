from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.
class TestCheckingMessage(APITestCase):

    def test_check_phishing_message(self):
        url = "/check"
        data = {'message': 'Este es el mensaje que he recibido https://testsafebrowsing.appspot.com/s/phishing.html'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])

    def test_check_not_phishing_message(self):
        url = "/check"
        data = {'message': 'Este es el mensaje que he recibido https://google.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["result"])

    def test_check_message_without_url(self):
        url = "/check"
        data = {'message': 'Este es el mensaje que he recibido sin URL'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)