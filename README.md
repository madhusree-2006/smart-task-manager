# Smart Task Manager

A simple task-management web application built with Python, Flask, SQLite, HTML and CSS. It is designed as a beginner-friendly portfolio project for demonstrating CRUD operations, database integration, form handling, search, filtering and responsive UI.

## Features

- Create tasks with a title, description, due date and priority
- Edit and delete tasks
- Mark tasks as completed or pending
- Search by task title or description
- Filter by all, pending or completed tasks
- Automatically stores tasks in a local SQLite database
- Responsive layout for desktop and mobile screens

## Tech stack

- Python 3.10+
- Flask
- SQLite
- HTML5 and CSS3

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (optional but recommended).

   **Windows**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

The SQLite database (`tasks.db`) is created automatically when the application starts.

## Project structure

```text
smart-task-manager/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   └── edit.html
└── static/
    └── style.css
```

## Future improvements

- User registration and login
- Unit tests with pytest
- Task reminders
- REST API endpoints
- Deploy to a hosting platform

## Portfolio note

Run and test the application, understand the main routes in `app.py`, and customize it before presenting it as your work. Add screenshots of the running application to this README after testing.
