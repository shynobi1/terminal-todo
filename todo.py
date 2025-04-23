#!/usr/bin/env python3

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from datetime import datetime
import json
import os
import re
from collections import Counter

console = Console()

class TodoItem:
    def __init__(self, title, description="", context="", priority=1, completed=False, category=None):
        self.title = title
        self.description = description
        self.context = context
        self.priority = priority
        self.completed = completed
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "context": self.context,
            "priority": self.priority,
            "completed": self.completed,
            "category": self.category,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        todo = cls(
            data["title"],
            data.get("description", ""),
            data.get("context", ""),
            data.get("priority", 1),
            data.get("completed", False),
            data.get("category")
        )
        todo.created_at = data.get("created_at", datetime.now().isoformat())
        todo.completed_at = data.get("completed_at")
        return todo

class TodoApp:
    def __init__(self):
        self.todos = []
        self.categories = set()
        self.data_file = "todos.json"
        self.load_todos()
        self.update_categories()

    def load_todos(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.todos = [TodoItem.from_dict(item) for item in data]

    def save_todos(self):
        with open(self.data_file, 'w') as f:
            json.dump([todo.to_dict() for todo in self.todos], f, indent=2)

    def update_categories(self):
        self.categories = {todo.category for todo in self.todos if todo.category}

    def extract_keywords(self, text):
        # Remove common words and get meaningful keywords
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could'}
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in common_words and len(word) > 2]

    def suggest_category(self, title, description, context):
        # Base categories with their keywords and weights
        base_categories = {
            "work": {
                "keywords": ["work", "job", "office", "meeting", "project", "deadline", "client", "business", "team", "career", "professional"],
                "weight": 1.0
            },
            "personal": {
                "keywords": ["personal", "family", "friend", "home", "house", "life", "relationship", "self", "private"],
                "weight": 1.0
            },
            "health": {
                "keywords": ["health", "exercise", "gym", "doctor", "medical", "fitness", "diet", "wellness", "mental", "physical", "sleep"],
                "weight": 1.0
            },
            "shopping": {
                "keywords": ["buy", "shopping", "purchase", "store", "market", "shop", "order", "groceries", "retail"],
                "weight": 1.0
            },
            "learning": {
                "keywords": ["learn", "study", "read", "course", "education", "skill", "knowledge", "research", "practice", "training"],
                "weight": 1.0
            },
            "finance": {
                "keywords": ["money", "bill", "pay", "bank", "finance", "budget", "investment", "saving", "debt", "expense"],
                "weight": 1.0
            },
            "travel": {
                "keywords": ["travel", "trip", "vacation", "flight", "hotel", "destination", "journey", "tour"],
                "weight": 1.0
            },
            "hobby": {
                "keywords": ["hobby", "craft", "art", "music", "game", "sport", "activity", "interest", "pastime"],
                "weight": 1.0
            },
            "maintenance": {
                "keywords": ["fix", "repair", "maintain", "clean", "organize", "setup", "install", "update", "improve"],
                "weight": 1.0
            },
            "social": {
                "keywords": ["party", "event", "gathering", "meet", "social", "network", "community", "group"],
                "weight": 1.0
            }
        }
        
        # Combine all text for analysis
        text = f"{title} {description} {context}".lower()
        keywords = self.extract_keywords(text)
        
        # Calculate scores for each category
        category_scores = {}
        for category, data in base_categories.items():
            score = 0
            for word in keywords:
                if word in data["keywords"]:
                    score += data["weight"]
            category_scores[category] = score
        
        # Get top categories
        top_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        # If we have a clear winner (score > 0), return it
        if top_categories and top_categories[0][1] > 0:
            return top_categories[0][0]
        
        # If no clear category, create a new one based on the most significant word
        if keywords:
            word_counts = Counter(keywords)
            most_common = word_counts.most_common(1)[0][0]
            # Capitalize the first letter and make it plural if appropriate
            new_category = most_common.capitalize() + 's' if not most_common.endswith('s') else most_common.capitalize()
            return new_category
        
        # If no keywords found, create a category based on the first word of the title
        first_word = title.split()[0].capitalize() if title else "Task"
        return first_word + 's' if not first_word.endswith('s') else first_word

    def show_numbered_menu(self, title, options):
        console.print(f"\n[bold]{title}[/bold]")
        for i, option in enumerate(options, 1):
            console.print(f"{i}. {option}")
        while True:
            try:
                choice = int(Prompt.ask("Enter your choice (number)"))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                console.print("[red]Invalid choice. Please enter a valid number.[/red]")
            except ValueError:
                console.print("[red]Please enter a number.[/red]")

    def add_todo(self):
        title = Prompt.ask("What's your new todo?")
        description = Prompt.ask("Can you describe what needs to be done?")
        context = Prompt.ask("Why is this important?")
        
        # Priority selection
        priority_options = ["Low (1)", "Medium (2)", "High (3)"]
        priority_choice = self.show_numbered_menu("Select priority", priority_options)
        priority = int(priority_choice.split()[1].strip('()'))
        
        # Category selection
        suggested_category = self.suggest_category(title, description, context)
        category_options = list(self.categories) + ["New Category"]
        
        if category_options:
            console.print(f"\nSuggested category: [green]{suggested_category}[/green]")
            category = self.show_numbered_menu("Select category", category_options)
        else:
            category = suggested_category
        
        if category == "New Category":
            category = Prompt.ask("Enter new category name")
        
        todo = TodoItem(title, description, context, priority, category=category)
        self.todos.append(todo)
        self.update_categories()
        self.save_todos()
        console.print("[green]Todo added successfully![/green]")

    def list_todos(self):
        # Group todos by category
        todos_by_category = {}
        for todo in self.todos:
            if todo.category not in todos_by_category:
                todos_by_category[todo.category] = []
            todos_by_category[todo.category].append(todo)

        for category, todos in sorted(todos_by_category.items()):
            table = Table(show_header=True, header_style="bold magenta", title=f"Category: {category}")
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Priority")
            table.add_column("Status")
            table.add_column("Created")

            for i, todo in enumerate(todos, 1):
                status = "✅" if todo.completed else "❌"
                priority_color = {
                    1: "red",
                    2: "yellow",
                    3: "green"
                }.get(todo.priority, "white")
                
                table.add_row(
                    str(i),
                    todo.title,
                    f"[{priority_color}]{'⭐' * todo.priority}[/{priority_color}]",
                    status,
                    datetime.fromisoformat(todo.created_at).strftime("%Y-%m-%d %H:%M")
                )
            
            console.print(table)
            console.print()  # Add spacing between category tables

    def complete_todo(self):
        self.list_todos()
        if not self.todos:
            console.print("[yellow]No todos to complete![/yellow]")
            return

        try:
            todo_options = [f"{i}. {todo.title}" for i, todo in enumerate(self.todos, 1)]
            selected_todo = self.show_numbered_menu("Select todo to complete", todo_options)
            todo_id = int(selected_todo.split('.')[0])
            todo = self.todos[todo_id - 1]
            
            if todo.completed:
                console.print("[yellow]This todo is already completed![/yellow]")
                return

            todo.completed = True
            todo.completed_at = datetime.now().isoformat()
            self.save_todos()
            
            console.print(f"[green]Completed: {todo.title}[/green]")
            
            # Suggest follow-up todo
            if Confirm.ask("Would you like to add a follow-up todo?"):
                self.add_todo()
                
        except (ValueError, IndexError):
            console.print("[red]Invalid todo number![/red]")

    def run(self):
        while True:
            menu_options = ["Add Todo", "List Todos", "Complete Todo", "Exit"]
            choice = self.show_numbered_menu("Todo App", menu_options)
            
            if choice == "Add Todo":
                self.add_todo()
            elif choice == "List Todos":
                self.list_todos()
            elif choice == "Complete Todo":
                self.complete_todo()
            elif choice == "Exit":
                console.print("[yellow]Goodbye![/yellow]")
                break

if __name__ == "__main__":
    app = TodoApp()
    app.run() 