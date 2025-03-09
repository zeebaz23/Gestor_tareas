import unittest
from auth import create_user, authenticate_user
from database import create_connection

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM users')
        self.conn.commit()

    def test_create_user(self):
        result = create_user('testuser', 'password')
        self.assertTrue(result)

    def test_create_user_duplicate(self):
        create_user('testuser', 'password')
        result = create_user('testuser', 'password')
        self.assertFalse(result)

    def test_authenticate_user(self):
        create_user('testuser', 'password')
        user = authenticate_user('testuser', 'password')
        self.assertIsNotNone(user)

    def test_authenticate_user_invalid(self):
        create_user('testuser', 'password')
        user = authenticate_user('invaliduser', 'password')
        self.assertIsNone(user)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()