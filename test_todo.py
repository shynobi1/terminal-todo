import unittest
from todo import TodoItem, TodoApp
import os
import json
from datetime import datetime

class TestTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = TodoApp()
        self.app.data_file = "test_todos.json"
        # Clear any existing test data
        if os.path.exists(self.app.data_file):
            os.remove(self.app.data_file)

    def tearDown(self):
        # Clean up test data
        if os.path.exists(self.app.data_file):
            os.remove(self.app.data_file)

    def test_todo_item_creation(self):
        todo = TodoItem("Test Todo", "Test Description", "Test Context", 2)
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertEqual(todo.context, "Test Context")
        self.assertEqual(todo.priority, 2)
        self.assertFalse(todo.completed)
        self.assertIsNotNone(todo.created_at)

    def test_todo_item_to_dict(self):
        todo = TodoItem("Test Todo", "Test Description", "Test Context", 2)
        todo_dict = todo.to_dict()
        self.assertEqual(todo_dict["title"], "Test Todo")
        self.assertEqual(todo_dict["description"], "Test Description")
        self.assertEqual(todo_dict["context"], "Test Context")
        self.assertEqual(todo_dict["priority"], 2)
        self.assertFalse(todo_dict["completed"])

    def test_todo_item_from_dict(self):
        original_todo = TodoItem("Test Todo", "Test Description", "Test Context", 2)
        todo_dict = original_todo.to_dict()
        new_todo = TodoItem.from_dict(todo_dict)
        self.assertEqual(new_todo.title, original_todo.title)
        self.assertEqual(new_todo.description, original_todo.description)
        self.assertEqual(new_todo.context, original_todo.context)
        self.assertEqual(new_todo.priority, original_todo.priority)
        self.assertEqual(new_todo.completed, original_todo.completed)

    def test_save_and_load_todos(self):
        # Create test todos
        todo1 = TodoItem("Todo 1", "Description 1", "Context 1", 1)
        todo2 = TodoItem("Todo 2", "Description 2", "Context 2", 2)
        self.app.todos = [todo1, todo2]
        
        # Save todos
        self.app.save_todos()
        
        # Create new app instance and load todos
        new_app = TodoApp()
        new_app.data_file = self.app.data_file
        new_app.load_todos()
        
        # Verify loaded todos
        self.assertEqual(len(new_app.todos), 2)
        self.assertEqual(new_app.todos[0].title, "Todo 1")
        self.assertEqual(new_app.todos[1].title, "Todo 2")

    def test_category_suggestion(self):
        # Test work-related todo
        category = self.app.suggest_category(
            "Finish project report",
            "Need to complete the quarterly report",
            "Important for team review"
        )
        self.assertEqual(category, "work")

        # Test shopping-related todo
        category = self.app.suggest_category(
            "Buy groceries",
            "Need milk and bread",
            "Running out of essentials"
        )
        self.assertEqual(category, "shopping")

        # Test learning-related todo
        category = self.app.suggest_category(
            "Study Python",
            "Complete Python course",
            "Important for career growth"
        )
        self.assertEqual(category, "learning")

if __name__ == '__main__':
    unittest.main() 