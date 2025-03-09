import unittest
from database import create_connection
from auth import create_user, authenticate_user

class TestEditTask(unittest.TestCase):
    def setUp(self):
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM users')
        self.cursor.execute('DELETE FROM tasks')
        self.conn.commit()
        create_user('testuser', 'password')

    def test_edit_task_normal(self):
        user = authenticate_user('testuser', 'password')
        self.cursor.execute('INSERT INTO tasks (user_id, text, created_at, category, status) VALUES (?, ?, datetime("now"), "General", "Por hacer")', (user[0], 'Comprar leche'))
        self.conn.commit()
        self.cursor.execute('UPDATE tasks SET text = ?, category = ?, status = ? WHERE id = ?', ('Comprar leche y pan', 'Compras', 'En progreso', user[0]))
        self.conn.commit()
        self.cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user[0],))
        tasks = self.cursor.fetchall()
        self.assertEqual(tasks[0][2], 'Comprar leche y pan')
        self.assertEqual(tasks[0][4], 'Compras')
        self.assertEqual(tasks[0][5], 'En progreso')

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()