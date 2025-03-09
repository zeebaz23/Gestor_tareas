import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from auth import create_user, authenticate_user
from database import create_connection

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Usuario").grid(row=0, column=0)
        tk.Label(self.root, text="Contraseña").grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.password_entry = tk.Entry(self.root, show="*")
        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Crear Cuenta", command=self.create_account_screen).grid(row=3, column=0, columnspan=2)

    def create_account_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Nuevo Usuario").grid(row=0, column=0)
        tk.Label(self.root, text="Nueva Contraseña").grid(row=1, column=0)
        self.new_username_entry = tk.Entry(self.root)
        self.new_password_entry = tk.Entry(self.root, show="*")
        self.new_username_entry.grid(row=0, column=1)
        self.new_password_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Crear Cuenta", command=self.create_account).grid(row=2, column=0, columnspan=2)
        tk.Button(self.root, text="Volver", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        if create_user(username, password):
            messagebox.showinfo("Éxito", "Cuenta creada exitosamente")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya existe")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = authenticate_user(username, password)
        if user:
            self.user_id = user[0]
            self.create_task_screen()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def create_task_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Texto de la Tarea").grid(row=0, column=0)
        self.task_text_entry = tk.Entry(self.root)
        self.task_text_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Categoría").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Estado").grid(row=2, column=0)
        self.status_combobox = ttk.Combobox(self.root, values=["Por hacer", "En progreso", "Completada"])
        self.status_combobox.grid(row=2, column=1)
        self.status_combobox.current(0)
        tk.Button(self.root, text="Crear Tarea", command=self.create_task).grid(row=3, column=0, columnspan=2)
        self.task_tree = ttk.Treeview(self.root, columns=("id", "text", "created_at", "category", "status"), show="headings")
        self.task_tree.heading("text", text="Texto de la Tarea")
        self.task_tree.heading("created_at", text="Fecha de Creación")
        self.task_tree.heading("category", text="Categoría")
        self.task_tree.heading("status", text="Estado")
        self.task_tree.grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Eliminar Tarea", command=self.delete_task).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Editar Tarea", command=self.edit_task_screen).grid(row=6, column=0, columnspan=2)
        self.load_tasks()

    def create_task(self):
        task_text = self.task_text_entry.get()
        category = self.category_entry.get()
        status = self.status_combobox.get()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user_id, text, created_at, category, status) VALUES (?, ?, ?, ?, ?)', (self.user_id, task_text, created_at, category, status))
        conn.commit()
        conn.close()
        self.load_tasks()

    def load_tasks(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, text, created_at, category, status FROM tasks WHERE user_id = ?', (self.user_id,))
        tasks = cursor.fetchall()
        for task in tasks:
            self.task_tree.insert("", "end", values=(task[0], task[1], task[2], task[3], task[4]), iid=str(task[0]))
        conn.close()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar una tarea para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar esta tarea?")
        if confirm:
            task_id = selected_item[0]
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.load_tasks()

    def edit_task_screen(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_id = int(selected_item[0])
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT text, category, status FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            conn.close()
            self.clear_screen()
            tk.Label(self.root, text="Texto de la Tarea").grid(row=0, column=0)
            self.task_text_entry = tk.Entry(self.root)
            self.task_text_entry.insert(0, task[0])
            self.task_text_entry.grid(row=0, column=1)
            tk.Label(self.root, text="Categor\u00eda").grid(row=1, column=0)
            self.category_entry = tk.Entry(self.root)
            self.category_entry.insert(0, task[1])
            self.category_entry.grid(row=1, column=1)
            tk.Label(self.root, text="Estado").grid(row=2, column=0)
            self.status_combobox = ttk.Combobox(self.root, values=["Por hacer", "En progreso", "Completada"])
            self.status_combobox.set(task[2])
            self.status_combobox.grid(row=2, column=1)
            tk.Button(self.root, text="Guardar Cambios", command=lambda: self.edit_task(task_id)).grid(row=3, column=0,
                                                                                                       columnspan=2)
            tk.Button(self.root, text="Volver", command=self.create_task_screen).grid(row=4, column=0, columnspan=2)

    def edit_task(self, task_id):
        task_text = self.task_text_entry.get()
        category = self.category_entry.get()
        status = self.status_combobox.get()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET text = ?, category = ?, status = ? WHERE id = ?',
                       (task_text, category, status, task_id))
        conn.commit()
        conn.close()
        self.create_task_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

