# 🚀 Quick Start Guide - How to Run Excel Import

## 📍 Step-by-Step Instructions

---

## **STEP 1: Install Dependencies** (First time only)

Open terminal/command prompt in project folder and run:

```bash
pip install -r requirements.txt
```

---

## **STEP 2: Run Database Migrations** (First time only)

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## **STEP 3: Create Superuser** (First time only)

```bash
python manage.py createsuperuser
```

Enter:
- Username: (your choice, e.g., `admin`)
- Email: (optional, press Enter)
- Password: (enter password)

---

## **STEP 4: Start Django Server**

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## **STEP 5: Access the Application**

### **Option A: Import Excel via Admin (Recommended)**

1. **Open Admin Panel:**
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Login:**
   - Enter your superuser username and password
   - Click "Log in"

3. **Navigate to पांढर रस्ते:**
   - In the admin panel, find "DASHBOARDS" section
   - Click on **"पांढर रस्ते"** (or "Pandhar Raste")

4. **Import Excel File:**
   - You'll see the list of records (may be empty)
   - At the top, you'll see an **"Action"** dropdown
   - Select **"Import from Excel file"** from the dropdown
   - Click the **"Go"** button next to it
   - This will take you to the import page

5. **Upload File:**
   - Click **"Choose File"** button
   - Select your `.xlsx` file
   - (Optional) Enter sheet name if needed
   - (Optional) Change header row number (default: 1)
   - Check/uncheck "Update existing records"
   - Click **"Import Data"** button

6. **View Results:**
   - You'll see success/error messages
   - Redirects back to records list
   - Your data is now imported!

---

### **Option B: View Dashboard**

1. **Open Dashboard:**
   ```
   http://127.0.0.1:8000/dashboard/
   ```

2. **Navigate to पांढर रस्ते:**
   ```
   http://127.0.0.1:8000/dashboard/pandhar-raste/
   ```
   OR click "पांढर रस्ते" in the sidebar

3. **View Data:**
   - KPIs at the top
   - Charts in the middle
   - Detailed table at the bottom

---

### **Option C: Import via Command Line**

Open a **NEW terminal window** (keep server running in first terminal):

```bash
python manage.py import_pandhar_raste "C:\path\to\your\file.xlsx"
```

Example:
```bash
python manage.py import_pandhar_raste "C:\Users\YourName\Desktop\pandhar_raste_data.xlsx"
```

---

## 📋 Complete URL List

| Purpose | URL |
|---------|-----|
| **Admin Login** | `http://127.0.0.1:8000/admin/` |
| **पांढर रस्ते Admin** | `http://127.0.0.1:8000/admin/dashboards/pandharraste/` |
| **Import Excel Page** | `http://127.0.0.1:8000/admin/dashboards/pandharraste/import-excel/` |
| **Dashboard Home** | `http://127.0.0.1:8000/dashboard/` |
| **पांढर रस्ते Dashboard** | `http://127.0.0.1:8000/dashboard/pandhar-raste/` |

---

## 🎯 Quick Workflow

### **First Time Setup:**
1. `pip install -r requirements.txt`
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser`
5. `python manage.py runserver`

### **Every Time You Use:**
1. `python manage.py runserver`
2. Go to: `http://127.0.0.1:8000/admin/`
3. Login
4. Click "पांढर रस्ते"
5. Select "Import from Excel file" → Go
6. Upload file → Import
7. View dashboard: `http://127.0.0.1:8000/dashboard/pandhar-raste/`

---

## 📝 Excel File Format

Your Excel file should have:
- **Column A:** Taluka name
- **Column B:** Geo-tag Roads (number)
- **Column C:** Cleared Roads (number)
- **Column D:** Cleared Length (km, decimal)
- **Column E:** Farmers Benefited (number)

First row can be headers.

---

## ✅ Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Migrations run (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Server running (`python manage.py runserver`)
- [ ] Excel file ready (correct format)
- [ ] Ready to import!

---

**That's it! You're ready to import Excel data!** 🎉

