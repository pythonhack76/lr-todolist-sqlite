import tkinter as tk
from tkinter import messagebox
import json
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("300x400")

        self.tasks = []
        self.load_tasks()  # Carica le attività salvate

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=25, height=10, font=('Arial', 12), bd=0, fg='#464646', selectbackground='#a6a6a6', activestyle="none")
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.task_entry = tk.Entry(self.root, font=('Arial', 12))
        self.task_entry.pack(pady=20)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.add_task_button = tk.Button(self.button_frame, text="Add Task", width=10, command=self.add_task)
        self.add_task_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", width=10, command=self.delete_task)
        self.delete_task_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.mark_done_button = tk.Button(self.button_frame, text="Mark Done", width=10, command=self.mark_task_done)
        self.mark_done_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Aggiungi due pulsanti nel frame dei pulsanti:
        self.show_all_button = tk.Button(self.button_frame, text="Show All", width=10, command=lambda: self.populate_tasks())
        self.show_all_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        self.show_done_button = tk.Button(self.button_frame, text="Show Done", width=10, command=lambda: self.filter_tasks(True))
        self.show_done_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        self.show_not_done_button = tk.Button(self.button_frame, text="Show Not Done", width=10, command=lambda: self.filter_tasks(False))
        self.show_not_done_button.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.populate_tasks()  # Popola la Listbox con le attività

    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks.append({"task": task, "done": False})
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self.save_tasks()  # Salva le attività ogni volta che una viene aggiunta
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected_task_index)
            del self.tasks[selected_task_index]
            self.save_tasks()  # Salva le attività dopo l'eliminazione
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def mark_task_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            task["done"] = not task["done"]
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(selected_task_index, self.get_display_text(task))
            self.save_tasks()  # Salva le attività dopo la modifica dello stato
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task.")

    def get_display_text(self, task):
        return f"{task['task']} - {'Done' if task['done'] else 'Not Done'}"

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)

    def populate_tasks(self):
        for task in self.tasks:
            self.task_listbox.insert(tk.END, self.get_display_text(task))

    def filter_tasks(self, show_done):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task["done"] == show_done:
                self.task_listbox.insert(tk.END, self.get_display_text(task))
    
    
    
    


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
