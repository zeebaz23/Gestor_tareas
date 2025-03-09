import unittest
from database import create_connection
from auth import create_user, authenticate_user

class TestDeleteTask(unittest.TestCase):
    def setUp(self):
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM users')
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()
        create_user('testuser', 'password')

    def test_delete_task_normal(self):
        user = authenticate_user('testuser', 'password')
        self.cursor.execute('INSERT INTO tasks (user_id, text, created_at, category, status) VALUES (?, ?, datetime("now"), "General", "Por hacer")', (user[0], 'Comprar leche'))
        self.conn.commit()
        self.cursor.execute('DELETE FROM tasks WHERE user_id = ? AND text = ?', (user[0], 'Comprar leche'))
        self.conn.commit()
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user[0],))
        tasks = self.cursor.fetchall()
        self.assertEqual(len(tasks), 0)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()