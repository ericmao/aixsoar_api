import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # Events Endpoints Tests
    def test_receive_event(self):
        response = self.app.post('/events', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'}, 
                                 json={"event_id": "12345", "timestamp": "2024-06-01T12:00:00Z",
                                       "host": "host123", "type": "malware_detection",
                                       "details": {"filename": "malicious.exe", "filepath": "/path/to/malicious.exe", "severity": "high"}})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Event received')

    def test_get_event(self):
        response = self.app.get('/events/12345', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['event_id'], '12345')

    def test_delete_event(self):
        response = self.app.delete('/events/12345', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Event deleted')

    # Samples Endpoints Tests
    def test_create_sample_request(self):
        response = self.app.post('/samples', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'},
                                 json={"sample_id": "67890", "host": "host123", "timestamp": "2024-06-01T12:00:00Z", "filepath": "/path/to/sample"})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Sample request received')

    def test_get_sample(self):
        response = self.app.get('/samples/67890', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['sample_id'], '67890')

    # Status Endpoints Tests
    def test_receive_status(self):
        response = self.app.post('/status', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'},
                                 json={"host": "host123", "timestamp": "2024-06-01T12:00:00Z", "status": "healthy"})
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Status received')

    def test_get_status(self):
        response = self.app.get('/status', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('host123', data)

if __name__ == '__main__':
    unittest.main()
