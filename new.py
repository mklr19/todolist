import sys
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTreeView, QTreeWidgetItem, QInputDialog, QMessageBox

class Task:
    def __init__(self, name, priority='medium', status='unfinished', category='General'):
        self.name = name
        self.priority = priority
        self.status = status
        self.category = category

    def set_priority(self, priority):
        self.priority = priority
    
    def mark_as_done(self):
        self.status = 'finished'

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
            for task in self.tasks:
                csvfile.write(f"{task.name},{task.priority},{task.status},{task.category}\n")

    def load_tasks(self):
        try:
            with open('tasks.csv', 'r') as csvfile:
                for line in csvfile:
                    values = line.strip().split(',')
                    if len(values) == 4:
                        self.tasks.append(Task(values[0], values[1], values[2], values[3]))
                    else:
                        print("Fehler: Die CSV-Datei hat nicht die erwartete Struktur.")
                        self.tasks = []
        except FileNotFoundError:
            pass

class TaskManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.task_manager = TaskManager()
        self.setWindowTitle("To-Do-Maker")

        self.search_button = QPushButton('Search in Tasks', self)
        self.search_button.clicked.connect(self.search_tasks)

        self.search_entry = QLineEdit(self)

        self.search_category_button = QPushButton('Search in Categories', self)
        self.search_category_button.clicked.connect(self.search_in_categories)

        self.search_category_entry = QLineEdit(self)

        self.tasks_treeview = QTreeView(self)
        self.tasks_treeview.setHeaderHidden(False)  # Zeigt den Header an
        self.tasks_treeview_model = QStandardItemModel(self)
        self.tasks_treeview.setModel(self.tasks_treeview_model)
        self.tasks_treeview_model.setHorizontalHeaderLabels(["Task", "Priority", "Status", "Category"])

        self.add_task_button = QPushButton('Add task', self)
        self.add_task_button.clicked.connect(self.add_task)

        self.delete_task_button = QPushButton('Delete task', self)
        self.delete_task_button.clicked.connect(self.delete_task)

        self.mark_task_as_done_button = QPushButton('Mark task as done', self)
        self.mark_task_as_done_button.clicked.connect(self.mark_task_as_done)

        self.unfinish_task_button = QPushButton('Mark task as undone', self)
        self.unfinish_task_button.clicked.connect(self.unfinish_task)

        self.change_task_priority_button = QPushButton('Change task priority', self)
        self.change_task_priority_button.clicked.connect(self.change_task_priority)

        self.change_task_name_button = QPushButton('Change task name', self)
        self.change_task_name_button.clicked.connect(self.change_task_name)

        self.change_category_button = QPushButton('Change category', self)
        self.change_category_button.clicked.connect(self.change_category)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_button)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.search_category_button)
        layout.addWidget(self.search_category_entry)
        layout.addWidget(self.tasks_treeview)
        layout.addWidget(self.add_task_button)
        layout.addWidget(self.delete_task_button)
        layout.addWidget(self.mark_task_as_done_button)
        layout.addWidget(self.unfinish_task_button)
        layout.addWidget(self.change_task_priority_button)
        layout.addWidget(self.change_task_name_button)
        layout.addWidget(self.change_category_button)

        self.refresh_tasks_treeview()

    def add_task(self):
        task_name, ok = QInputDialog.getText(self, 'Add task', 'Task name:')
        task_priority, ok_priority = QInputDialog.getText(self, 'Add task', 'Task priority (high, medium, low):')
        task_category, ok_category = QInputDialog.getText(self, 'Add task', 'Task category:')
        
        if ok and ok_priority and ok_category:
            self.task_manager.add_task(Task(task_name, task_priority, 'unfinished', task_category))
            self.refresh_tasks_treeview()

    def change_task_priority(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            new_priority, ok = QInputDialog.getText(self, 'Change priority', 'New priority (high, medium, low):')
            if ok:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.set_priority(new_priority)
                self.refresh_tasks_treeview()

    def delete_task(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            self.task_manager.delete_task(task_name)
            self.refresh_tasks_treeview()

    def mark_task_as_done(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            self.task_manager.mark_task_as_done(task_name)
            self.refresh_tasks_treeview()

    def refresh_tasks_treeview(self):
        self.tasks_treeview.model().removeRows(0, self.tasks_treeview.model().rowCount())

        for task in self.task_manager.tasks:
            item = QTreeWidgetItem([task.name, task.priority, task.status, task.category])
            tag = 'finished' if task.status == 'finished' else 'unfinished'
            item.setData(0, 0, tag)
            self.tasks_treeview_model.insertRow(0, item)



    def run(self):
        self.show()

    def change_task_name(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            new_name, ok = QInputDialog.getText(self, 'Change task name', 'New task name:')
            if ok:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.name = new_name
                self.refresh_tasks_treeview()
                self.task_manager.save_tasks()

    def change_category(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            new_category, ok = QInputDialog.getText(self, 'Change category', 'New category name:')
            if ok:
                for task in self.task_manager.tasks:
                    if task.name == task_name:
                        task.category = new_category
                self.refresh_tasks_treeview()
                self.task_manager.save_tasks()

    def unfinish_task(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.status = 'unfinished'
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()

    def delete_category(self):
        selected_task_id = self.tasks_treeview.currentIndex().row()
        if selected_task_id != -1:
            task_name = self.task_manager.tasks[selected_task_id].name
            for task in self.task_manager.tasks:
                if task.name == task_name:
                    task.category = "Default"
            self.refresh_tasks_treeview()
            self.task_manager.save_tasks()

    def search_tasks(self):
        search_query = self.search_entry.text().lower()
        self.tasks_treeview.clear()
        for task in self.task_manager.tasks:
            if search_query in task.name.lower():
                item = QTreeWidgetItem([task.name, task.priority, task.status, task.category])
                tag = 'finished' if task.status == 'finished' else 'unfinished'
                item.setData(0, 0, tag)
                self.tasks_treeview.addTopLevelItem(item)

    def search_in_categories(self):
        search_query = self.search_category_entry.text().lower()
        self.tasks_treeview.clear()
        for task in self.task_manager.tasks:
            if search_query in task.category.lower():
                item = QTreeWidgetItem([task.name, task.priority, task.status, task.category])
                tag = 'finished' if task.status == 'finished' else 'unfinished'
                item.setData(0, 0, tag)
                self.tasks_treeview.addTopLevelItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Verhindert das automatische Schließen beim Schließen des Hauptfensters

    login_window = QWidget()

    label_username = QLabel("Benutzername:", login_window)
    label_password = QLabel("Passwort:", login_window)
    entry_username = QLineEdit(login_window)
    entry_password = QLineEdit(login_window)
    button_login = QPushButton("Einloggen", login_window)
    button_register = QPushButton("Registrieren", login_window)

    layout = QVBoxLayout(login_window)
    layout.addWidget(label_username)
    layout.addWidget(entry_username)
    layout.addWidget(label_password)
    layout.addWidget(entry_password)
    layout.addWidget(button_login)
    layout.addWidget(button_register)

    def register():
        username = entry_username.text()
        password = entry_password.text()
        if username and password:
            with open("credentials.txt", "a") as file:
                file.write(f"{username}:{password}\n")
            QMessageBox.information(login_window, "Erfolg", "Registrierung erfolgreich!")
        else:
            QMessageBox.critical(login_window, "Fehler", "Benutzername und Passwort dürfen nicht leer sein.")

    def check_credentials():
        username = entry_username.text()
        password = entry_password.text()
        try:
            with open("credentials.txt", "r") as file:
                credentials = file.readlines()
            for credential in credentials:
                stored_username, stored_password = credential.strip().split(':')
                if username == stored_username and password == stored_password:
                    login_window.close()
                    task_manager_app = TaskManagerApp()
                    task_manager_app.run()
                    break
            else:
                QMessageBox.critical(login_window, "Fehler", "Falscher Benutzername oder Passwort!")
        except FileNotFoundError:
            QMessageBox.critical(login_window, "Fehler", "Keine Registrierungsdaten gefunden. Bitte registrieren.")

    button_login.clicked.connect(check_credentials)
    button_register.clicked.connect(register)

    login_window.show()
    sys.exit(app.exec_())
