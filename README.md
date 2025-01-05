
# Task List API Backend

A backend RESTful API built with Flask to manage tasks and goals in a full-stack project. The API is integrated with a PostgreSQL database and provides endpoints for creating, reading, updating, and deleting tasks and goals. 

## About the Project

This backend application is part of a full-stack project created to practice and strengthen skills in backend development, API design, and database integration. It serves as the server-side component of the TaskList application.

### Deployed Application

- **Backend Deployment**: [Deployed Backend on Render](https://task-list-api-ai13.onrender.com)
- **Frontend Deployment**: [Deployed Frontend on GitHub Pages](https://nerpassevera.github.io/task-list-front-end)

## Features

### Tasks
- **Create Tasks**: Add new tasks.
- **Delete Tasks**: Remove tasks from the list.
- **Read Tasks**: Retrieve all tasks or a single task.
- **Update Tasks**: Update task information.
- **Mark Tasks as Completed/Incompleted**: Change the task status.
- **Slack Notifications**: Notify a Slack channel when a task is marked as completed.

### Goals
- **Create Goals**: Add new goals.
- **Delete Goals**: Remove goals from the list.
- **Read Goals**: Retrieve all goals or a single goal.
- **Update Goals**: Update goal information.
- **Assign Tasks to Goals**: Link multiple tasks to specific goals.

## Technologies Used

- **Flask**: Lightweight web framework for Python.
- **SQLAlchemy**: ORM for database management.
- **Alembic**: Database migration tool.
- **PostgreSQL**: Relational database for storing tasks and goals.
- **Flask-CORS**: Manage Cross-Origin Resource Sharing for API.
- **Python-dotenv**: Manage environment variables using a `.env` file.

## API Endpoints

### Tasks Routes

| Method   | Endpoint                    | Description                              |
|----------|-----------------------------|------------------------------------------|
| GET      | `/tasks`                    | Retrieve all tasks.                      |
| POST     | `/tasks`                    | Create a new task.                       |
| GET      | `/tasks/<task_id>`          | Retrieve a specific task by ID.          |
| PUT      | `/tasks/<task_id>`          | Update a specific task by ID.            |
| DELETE   | `/tasks/<task_id>`          | Delete a specific task by ID.            |
| PATCH    | `/tasks/<task_id>/mark_complete` | Mark a task as completed.           |
| PATCH    | `/tasks/<task_id>/mark_incomplete` | Mark a task as incomplete.         |

### Goals Routes

| Method   | Endpoint                    | Description                              |
|----------|-----------------------------|------------------------------------------|
| GET      | `/goals`                    | Retrieve all goals.                      |
| POST     | `/goals`                    | Create a new goal.                       |
| GET      | `/goals/<goal_id>`          | Retrieve a specific goal by ID.          |
| PUT      | `/goals/<goal_id>`          | Update a specific goal by ID.            |
| DELETE   | `/goals/<goal_id>`          | Delete a specific goal by ID.            |
| POST     | `/goals/<goal_id>/tasks`    |Assign multiple tasks to a specific goal. |
| GET      | `/goals/<goal_id>/tasks`	 |Retrieve all tasks associated with a goal.|

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- PostgreSQL

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Nerpassevera/task-list-api.git
    cd task-list-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate   # On Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    cp .env.example .env
    ```

    Update `.env` with your database URL and Slack API key:
    ```
    SQLALCHEMY_DATABASE_URI=<your_database_url>
    SLACK_API_KEY=<your_slack_api_key>
    ```

5. Run database migrations:
    ```bash
    flask db upgrade
    ```

6. Start the development server:
    ```bash
    flask run
    ```

## Future Plans

- Allow users to dynamically change the Slack channel for notifications.
- Create user accounts

## Author

- [Tatiana Trofimova](https://github.com/Nerpassevera)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
