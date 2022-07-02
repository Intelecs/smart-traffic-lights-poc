import unittest
from device.BluetoothClient import BluetoothClient


class TestBluetoothClient(unittest.TestCase):

    bluetooth_client = None

    @classmethod
    def setUpClass(cls):
        cls.bluetooth_client = BluetoothClient()

    def test_bluetooth_client_mac_address(self):
        self.assertIsInstance(self.bluetooth_client.get_mac_address(), str)

    def test_near_by_devices(self):

        self.assertIsInstance(self.bluetooth_client.near_by_devices(), list)
