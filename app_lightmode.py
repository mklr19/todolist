import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import csv
import tkinter.font as tkFont 


class Task:
    def __init__(self, username, name, priority='medium', status='unfinished', category='General'):
        self.username = username  
        self.name = name
        self.priority = priority  
        self.status = status
        self.category = category

    def set_priority(self, priority):  
        self.priority = priority
    
    def mark_as_done(self):
        self.status = 'finished'


def priority_ranking(priority):  
    ranks = {'high': 3, 'medium': 2, 'low': 1}
    return ranks.get(priority, 0)


class TaskManager:

    def __init__(self, current_user):
        self.tasks = []
        self.current_user = current_user
        self.load_tasks()

    def add_task(self, task):
        print(f"Adding task: {task.username}, {task.name}, {task.priority}, {task.status}, {task.category}")
        task.username = self.current_user
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully.")


    def delete_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.name != task_name]
        self.save_tasks()

    def mark_task_as_done(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                task.mark_as_done()
                self.save_tasks()


    def save_tasks(self):
        existing_tasks = []
        try:
            with open('tasks.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                existing_tasks = list(reader)
        except FileNotFoundError:
            pass

        existing_tasks = [task for task in existing_tasks if task and task[0] != self.current_user]

        with open('tasks.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for task in existing_tasks:
                writer.writerow(task)
            for task in self.tasks:
                if task.username == self.current_user:
                    writer.writerow([task.username, task.name, task.priority, task.status, task.category])
   
    def load_tasks(self):
        try:
            with open('tasks.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                try:
                    self.tasks = [Task(row[0], row[1], row[2], row[3], row[4]) for row in reader if len(row) == 5 and row[0] == self.current_user]
                except IndexError:
                    print("Fehler: Die CSV-Datei hat nicht die erwartete Struktur.")
                    self.tasks = []
        except FileNotFoundError:
            pass


class TaskManagerApp:
    def __init__(self, username):
        self.username = username  
        self.task_manager = TaskManager(self.username)
        if __name__ == "__main__":
            self.root = tk.Tk()
            self.root.title("To-Do-Maker")
            self.root.tk.call('source', 'forest-light.tcl')
            ttk.Style().theme_use('forest-light')
       

        left_frame  =  ttk.LabelFrame(self.root,  width=300,  height=600)
        left_frame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)

        right_frame  =  ttk.Frame(self.root,  width=300,  height=600)
        right_frame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)
        

        search_task_frame = ttk.Frame(right_frame,  width=300,  height=600,  )
        search_task_frame.pack(side='left',  fill='both',  padx=5,  pady=5,  expand=True)
        search_cat_frame = ttk.Frame(right_frame,  width=300,  height=600)
        search_cat_frame.pack(side='left',  fill='both',  padx=5,  pady=5,  expand=True)

        self.search_label = ttk.Label(search_task_frame, text="Search for Tasks:")
        self.search_label.pack(side="top", fill="x")
        self.search_entry = ttk.Entry(search_task_frame)
        self.search_entry.pack(side="top", fill="x")
        self.search_button = ttk.Button(search_task_frame, text='Search', command=self.search_tasks)
        self.search_button.pack(side="top", pady=3)

        self.search_cat_label = ttk.Label(search_cat_frame, text="Search for Categories:")
        self.search_cat_label.pack(side="top", fill="x")
        self.search_category_entry = ttk.Entry(search_cat_frame)
        self.search_category_entry.pack(side="top", fill="x")
        self.search_category_button = ttk.Button(search_cat_frame, text='Search', command=self.search_in_categories)
        self.search_category_button.pack(side="top", pady=3)
        

        self.tasks_treeview = ttk.Treeview(self.root, columns=("Task", "Priority", "Status", "Category"))
        self.tasks_treeview.column("#0", width=0, stretch=tk.NO)
        self.tasks_treeview.heading("#1", text="Task")
        self.tasks_treeview.heading("#2", text="Priority")
        self.tasks_treeview.heading("#3", text="Status")
        self.tasks_treeview.heading("#4", text="Category")  
        self.tasks_treeview.pack()

        self.add_task_button = ttk.Button(left_frame, text='Add task', command=self.show_add_task_window)
        self.add_task_button.pack(padx=3, pady= 3, fill="x")
        self.delete_task_button = ttk.Button(left_frame, text='Delete task', command=self.delete_task)
        self.delete_task_button.pack(padx=3, pady= 3, fill="x")
        self.delete_category_button = ttk.Button(left_frame, text='Delete category', command=self.delete_category)
        self.delete_category_button.pack(padx=3, pady= 3, fill="x")
        self.mark_task_as_done_button = ttk.Button(left_frame, text='Mark task as done', command=self.mark_task_as_done)
        self.mark_task_as_done_button.pack(padx=3, pady= 3, fill="x")
        self.unfinish_task_button = ttk.Button(left_frame, text='Mark task as undone', command=self.unfinish_task)
        self.change_task_priority_button = ttk.Button(left_frame, text='Change task priority', command=self.change_task_priority)  # neu
        self.unfinish_task_button.pack(padx=3, pady= 3, fill="x")
        self.change_task_priority_button.pack(padx=3, pady= 3, fill="x")
        self.change_task_name_button = ttk.Button(left_frame, text='Change task name', command=self.change_task_name)
        self.change_task_name_button.pack(padx=3, pady= 3, fill="x")
        self.change_category_button = ttk.Button(left_frame, text='Change category', command=self.change_category)
        self.change_category_button.pack(padx=3, pady= 3, fill="x")
        self.tasks_treeview.tag_configure('finished', background='#00FF00')  # Helles Grün
        self.tasks_treeview.tag_configure('unfinished', background='#FF6666')  # Helles Rot
        self.tasks_treeview.pack(fill=tk.BOTH, expand=True)
       
        
 
    def show_add_task_window(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Add Task")
        ttk.Label(add_task_window, text="Task name:").grid(row=0, column=0, padx=10, pady=10)
        task_name_entry = ttk.Entry(add_task_window)
        task_name_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(add_task_window, text="Task priority:").grid(row=1, column=0, padx=10, pady=10)
        priorities = ['high', 'medium', 'low']
        task_priority_combobox = ttk.Combobox(add_task_window, values=priorities)
        task_priority_combobox.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(add_task_window, text="Task category:").grid(row=2, column=0, padx=10, pady=10)
        task_category_entry = ttk.Entry(add_task_window)
        task_category_entry.grid(row=2, column=1, padx=10, pady=10)
        add_task_button = ttk.Button(add_task_window, text='Add task', command=lambda: self.add_task_from_window(
            task_name_entry.get(), task_priority_combobox.get(), task_category_entry.get(), add_task_window))
        add_task_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_task_from_window(self, name, priority, category, window):
        if name and priority and category:
            new_task = Task(username=self.task_manager.current_user, name=name, priority=priority, category=category)
            self.task_manager.add_task(new_task)
            self.refresh_tasks_treeview()
            window.destroy()    

    def change_task_priority(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to change its priority.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        new_priority = self.show_priority_dialog()
        if new_priority:
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.set_priority(new_priority)
            self.refresh_tasks_treeview()

    def show_priority_dialog(self):
        priority_dialog = tk.Toplevel(self.root)
        priority_dialog.title("Change Priority")
        ttk.Label(priority_dialog, text="New priority:").pack(pady=10)
        priorities = ['high', 'medium', 'low']
        priority_combobox = ttk.Combobox(priority_dialog, values=priorities)
        priority_combobox.pack(pady=10)

        def close_dialog():
            priority_dialog.result = priority_combobox.get()
            priority_dialog.destroy()

        ttk.Button(priority_dialog, text="OK", command=close_dialog).pack(pady=10)

        priority_dialog.wait_window()  

        return priority_dialog.result

    def delete_task(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to delete.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        self.task_manager.delete_task(task_name)
        self.refresh_tasks_treeview() 

    def mark_task_as_done(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to mark it as done.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        self.task_manager.mark_task_as_done(task_name)
        self.refresh_tasks_treeview()


    def refresh_tasks_treeview(self):  
        for row in self.tasks_treeview.get_children():
            self.tasks_treeview.delete(row)
        for task in self.task_manager.tasks:
            tag = 'finished' if task.status == 'finished' else 'unfinished'
            self.tasks_treeview.insert("", tk.END, values=(task.name, task.priority, task.status, task.category), tags=(tag,))  # Kategorie hinzufügen
            
    def run(self):
        # Only call mainloop when executed directly
        if __name__ == "__main__":
            self.tasks_treeview.heading("#1", text="Task", command=lambda: self.sort_by_task(self.tasks_treeview, "#1", False))
            self.tasks_treeview.heading("#2", text="Priority", command=lambda: self.sort_by_priority(self.tasks_treeview, "#2", False))
            self.tasks_treeview.heading("#3", text="Status", command=lambda: self.sort_by_status(self.tasks_treeview, "#3", False))
            self.tasks_treeview.heading("#4", text="Category", command=lambda: self.sort_by_category(self.tasks_treeview, "#4", False))

            self.refresh_tasks_treeview()  
            self.root.mainloop()
        
    def sort_by_task(self, tv, col, reverse):
        self.reset_heading_text(tv)
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(reverse=reverse)

        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)

        arrow = " ↓" if reverse else " ↑"
        tv.heading(col, text=f"Task{arrow}", command=lambda: self.sort_by_task(tv, col, not reverse))
        
        
    def sort_by_priority(self, tv, col, reverse):
        self.reset_heading_text(tv)
        priority_map = {'low': 1, 'medium': 2, 'high': 3}
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        
        task_list.sort(key=lambda x: priority_map.get(x[0].lower(), 0), reverse=reverse)
    
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)
        
        arrow = " ↓" if reverse else " ↑"
        tv.heading(col, text=f"Priority{arrow}", command=lambda: self.sort_by_priority(tv, col, not reverse))

       
        
    def sort_by_status(self, tv, col, reverse):
        self.reset_heading_text(tv)
        status_map = {'finished': 1, 'unfinished': 0}
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(key=lambda x: status_map.get(x[0].lower(), 0), reverse=reverse)
    
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)

        arrow = " ↓" if reverse else " ↑"
        tv.heading(col, text=f"Status{arrow}", command=lambda: self.sort_by_status(tv, col, not reverse))

        
    def change_task_name(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to change its name.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        new_name = simpledialog.askstring('Change task name', 'New task name:')
        if new_name:
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.name = new_name
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()
                
    def sort_by_category(self, tv, col, reverse):
        self.reset_heading_text(tv)
        task_list = [(tv.set(k, col), k) for k in tv.get_children('')]
        task_list.sort(reverse=reverse)
    
        for index, (val, k) in enumerate(task_list):
            tv.move(k, '', index)

        arrow = " ↓" if reverse else " ↑"
        tv.heading(col, text=f"Category{arrow}", command=lambda: self.sort_by_category(tv, col, not reverse))
    
    def reset_heading_text(self, tv):
        for col in ["Task", "Priority", "Status", "Category"]:
            tv.heading(col, text=col)   

    def unfinish_task(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to mark it as undone.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        for task in self.task_manager.tasks:
            if task.name == task_name:
                task.status = 'unfinished'
        self.refresh_tasks_treeview()
        self.task_manager.save_tasks()
            

    def delete_category(self):
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to delete its category.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        for task in self.task_manager.tasks:
            if task.name == task_name:
                task.category = "Default"  
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
        selected_task = self.tasks_treeview.selection()
        if not selected_task:
            messagebox.showinfo("Information", "Please select a task to change its category.")
            return

        task_name = self.tasks_treeview.item(selected_task)["values"][0]
        new_category = simpledialog.askstring('Change category', 'New category name:')
        if new_category:
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.category = new_category
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()
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
        with open("credentials.txt", "a") as file:
            with open("credentials.txt", "r") as read_file:
                existing_users = read_file.read()
                if username not in existing_users:
                    file.write(f"{username}:{password}\n")
                    messagebox.showinfo("Sucess", "Registration complete!")
                else:
                    messagebox.showerror("Error", "Username already exists.")
    else:
        messagebox.showerror("Error", "Username and Password can't be empty.")

def check_credentials():
    username = entry_username.get()
    password = entry_password.get()
    try:
        with open("credentials.txt", "r") as file:
            credentials = file.readlines()
        for credential in credentials:
            stored_username, stored_password = credential.strip().split(':')
            if username == stored_username and password == stored_password:
                label_username.grid_forget()
                entry_username.grid_forget()
                label_password.grid_forget()
                entry_password.grid_forget()
                button_login.grid_forget()
                button_register.grid_forget()
                window.destroy()
                app = TaskManagerApp(username=username) 
                app.run()
                break
        else:
            messagebox.showerror("Error", "Wrong Username or Password!")
    except FileNotFoundError:
        messagebox.showerror("Error", "Please register first.")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Login-Fenster")
    window.tk.call('source', 'forest-light.tcl')
    ttk.Style().theme_use('forest-light')

    label_username = ttk.Label(window, text="Username:",)
    label_password = ttk.Label(window, text="Password:")
    entry_username = ttk.Entry(window)
    entry_password = ttk.Entry(window, show="*")
    button_login = ttk.Button(window, text="Login", command=check_credentials)
    button_register = ttk.Button(window, text="Register", command=register)

    label_username.grid(row=0, column=0, sticky=tk.W,padx=5)
    entry_username.grid(row=0, column=1)    
    label_password.grid(row=1, column=0, sticky=tk.W,padx=5)
    entry_password.grid(row=1, column=1)
    button_login.grid(row=2, column=1, pady=10)
    button_register.grid(row=2, column=0, pady=10, padx=30)
    window.mainloop()


