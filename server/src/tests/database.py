import unittest
from modules.DatabaseModel.database_model import *
from sqlalchemy.orm import Session
from modules.Database.database import Database
import os
import sys

class DatabaseTestCase(unittest.TestCase):
    db = None
    engine = None
    
    @classmethod
    def setUpClass(cls):
        if os.path.exists("test.db"):
            os.remove("test.db")
        if not os.path.exists("test.db"):
            open("test.db", 'w').close()
        # Create a new test database
        DatabaseTestCase.db = Database("test.db")
        DatabaseTestCase.engine = DatabaseTestCase.db.engine()
        
    @classmethod
    def tearDownClass(cls):
        # Drop the test database
        del DatabaseTestCase.db
        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_connect(self):
        # Test the database connection
        with Session(DatabaseTestCase.engine) as session:
            pass
        

    def test_insert(self):
        # Test inserting data into the table
        device = Aggregator()
        self.db.insert("test_table", data)
        rows = self.db.select("test_table", ["id", "name", "age"])
        self.assertEqual(len(rows), 1)
        self.db.delete("test_table", data)

if __name__ == '__main__':
    unittest.main()