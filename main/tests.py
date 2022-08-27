from rest_framework.test import APITestCase

# Create your tests here.
class TestCheckingMessage(APITestCase):
    def test_check_phishing_message(self):
        url = "/check/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])

    def test_check_not_phishing_message(self):
        url = "/check/"
        data = {'message': 'Hello https://google.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["result"])

    def test_check_message_without_url(self):
        url = "/check/"
        data = {'message': 'This is an incoming message without URL'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_check_message_without_message(self):
        url = "/check/"
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

class TestReportMessage(APITestCase):
    def test_report_message(self):
        url = "/report-message/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html', 
                'isoCode': 'es',
                'isPhishing': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])

    def test_set_message_as_non_phishing(self):
        url = "/report-message/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html', 
                'isoCode': 'es',
                'isPhishing': False}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])
    
    def test_report_message_without_message(self):
        url = "/report-message/"
        data = { 'isoCode': 'es', 'isPhishing': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_report_message_without_iso_code(self):
        url = "/report-message/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html', 
                'isPhishing': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_report_message_without_is_phishing(self):
        url = "/report-message/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html', 
                'isoCode': 'es'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_report_message_with_invalid_country_code(self):
        url = "/report-message/"
        data = {'message': 'This is an incoming message https://testsafebrowsing.appspot.com/s/phishing.html', 
                'isoCode': 'esssssss',
                'isPhishing': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

class TestDomains(APITestCase):
    def test_get_domains(self):
        url = "/domains/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
class TestBarChart(APITestCase):
    def test_get_bar_chart(self):
        url = "/bar-chart/"
        data = {'filter': 'Este mes', }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('chart' in response.json())
    
    def test_get_bar_chart_without_filter(self):
        url = "/bar-chart/"
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_bar_chart_with_invalid_filter(self):
        url = "/bar-chart/"
        data = {'filter':'hoyyyy'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

class TestPieChart(APITestCase):
    def test_get_pie_chart(self):
        url = "/pie-chart/"        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('phishing' in response.json())
        self.assertTrue('non_phishing' in response.json())
