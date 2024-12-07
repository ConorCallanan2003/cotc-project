import unittest
import modules.Database.database
from sqlalchemy.orm import Session


class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a new test database
        cls.db = modules.Database.database.Database()
        cls.engine = cls.getDBEngine()

    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        cls.db.dbEngine.dispose()

    def test_connect(self):
        # Test the database connection
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM test_table")

    def test_insert(self):
        # Test inserting data into the table
        data = {"id": 1, "name": "John", "age": 30}
        self.db.insert("test_table", data)
        rows = self.db.select("test_table", ["id", "name", "age"])
        self.assertEqual(len(rows), 1)
        self.db.delete("test_table", data)

if __name__ == '__main__':
    unittest.main()