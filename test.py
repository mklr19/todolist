import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import csv
import tkinter.font as tkFont  # Importieren des tkFont Moduls

class Task:
    def __init__(self, name, priority='medium', status='unfinished', category='General'):
        self.name = name
        self.priority = priority  # neu
        self.status = status
        self.category = category

    def set_priority(self, priority):  # neu
        self.priority = priority
    
    def mark_as_done(self):
        self.status = 'finished'


def priority_ranking(priority):  # neu
    ranks = {'high': 3, 'medium': 2, 'low': 1}
    return ranks.get(priority, 0)


class TaskManager:

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]
        self.save_tasks()

    def mark_task_as_done(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_done()
                self.save_tasks()


    def save_tasks(self):
        with open('tasks.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for task in self.tasks:
                writer.writerow([task.name, task.priority, task.status, task.category])  # Kategorie hinzufügen


    def load_tasks(self):
        try:
            with open('tasks.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                try:
                    self.tasks = [Task(row[0], row[1], row[2], row[3]) for row in reader]
                except IndexError:
                    print("Fehler: Die CSV-Datei hat nicht die erwartete Struktur.")
                    self.tasks = []
        except FileNotFoundError:
            pass


class TaskManagerApp:
    def __init__(self):
        self.task_manager = TaskManager()
        self.root = tk.Tk()
        self.root.title("To-Do-Maker")
        self.search_button = tk.Button(self.root, text='Search in Tasks', command=self.search_tasks)
        self.search_button.pack(fill=tk.X)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(fill=tk.X) 
        self.search_category_button = tk.Button(self.root, text='Search in Categories', command=self.search_in_categories)
        self.search_category_button.pack(fill=tk.X)
        self.search_category_entry = tk.Entry(self.root)
        self.search_category_entry.pack(fill=tk.X)
        self.tasks_treeview = ttk.Treeview(self.root, columns=("Task", "Priority", "Status", "Category"))
        self.tasks_treeview.heading("#1", text="Task")
        self.tasks_treeview.heading("#2", text="Priority")
        self.tasks_treeview.heading("#3", text="Status")
        self.tasks_treeview.heading("#4", text="Category")  # Neue Kategorie-Spalte
        self.tasks_treeview.pack()
        self.add_task_button = tk.Button(self.root, text='Add task', command=self.add_task)
        self.add_task_button.pack()
        self.delete_task_button = tk.Button(self.root, text='Delete task', command=self.delete_task)
        self.delete_task_button.pack()
        self.delete_category_button = tk.Button(self.root, text='Delete category', command=self.delete_category)
        self.delete_category_button.pack(fill=tk.X)
        self.mark_task_as_done_button = tk.Button(self.root, text='Mark task as done', command=self.mark_task_as_done)
        self.unfinish_task_button = tk.Button(self.root, text='Mark task as undone', command=self.unfinish_task)
        self.change_task_priority_button = tk.Button(self.root, text='Change task priority', command=self.change_task_priority)  # neu
        self.tasks_treeview.tag_configure('finished', background='#00FF00')  # Helles Grün
        self.tasks_treeview.tag_configure('unfinished', background='#FF6666')  # Helles Rot
        self.tasks_treeview.pack(fill=tk.BOTH, expand=True)
        self.add_task_button.pack(fill=tk.X)
        self.delete_task_button.pack(fill=tk.X)
        self.mark_task_as_done_button.pack(fill=tk.X)
        self.unfinish_task_button.pack(fill=tk.X)
        self.change_task_priority_button.pack(fill=tk.X)
        self.change_task_name_button = tk.Button(self.root, text='Change task name', command=self.change_task_name)
        self.change_task_name_button.pack(fill=tk.X)
        self.change_category_button = tk.Button(self.root, text='Change category', command=self.change_category)
        self.change_category_button.pack(fill=tk.X)
        
        
        
        

    def add_task(self):
        task_name = simpledialog.askstring('Add task', 'Task name:')
        task_priority = simpledialog.askstring('Add task', 'Task priority (high, medium, low):')
        task_category = simpledialog.askstring('Add task', 'Task category:')  # Kategorie hinzufügen
        if task_name and task_priority and task_category:
            self.task_manager.add_task(Task(task_name, task_priority, 'unfinished', task_category))  # Kategorie hinzufügen
            self.refresh_tasks_treeview()

    def change_task_priority(self):  # neu
        selected_task_id = self.tasks_treeview.selection()[0]  # aktualisiert
        if selected_task_id:
            task_name = self.tasks_treeview.item(selected_task_id)["values"][0]  # aktualisiert
            new_priority = simpledialog.askstring('Change priority', 'New priority (high, medium, low):')
            if new_priority:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.set_priority(new_priority)
                self.refresh_tasks_treeview()  # aktualisiert

    def delete_task(self):
        selected_task = self.tasks_treeview.selection()[0]  # aktualisiert
        if selected_task:
            task_name = self.tasks_treeview.item(selected_task)["values"][0]
            self.task_manager.delete_task(task_name)
            self.refresh_tasks_treeview()  # Methode aktualisiert

    def mark_task_as_done(self):
        selected_task = self.tasks_treeview.selection()[0]
        if selected_task:
            task_name = self.tasks_treeview.item(selected_task)["values"][0]
            self.task_manager.mark_task_as_done(task_name)
            self.refresh_tasks_treeview()  # Methode aktualisiert


    def refresh_tasks_treeview(self):  # Methode umbenannt
        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)
        for task in self.task_manager.tasks:
            tag = 'finished' if task.status == 'finished' else 'unfinished'
            self.tasks_treeview.insert("", tk.END, values=(task.name, task.priority, task.status, task.category), tags=(tag,))  # Kategorie hinzufügen
            
    def run(self):
        self.tasks_treeview.heading("#1", text="Task", command=lambda: self.sort_by_task(self.tasks_treeview, "#1", False))
        self.tasks_treeview.heading("#2", text="Priority", command=lambda: self.sort_by_priority(self.tasks_treeview, "#2", False))
        self.tasks_treeview.heading("#3", text="Status", command=lambda: self.sort_by_status(self.tasks_treeview, "#3", False))
        self.tasks_treeview.heading("#4", text="Category", command=lambda: self.sort_by_category(self.tasks_treeview, "#4", False))

        self.refresh_tasks_treeview()  # aktualisiert
        self.root.mainloop()
        
    def sort_by_task(self, tv, col, reverse):
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)

        # Reverse sort next time
        tv.heading(col, command=lambda: self.sort_by_task(tv, col, not reverse))
        
    def sort_by_priority(self, tv, col, reverse):
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        # Verwenden der priority_map um die Prioritäten in sortierbare Zahlen umzuwandeln, 
        # mit einem Standardwert für ungültige oder unbekannte Prioritäten
        task_list.sort(key=lambda x: priority_map.get(x[0].lower(), 0), reverse=reverse)
    
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)
    
        # Reverse sort next time
        tv.heading(col, command=lambda: self.sort_by_priority(tv, col, not reverse))
        
    def sort_by_status(self, tv, col, reverse):
        status_map = {'finished': 1, 'unfinished': 0}
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(key=lambda x: status_map.get(x[0].lower(), 0), reverse=reverse)
    
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)
    
        # Reverse sort next time
        tv.heading(col, command=lambda: self.sort_by_status(tv, col, not reverse))
        
    def change_task_name(self):
        selected_task_id = self.tasks_treeview.selection()[0]
        if selected_task_id:
            task_name = self.tasks_treeview.item(selected_task_id)["values"][0]
            new_name = simpledialog.askstring('Change task name', 'New task name:')
            if new_name:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.name = new_name
                self.refresh_tasks_treeview()
                self.task_manager.save_tasks()
                
    def sort_by_category(self, tv, col, reverse):
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(reverse=reverse)
    
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)
    
        # Reverse sort next time
        tv.heading(col, command=lambda: self.sort_by_category(tv, col, not reverse))
                
    def unfinish_task(self):
        selected_task_id = self.tasks_treeview.selection()[0]
        if selected_task_id:
            task_name = self.tasks_treeview.item(selected_task_id)["values"][0]
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.status = 'unfinished'
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()
            
    def delete_category(self):
        selected_task_id = self.tasks_treeview.selection()[0]
        if selected_task_id:
            task_name = self.tasks_treeview.item(selected_task_id)["values"][0]
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.category = "Default"  # Setzt die Kategorie auf Default
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()

            
    def search_tasks(self):
        search_query = self.search_entry.get().lower()
        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)
        for task in self.task_manager.tasks:
            if search_query in task.name.lower():
                tag = 'finished' if task.status == 'finished' else 'unfinished'
                self.tasks_treeview.insert("", tk.END, values=(task.name, task.priority, task.status, task.category), tags=(tag,))
                
    def change_category(self):
        selected_task_id = self.tasks_treeview.selection()[0]
        if selected_task_id:
            task_name = self.tasks_treeview.item(selected_task_id)["values"][0]
            new_category = simpledialog.askstring('Change category', 'New category name:')
            if new_category:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.category = new_category
                self.refresh_tasks_treeview()
                self.task_manager.save_tasks()

    def search_in_categories(self):
        search_query = self.search_category_entry.get().lower()
        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)
        for task in self.task_manager.tasks:
            if search_query in task.category.lower():
                tag = 'finished' if task.status == 'finished' else 'unfinished'
                self.tasks_treeview.insert("", tk.END, values=(task.name, task.priority, task.status, task.category), tags=(tag,))
            







def register():
  username = entry_username.get()
  password = entry_password.get()
  if username and password:
    with open("credentials.txt", "a") as file:  # Änderung hier: "w" zu "a"
      file.write(f"{username}:{password}\n"
                 )  # Änderung hier: Trennzeichen hinzugefügt
    messagebox.showinfo("Erfolg", "Registrierung erfolgreich!")
  else:
    messagebox.showerror("Fehler",
                         "Benutzername und Passwort dürfen nicht leer sein.")


def check_credentials():
  username = entry_username.get()
  password = entry_password.get()
  try:
    with open("credentials.txt", "r") as file:
      credentials = file.readlines()
    for credential in credentials:
      stored_username, stored_password = credential.strip().split(
          ':')  # Änderung hier: Trennzeichen hinzugefügt
      if username == stored_username and password == stored_password:
        label_username.grid_forget()
        entry_username.grid_forget()
        label_password.grid_forget()
        entry_password.grid_forget()
        button_login.grid_forget()
        button_register.grid_forget()
        #label_success = tk.Label(window, text="Test")
        #label_success.grid(row=0, column=0, columnspan=2, pady=10)
        window.destroy()  # Schließt das Login-Fenster
        app = TaskManagerApp()
        app.run()
        break
    else:
      messagebox.showerror("Fehler", "Falscher Benutzername oder Passwort!")
  except FileNotFoundError:
    messagebox.showerror(
        "Fehler", "Keine Registrierungsdaten gefunden. Bitte registrieren.")

# Erstellen des Hauptfensters
window = tk.Tk()
window.title("Login-Fenster")

# Erstellen der Widgets
label_username = tk.Label(window, text="Benutzername:")
label_password = tk.Label(window, text="Passwort:")
entry_username = tk.Entry(window)
entry_password = tk.Entry(window, show="*")
button_login = tk.Button(window, text="Einloggen", command=check_credentials)
button_register = tk.Button(window, text="Registrieren", command=register)

# Anordnen der Widgets
label_username.grid(row=0, column=0, sticky=tk.W)
entry_username.grid(row=0, column=1)    
label_password.grid(row=1, column=0, sticky=tk.W)
entry_password.grid(row=1, column=1)
button_login.grid(row=2, column=1, pady=10)
button_register.grid(row=2, column=0, pady=10)

# Starten der Tkinter event loop
window.mainloop()

