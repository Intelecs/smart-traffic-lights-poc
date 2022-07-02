import unittest
from storage.Database import Database


class TestDatabase(unittest.TestCase):

    database = None

    @classmethod
    def setUpClass(cls):
        cls.database = Database()
        cls.database.run()

    def test_database_connected(self):
        self.assertTrue(self.database.is_connected)

    # def test_database_disconnected(self):
    #     self.database.__disconnect__()
    #     self.assertFalse(self.database.is_connected)

    def test_database_insert(self):
        violation = {
            "car_plate_number": "ABV",
            "captured_image": "test.jpg",
        }
        self.assertTrue(self.database.add_violation(violation))

    # def test_database_get_violations(self):
    #     violations = self.database.get_violations()
    #     self.assertTrue(len(violations) > 0)

    # def test_violation_query(self):
    #     self.assertTrue(isinstance(self.database.query_violation(id= 1), dict))

    def test_violation_delete(self):
        self.assertTrue(self.database.delete_violation(id=1))

    # def test_database_delete_violations(self):
    #     self.assertTrue(self.database.delete_all_records())
    @classmethod
    def tearDownClass(cls):
        cls.database.__disconnect__()
