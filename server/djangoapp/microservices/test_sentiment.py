import unittest
from app import app

class SentimentTests(unittest.TestCase):
    def test_classification(self):
        client=app.test_client()
        for text,expected in [('Fantastic services','positive'),('Horrible terrible service','negative'),('The car is blue','neutral')]:
            self.assertEqual(client.post('/analyze',json={'text':text}).json['sentiment'],expected)
        self.assertEqual(client.get('/analyze/Fantastic%20services').json['sentiment'],'positive')
    def test_bad_inputs(self):
        for data in [{},[],{'text':''},{'text':'x'*2001}]:
            self.assertEqual(app.test_client().post('/analyze',json=data).status_code,400)
        self.assertEqual(app.test_client().get('/health').status_code,200)
