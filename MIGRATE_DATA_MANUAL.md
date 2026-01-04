# 📦 Manual Data Migration: SQLite → PostgreSQL

Since you have data in SQLite that needs to be migrated, follow these simple steps:

## ✅ Step 1: Export Data from SQLite

First, we need to temporarily tell Django to use SQLite for export.

**Option A: Quick Manual Export (Recommended)**

1. Temporarily comment out PostgreSQL settings and use SQLite in `config/settings.py`:

   Find this section:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           ...
       }
   }
   ```

   Temporarily replace it with:
   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.sqlite3",
           "NAME": BASE_DIR / "db.sqlite3",
       }
   }
   ```

2. Export the data:
   ```bash
   python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > data_backup.json
   ```

3. **IMPORTANT**: Restore PostgreSQL settings in `config/settings.py` (uncomment the PostgreSQL config)

## ✅ Step 2: Verify PostgreSQL Connection

Make sure PostgreSQL is running and your `.env` file is correct:

```bash
python manage.py migrate
```

This should create all tables in PostgreSQL (they'll be empty).

## ✅ Step 3: Import Data into PostgreSQL

Now import the exported data:

```bash
python manage.py loaddata data_backup.json
```

You should see output like:
```
Installed 64 object(s) from 1 fixture(s)
```

## ✅ Step 4: Verify Migration

Check that data was transferred:

```bash
python manage.py shell
```

Then in the Python shell:
```python
from dashboards.models import PandharRaste, EHaqq, AgriStack

print(f"PandharRaste: {PandharRaste.objects.count()}")
print(f"EHaqq: {EHaqq.objects.count()}")
print(f"AgriStack: {AgriStack.objects.count()}")
exit()
```

Expected output:
- PandharRaste: 16
- EHaqq: 14
- AgriStack: 13

## ✅ Step 5: Test Your Application

```bash
python manage.py runserver
```

Visit:
- http://127.0.0.1:8000/admin/ - Check your data
- http://127.0.0.1:8000/dashboard/ - Check dashboards

---

## 🎉 Done!

Your data is now in PostgreSQL! Keep `db.sqlite3` as a backup.

