# Terminal Todo App

A powerful terminal-based todo application that helps you manage your tasks with smart category detection and contextual follow-ups.

## Features

- 📝 Add todos with descriptions and context
- 🏷️ Automatic category detection based on task content
- ⭐ Priority levels (1-3)
- ✅ Mark todos as complete
- 🔄 Follow-up todo suggestions
- 🎨 Beautiful terminal interface with colors and tables
- 💾 Persistent storage of todos
- 🔍 Smart category suggestions using task title, description, and context

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/terminal-todo.git
   cd terminal-todo
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python todo.py
```

### Main Menu Options

1. **Add Todo**

   - Enter the todo title
   - Provide a description
   - Explain why it's important
   - Select priority (Low/Medium/High)
   - Choose or confirm the suggested category

2. **List Todos**

   - View all todos grouped by category
   - See priority levels with colored stars
   - Check completion status
   - View creation dates

3. **Complete Todo**

   - Mark todos as complete
   - Get follow-up todo suggestions
   - Track completion dates

4. **Exit**
   - Save all changes and exit the application

### Category System

The app automatically suggests categories based on:

- Task title
- Description
- Context (why it's important)

Predefined categories include:

- Work
- Personal
- Health
- Shopping
- Learning
- Finance
- Travel
- Hobby
- Maintenance
- Social

New categories are automatically created based on task content when needed.

## Data Storage

Your todos are automatically saved to a `todos.json` file in the same directory as the application. This file is excluded from version control to protect your personal data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python
- Uses the [Rich](https://github.com/Textualize/rich) library for beautiful terminal formatting
