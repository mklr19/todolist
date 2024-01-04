import unittest
from app import TaskManagerApp, Task, TaskManager

class TestTask(unittest.TestCase):
    def test_task_creation(self):
        task = Task("User", "Sample Task", "high", "unfinished", "General")
        self.assertEqual(task.username, "User")
        self.assertEqual(task.name, "Sample Task")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, "unfinished")
        self.assertEqual(task.category, "General")

    def test_task_priority(self):
        task = Task("User", "Sample Task", "low", "unfinished", "General")
        task.set_priority("high")
        self.assertEqual(task.priority, "high")

    def test_task_completion(self):
        task = Task("User", "Sample Task", "medium", "unfinished", "General")
        task.mark_as_done()
        self.assertEqual(task.status, "finished")
    
class TestTaskManagerClass(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager('Marcel')

    def test_add_task(self):
        task = Task('Marcel', 'Do something')
        self.task_manager.add_task(task)
        self.assertEqual(len(self.task_manager.tasks), 1)

    def test_delete_task(self):
        task = Task('Marcel', 'Do something')
        self.task_manager.add_task(task)
        self.task_manager.delete_task('Do something')
        self.assertEqual(len(self.task_manager.tasks), 0)

    def test_mark_task_as_done(self):
        task = Task('Marcel', 'Do something')
        self.task_manager.add_task(task)
        self.task_manager.mark_task_as_done('Do something')
        self.assertEqual(self.task_manager.tasks[0].status, 'finished')  
        self.task_manager.delete_task('Do something')  
        self.assertEqual(len(self.task_manager.tasks), 0)
        
if __name__ == '__main__':
    unittest.main()