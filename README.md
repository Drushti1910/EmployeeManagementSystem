# Employee Management System

A small REST API built with Flask and MySQL. The code is split into route,
service, and repository layers.

## Requirements

- Python 3.10+
- MySQL Server

## Setup

From this directory, create and activate a virtual environment, then install
the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create the database and table using `schema.sql`:

```powershell
cmd.exe /c "mysql -u root -p < schema.sql"
```

If `mysql` is not recognized, open `schema.sql` in MySQL Workbench, connect to
your local MySQL server, and execute the script with the lightning-bolt button.

Copy `.env.example` to `.env`, then set the MySQL password and any other
connection values. Start the API:

```powershell
python run.py
```

The server listens at `http://127.0.0.1:5000`. The API reads database settings
from environment variables; a `.env` file can be loaded by your shell or IDE.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/employees` | List employees |
| GET | `/api/employees/<id>` | Get one employee |
| POST | `/api/employees` | Create an employee |
| PUT | `/api/employees/<id>` | Replace all employee fields |
| PATCH | `/api/employees/<id>` | Update one or more employee fields |
| DELETE | `/api/employees/<id>` | Delete an employee |
| GET | `/health` | Check API availability |

Employee fields are `name`, `email`, `department`, and `salary`. `POST` and
`PUT` require all four fields; `PATCH` accepts any non-empty subset. Email
addresses must be unique.

Example request body:

```json
{
  "name": "Alex Morgan",
  "email": "alex@example.com",
  "department": "Engineering",
  "salary": 75000
}
```

## Project structure

```text
app/
  repositories/   MySQL queries and connection handling
  routes/         HTTP endpoints
  services/       Validation and business rules
  config.py       Environment-based configuration
  db.py           MySQL connection setup
schema.sql        Database and table definition
run.py            Application entry point
```

Run the API tests with:

```powershell
python -m unittest discover -s tests -v
```
