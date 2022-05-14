import unittest
from device.MQTTclient import MQTTclient


class TestDeviceClient(unittest.TestCase):

    device = None

    @classmethod
    def setUpClass(cls):
        cls.device = MQTTclient(
            host="axwsbhnc43ml1-ats.iot.eu-west-1.amazonaws.com",
            root_ca_path="greengrass/greengrass-v2-certs/AmazonRootCA1.pem",
            private_key_path="greengrass/greengrass-v2-certs/JunctionNodeA/7be9635fcee9f1b70a0f2f0e33f2468703e849d8388d73cce9d1c29b5fa77124-private.pem.key",
            certificate_path="greengrass/greengrass-v2-certs/JunctionNodeA/7be9635fcee9f1b70a0f2f0e33f2468703e849d8388d73cce9d1c29b5fa77124-certificate.pem.crt",
        )
        cls.device.__setup__()
    
    def test_device_client_online(self):
        self.assertTrue(self.device.is_connected)
    
    def test_device_client_subscribe(self):
        self.device.topics = ["test/topic"]
        self.assertTrue(self.device.__subscribe__())
    
    def test_device_client_publish(self):
        self.assertTrue(self.device.__publish__("test/topic", {"test": "test"}))

    @classmethod
    def tearDownClass(cls):
        cls.device.__disconnect__()

    