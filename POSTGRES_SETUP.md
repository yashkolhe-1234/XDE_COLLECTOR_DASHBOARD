# PostgreSQL Setup Guide

## Step 1: Install PostgreSQL

### Windows:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` superuser
4. Default port is `5432`

### Alternative: Using Chocolatey
```bash
choco install postgresql
```

## Step 2: Create Database

1. Open **pgAdmin** (comes with PostgreSQL installation) or use **psql** command line

### Using pgAdmin:
- Right-click on "Databases" → "Create" → "Database"
- Name: `collector_dashboard_db`
- Click "Save"

### Using psql (Command Line):
```bash
psql -U postgres
```

Then run:
```sql
CREATE DATABASE collector_dashboard_db;
\q
```

## Step 3: Update Django Settings

The settings have been updated in `config/settings.py`. You may need to adjust:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "collector_dashboard_db",      # Your database name
        "USER": "postgres",                     # Your PostgreSQL username
        "PASSWORD": "your_password_here",       # Your PostgreSQL password
        "HOST": "localhost",                    # Usually localhost
        "PORT": "5432",                         # Default PostgreSQL port
    }
}
```

## Step 4: Install Python PostgreSQL Adapter

```bash
pip install psycopg2-binary
```

Or if you're using a virtual environment:
```bash
.\collector_revenue\Scripts\activate
pip install psycopg2-binary
```

## Step 5: Run Migrations

After installing psycopg2-binary, run:

```bash
python manage.py migrate
```

This will create all the tables in your PostgreSQL database.

## Step 6: Create Superuser (if needed)

```bash
python manage.py createsuperuser
```

## Step 7: Test the Connection

Run the Django server:
```bash
python manage.py runserver
```

If it starts without errors, PostgreSQL is configured correctly!

---

## Step 8: Migrate Existing Data (If You Have SQLite Data)

If you have existing data in `db.sqlite3` that you want to transfer to PostgreSQL, see:

📖 **[DATA_MIGRATION_GUIDE.md](DATA_MIGRATION_GUIDE.md)** - Complete step-by-step guide

**Quick Migration (Automated):**
```bash
python migrate_to_postgres.py
```

This script will:
- Export all data from SQLite
- Import it into PostgreSQL
- Verify the migration was successful

**Manual Migration:**
See `DATA_MIGRATION_GUIDE.md` for detailed manual steps.

## Troubleshooting

### Error: "FATAL: password authentication failed"
- Check your PostgreSQL password in `settings.py`
- Make sure the `postgres` user password is correct

### Error: "could not connect to server"
- Make sure PostgreSQL service is running
- Check if PostgreSQL is running on port 5432
- Verify HOST and PORT in settings.py

### Error: "database does not exist"
- Create the database first (see Step 2)
- Check the database name in settings.py matches the created database

### Windows Service Check:
```bash
# Check if PostgreSQL service is running
sc query postgresql-x64-16
```

### Start PostgreSQL Service (if stopped):
```bash
net start postgresql-x64-16
```

## Security Note

For production, use environment variables instead of hardcoding credentials:

```python
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "collector_dashboard_db"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}
```

