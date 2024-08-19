import tkinter as tk
from tkinter import messagebox
import sqlite3

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("350x450")

        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=35, height=10, font=('Arial', 12), bd=0, fg='#464646', selectbackground='#a6a6a6', activestyle="none")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.task_entry = tk.Entry(self.root, font=('Arial', 12))
        self.task_entry.pack(pady=10)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.add_task_button = tk.Button(self.button_frame, text="Add Task", width=10, command=self.add_task)
        self.add_task_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", width=10, command=self.delete_task)
        self.delete_task_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.mark_done_button = tk.Button(self.button_frame, text="Mark Done", width=10, command=self.mark_task_done)
        self.mark_done_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.populate_tasks()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                task TEXT NOT NULL,
                priority TEXT NOT NULL,
                done BOOLEAN NOT NULL
            )
            """)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task != "":
            with self.conn:
                self.conn.execute("INSERT INTO tasks (task, priority, done) VALUES (?, ?, ?)", (task, priority, False))
            self.populate_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task_id = self.get_task_id(selected_task_index)
            with self.conn:
                self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.populate_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def mark_task_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task_id = self.get_task_id(selected_task_index)
            with self.conn:
                self.conn.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
            self.populate_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def get_task_id(self, index):
        task_tuple = self.conn.execute("SELECT id FROM tasks ORDER BY priority ASC LIMIT 1 OFFSET ?", (index,)).fetchone()
        return task_tuple[0] if task_tuple else None

    def get_display_text(self, task):
        status = "Done" if task[3] else "Not Done"
        return f"{task[1]} - {task[2]} - {status}"

    def populate_tasks(self):
        self.task_listbox.delete(0, tk.END)
        cursor = self.conn.execute("SELECT * FROM tasks ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END")
        for task in cursor:
            self.task_listbox.insert(tk.END, self.get_display_text(task))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
