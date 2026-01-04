# 📦 Data Migration Guide: SQLite → PostgreSQL

This guide will help you transfer all your existing data from SQLite (`db.sqlite3`) to PostgreSQL.

---

## ⚠️ Prerequisites

1. ✅ PostgreSQL is installed and running
2. ✅ Database `collector_dashboard_db` is created
3. ✅ `.env` file is configured with correct credentials
4. ✅ `python-decouple` and `psycopg2-binary` are installed

---

## 🚀 Step-by-Step Migration Process

### **Step 1: Install Dependencies**

Make sure you have all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` (PostgreSQL adapter)
- `python-decouple` (for .env file support)

---

### **Step 2: Verify PostgreSQL Connection**

Test that Django can connect to PostgreSQL:

```bash
python manage.py dbshell
```

If it connects successfully, you'll see a PostgreSQL prompt. Type `\q` to exit.

**If you get an error:**
- Check your `.env` file has correct credentials
- Verify PostgreSQL service is running
- Ensure database `collector_dashboard_db` exists

---

### **Step 3: Create Tables in PostgreSQL**

Run migrations to create all tables in PostgreSQL (empty tables):

```bash
python manage.py migrate
```

This will create all the tables but they'll be empty.

---

### **Step 4: Export Data from SQLite**

We'll temporarily switch back to SQLite to export the data.

#### **Option A: Export All Data (Recommended)**

Create a temporary settings file that uses SQLite:

```bash
# Temporarily backup your current settings
copy config\settings.py config\settings.py.postgres

# Export data from SQLite
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_backup.json
```

#### **Option B: Export Specific Apps Only**

If you only want to export your dashboard data:

```bash
python manage.py dumpdata dashboards > dashboards_data.json
```

This exports:
- `PandharRaste` records
- `EHaqq` records
- `AgriStack` records

---

### **Step 5: Switch Back to PostgreSQL**

Your settings are already configured to use PostgreSQL (via `.env` file), so you're good to go!

---

### **Step 6: Import Data into PostgreSQL**

Now import the exported data into PostgreSQL:

#### **If you used Option A (all data):**
```bash
python manage.py loaddata data_backup.json
```

#### **If you used Option B (dashboards only):**
```bash
python manage.py loaddata dashboards_data.json
```

---

### **Step 7: Verify the Migration**

Check that your data was transferred correctly:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from dashboards.models import PandharRaste, EHaqq, AgriStack

# Check record counts
print(f"PandharRaste records: {PandharRaste.objects.count()}")
print(f"EHaqq records: {EHaqq.objects.count()}")
print(f"AgriStack records: {AgriStack.objects.count()}")

# View a few records
print("\nSample PandharRaste records:")
for record in PandharRaste.objects.all()[:5]:
    print(f"  - {record.taluka}")

exit()
```

---

### **Step 8: Test Your Application**

Start the Django server and verify everything works:

```bash
python manage.py runserver
```

Visit:
- `http://127.0.0.1:8000/admin/` - Check admin panel
- `http://127.0.0.1:8000/dashboard/` - Check dashboards

---

## 🔄 Alternative: Automated Migration Script

I've created a helper script `migrate_to_postgres.py` that automates this process. See below for usage.

---

## ⚠️ Important Notes

1. **Backup First**: Always backup your `db.sqlite3` file before migration:
   ```bash
   copy db.sqlite3 db.sqlite3.backup
   ```

2. **User Accounts**: If you have Django superusers, they will be migrated with Option A. If you only export dashboards data, you'll need to recreate superusers:
   ```bash
   python manage.py createsuperuser
   ```

3. **Keep SQLite Backup**: Don't delete `db.sqlite3` immediately. Keep it as a backup until you're 100% sure everything works.

4. **Primary Keys**: Django will preserve primary keys during migration, so relationships remain intact.

---

## 🐛 Troubleshooting

### **Error: "No such table"**
- Make sure you ran `python manage.py migrate` on PostgreSQL first
- Check that all migrations are applied: `python manage.py showmigrations`

### **Error: "Duplicate key"**
- This means data already exists. You can either:
  - Clear the PostgreSQL database and start fresh
  - Use `--natural-foreign` and `--natural-primary` flags with dumpdata

### **Error: "Connection refused"**
- Check PostgreSQL service is running
- Verify credentials in `.env` file
- Test connection: `python manage.py dbshell`

### **Data Count Mismatch**
- Compare counts between SQLite and PostgreSQL
- Check for any errors during `loaddata` command
- Verify all apps were included in export

---

## ✅ Success Checklist

- [ ] PostgreSQL database created
- [ ] `.env` file configured
- [ ] Dependencies installed
- [ ] Migrations run on PostgreSQL
- [ ] Data exported from SQLite
- [ ] Data imported to PostgreSQL
- [ ] Record counts verified
- [ ] Application tested and working
- [ ] SQLite backup kept safe

---

## 🎉 You're Done!

Once everything is verified, you can:
- Keep `db.sqlite3` as a backup (recommended)
- Or delete it if you're confident everything migrated correctly

Your application is now running on PostgreSQL! 🚀

