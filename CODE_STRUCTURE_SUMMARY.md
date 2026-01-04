# 📊 Code Structure Summary - Collector Dashboard

## 🏗️ Project Overview

**Django 5.2.9** web application for managing and visualizing government scheme data (Marathi language support). Uses **PostgreSQL** database with Excel import functionality.

---

## 📁 Project Structure

```
XDE_COLLECTOR_DASHBOARD/
├── config/                    # Django project configuration
│   ├── settings.py           # Main settings (PostgreSQL, apps, middleware)
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py               # WSGI config
│   └── asgi.py               # ASGI config
│
├── dashboards/                # Main dashboard app
│   ├── models.py             # 3 models: PandharRaste, EHaqq, AgriStack
│   ├── views.py              # 7 dashboard views
│   ├── urls.py               # Dashboard URL patterns
│   ├── admin.py              # Django admin with Excel import
│   ├── sidebar.py            # Navigation menu items
│   ├── services/
│   │   └── pandhar_raste_service.py  # KPI & chart data logic
│   └── templates/
│       ├── dashboards/       # Dashboard HTML templates
│       └── admin/           # Excel import forms
│
├── data_ingestion/           # Excel import functionality
│   ├── services/
│   │   └── excel_importer.py  # Core Excel parsing & import logic
│   └── management/commands/   # Django management commands
│       ├── import_pandhar_raste.py
│       ├── import_e_haqq.py
│       └── import_agristack.py
│
├── users/                    # User management (placeholder)
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (DB credentials)
└── db.sqlite3               # SQLite backup (migrated to PostgreSQL)
```

---

## 🗄️ Database Models

### 1. **PandharRaste** (पांढर रस्ते)
- **Purpose**: Road infrastructure scheme data (taluka-wise)
- **Fields**:
  - `taluka` (CharField) - Taluka name
  - `geo_tag_roads` (Integer) - Geo-tagged roads count
  - `geo_tag_length_km` (Float) - Geo-tagged length in km
  - `cleared_roads` (Integer) - Cleared encroachment roads
  - `cleared_length_km` (Float) - Cleared length in km
  - `farmers_benefited` (Integer) - Benefited farmers count

### 2. **EHaqq** (ई-हक्क)
- **Purpose**: E-rights application scheme data
- **Fields**:
  - `taluka` (CharField, unique) - Taluka name
  - `total_applications` (Integer) - Total applications
  - `approved_applications` (Integer) - Approved count
  - `rejected_applications` (Integer) - Rejected count
  - `pending_applications` (Integer) - Pending count
  - `approved_percentage` (Float) - Approval percentage
  - `rejected_percentage` (Float) - Rejection percentage
  - `pending_percentage` (Float) - Pending percentage
  - `period_work_count` (Integer) - Period work count

### 3. **AgriStack** (ॲग्रीस्टॅक)
- **Purpose**: Agriculture stack farmer ID scheme data
- **Fields**:
  - `taluka` (CharField, unique) - Taluka name
  - `total_villages` (Integer) - Total villages
  - `total_farmers` (Integer) - Total farmers
  - `farmers_with_id_created` (Integer) - Farmers with ID created
  - `farmers_pending_id` (Integer) - Farmers pending ID creation
  - `completion_percentage` (Float) - Completion percentage

---

## 🎯 Views & URLs

### Root URLs (`config/urls.py`)
- `/admin/` → Django admin panel
- `/dashboard/` → Dashboard app URLs

### Dashboard URLs (`dashboards/urls.py`)
- `/dashboard/` → Home dashboard
- `/dashboard/pandhar-raste/` → Pandhar Raste dashboard
- `/dashboard/e-haqq/` → E-Haqq dashboard
- `/dashboard/e-ferfar/` → E-Ferfar dashboard (placeholder)
- `/dashboard/e-ferfar-2/` → E-Ferfar 2 dashboard (placeholder)
- `/dashboard/e-chavdi/` → E-Chavdi dashboard (placeholder)
- `/dashboard/agristack/` → AgriStack dashboard

### View Functions (`dashboards/views.py`)
1. **`dashboard_home()`** - Home page
2. **`pandhar_raste_dashboard()`** - Pandhar Raste with KPIs, charts, table
3. **`e_haqq_dashboard()`** - E-Haqq with application stats & charts
4. **`e_ferfar_dashboard()`** - Placeholder
5. **`e_ferfar_2_dashboard()`** - Placeholder
6. **`e_chavdi_dashboard()`** - Placeholder
7. **`agristack_dashboard()`** - AgriStack with farmer ID stats & charts

---

## 🔧 Services Layer

### `dashboards/services/pandhar_raste_service.py`
- **`get_pandhar_raste_kpis()`** - Calculate total KPIs (sums all talukas)
- **`get_pandhar_raste_chart_data()`** - Prepare chart data for 4 charts
- **`get_pandhar_raste_table_data()`** - Get QuerySet for table display

### `data_ingestion/services/excel_importer.py`
- **`import_pandhar_raste_excel()`** - Import PandharRaste from Excel
- **`import_e_haqq_excel()`** - Import EHaqq from Excel
- **`import_agristack_excel()`** - Import AgriStack from Excel
- **`validate_excel_format()`** - Validate Excel file structure
- **`ExcelImportError`** - Custom exception class

**Features**:
- Reads `.xlsx` and `.xlsm` files
- Supports custom sheet names and header rows
- Update existing records or skip duplicates
- Error handling and validation
- Transaction support (atomic imports)

---

## 🎨 Templates

### Base Template
- `dashboards/templates/dashboards/base.html` - Base layout with sidebar

### Dashboard Templates
- `home.html` - Dashboard home
- `pandhar_raste.html` - Pandhar Raste dashboard (4 charts + table)
- `e_haqq.html` - E-Haqq dashboard (multiple charts + table)
- `agristack.html` - AgriStack dashboard (charts + table)
- `e_ferfar.html`, `e_ferfar_2.html`, `e_chavdi.html` - Placeholders

### Admin Templates
- `admin/import_excel.html` - PandharRaste Excel import form
- `admin/import_e_haqq_excel.html` - EHaqq Excel import form
- `admin/import_agristack_excel.html` - AgriStack Excel import form

---

## ⚙️ Django Admin

### Admin Classes (`dashboards/admin.py`)

1. **PandharRasteAdmin**
   - List display: taluka, geo_tag_roads, geo_tag_length_km, cleared_roads, cleared_length_km, farmers_benefited
   - Search: taluka
   - Custom action: "Import from Excel file"
   - Custom URL: `/admin/dashboards/pandharraste/import-excel/`

2. **EHaqqAdmin**
   - List display: taluka, total_applications, approved_applications, rejected_applications, pending_applications, approved_percentage, period_work_count
   - Search: taluka
   - Custom action: "Import from Excel file"
   - Custom URL: `/admin/dashboards/ehaqq/import-excel/`

3. **AgriStackAdmin**
   - List display: taluka, total_villages, total_farmers, farmers_with_id_created, farmers_pending_id, completion_percentage
   - Search: taluka
   - Custom action: "Import from Excel file"
   - Custom URL: `/admin/dashboards/agristack/import-excel/`

**Admin Features**:
- Excel file upload via web interface
- File validation (.xlsx, .xlsm only)
- Update existing or skip duplicates
- Success/error messages
- Redirects to changelist after import

---

## 📊 Data Flow

### Excel Import Flow
1. User uploads Excel file via Django admin
2. File saved temporarily
3. `validate_excel_format()` checks file structure
4. `import_*_excel()` parses Excel using `openpyxl`
5. Data validated and mapped to model fields
6. Records created/updated in database (transaction)
7. Success/error messages displayed
8. Temp file deleted

### Dashboard Display Flow
1. User visits dashboard URL
2. View function called
3. Service functions fetch/calculate data:
   - KPIs (aggregations)
   - Chart data (taluka-wise lists)
   - Table data (QuerySet)
4. Data serialized to JSON for JavaScript charts
5. Template rendered with context
6. Charts rendered using Chart.js (client-side)

---

## 🗃️ Database Configuration

### Current Setup
- **Engine**: PostgreSQL (`django.db.backends.postgresql`)
- **Connection**: Via `.env` file using `python-decouple`
- **Environment Variables**:
  - `DB_NAME` - Database name (default: `collector_dashboard_db`)
  - `DB_USER` - PostgreSQL user (default: `postgres`)
  - `DB_PASSWORD` - PostgreSQL password
  - `DB_HOST` - Host (default: `localhost`)
  - `DB_PORT` - Port (default: `5432`)

### Migration Status
- ✅ Migrated from SQLite to PostgreSQL
- ✅ All data migrated (83 objects)
- ✅ Migrations applied

---

## 📦 Dependencies

### Core
- `Django>=5.2.9` - Web framework
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `python-decouple>=3.8` - Environment variables

### Excel Processing
- `openpyxl>=3.1.0` - Excel file reading/writing
- `pandas>=2.0.0` - Data manipulation (if needed)

### Utilities
- `python-dateutil>=2.8.0` - Date parsing

---

## 🎯 Key Features

1. **Multi-Scheme Dashboards**: 3 active dashboards (PandharRaste, E-Haqq, AgriStack)
2. **Excel Import**: Bulk import via Django admin
3. **Data Visualization**: Chart.js charts (bar, line, donut)
4. **Marathi Support**: Marathi field names and labels
5. **Taluka-Wise Aggregation**: Data organized by taluka (administrative division)
6. **KPI Calculations**: Automatic totals and percentages
7. **Responsive UI**: Bootstrap-based layout

---

## 🔄 Management Commands

### Excel Import Commands
- `python manage.py import_pandhar_raste <file_path>`
- `python manage.py import_e_haqq <file_path>`
- `python manage.py import_agristack <file_path>`

---

## 📝 Notes

- **Placeholder Dashboards**: E-Ferfar, E-Ferfar 2, E-Chavdi are placeholders
- **Users App**: Currently empty/placeholder
- **Static Files**: Not configured (development mode)
- **Media Files**: Not configured
- **Authentication**: Standard Django auth (no custom user model)

---

## 🚀 Deployment Ready

- ✅ PostgreSQL configured
- ✅ Environment variables via `.env`
- ✅ Database migrations applied
- ✅ Data migrated successfully
- ⚠️ Production settings needed (DEBUG=False, ALLOWED_HOSTS, static files)

---

**Last Updated**: After PostgreSQL migration
**Database**: PostgreSQL (collector_dashboard_db)
**Records**: 16 PandharRaste, 14 EHaqq, 13 AgriStack

