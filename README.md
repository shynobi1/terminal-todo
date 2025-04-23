# Interactive Todo App

A terminal-based todo application that helps you manage your tasks with context and follow-up suggestions.

## Features

- Add todos with descriptions and context
- Set priority levels (1-5)
- Mark todos as complete
- Get follow-up todo suggestions after completing tasks
- Beautiful terminal interface with colors and tables
- Persistent storage of todos

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python todo.py
```

### Main Menu Options

1. **Add Todo**: Create a new todo item with:

   - Title
   - Description
   - Context (why it's important)
   - Priority level (1-5)

2. **List Todos**: View all your todos in a formatted table with:

   - ID
   - Title
   - Priority (shown with stars)
   - Completion status
   - Creation date

3. **Complete Todo**: Mark a todo as complete and optionally add a follow-up todo

4. **Exit**: Close the application

## Data Storage

Your todos are automatically saved to a `todos.json` file in the same directory as the application.
