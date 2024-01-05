# To-Do-List

This is a simple To-Do List application built using Python and the Tkinter library.

## Getting Started

These instructions will help you set up and run the application on your local machine.

### Prerequisites

Make sure you have the following installed on your system:

- [Python](https://www.python.org/) (Version 3.11)
- [Tkinter](https://docs.python.org/3.11/library/tkinter.html) (usually included with Python but you **need version 8.6** to run this app)
- to check your Tkinter Version type the following command into your terminal:
   ```bash
    python -m tkinter
    ```
- You can also create a venv to install Python and run the App
### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/mklr19/todolist.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your_path/todolist
    ```

### Running the Application

Execute the following command in your terminal to start the To-Do-List application:

```bash
python app.py
```
you can also find **app_darkmode.py** and **app_lightmode.py**, which you can also execute.

### Important Files
- **credantials.txt**: Your Usernames and Passwords are stored. (not realy save)
- **tasks.csv**: Every Task is stored in this file.
- **test_app.py**: You can run this code to check the function of the app. (Tests were written with unittest)

## Usage

### Login/Register:

1. When you run the application, a login window will appear.
2. If you don't have an account, click "Register" and follow the instructions to create a new account.
3. If you already have an account, enter your credentials and click "Login."

### Main Window:

- The main window displays the tasks in a treeview with columns for Task, Priority, Status, and Category.
- Use the buttons on the left to perform various actions, such as adding, deleting, and marking tasks.

### Add Task:

1. Click the "Add task" button to open a new window.
2. Enter the task name, select a priority, and provide a category.
3. Click "Add task" to add the task.

### Modify Tasks:

- Select a task in the treeview to perform actions such as deleting, marking as done/undone, or changing properties.

### Sort Tasks:

- Click on the column headers in the treeview to sort tasks based on Task, Priority, Status, or Category.

### Search:

- Use the search box to find tasks based on their names or categories.
