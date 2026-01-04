# Excel Import Guide - पांढर रस्ते Dashboard

## 📋 Overview

This guide explains how to import data from Excel files into the पांढर रस्ते dashboard database.

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `Django` - Web framework
- `openpyxl` - Excel file reading
- `pandas` - Data processing (optional, for advanced use)

---

## 📊 Excel File Format

Your Excel file (`.xlsx`) should follow this format:

| Column A | Column B | Column C | Column D | Column E | Column F | Column G | Column H |
|----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| **अ.क्र.** | **Taluka** | **Geo-tag Roads** | **Geo-tag Length** | **Cleared Roads** | **Cleared Length (km)** | **Farmers Benefited** | **शेरा** |
| 1 | तालुका 1 | 150 | 45.2 | 120 | 45.2 | 500 | - |
| 2 | तालुका 2 | 200 | 67.8 | 180 | 67.8 | 750 | - |
| 3 | तालुका 3 | 175 | 52.3 | 150 | 52.3 | 600 | - |

### Column Mapping:
- **Column A:** अ.क्र. (Serial Number) - **SKIPPED** (not imported)
- **Column B:** Taluka name (तालुका) - **REQUIRED**
- **Column C:** अतिक्रमित व Geo-tag केलेले रस्ते (Geo-tag Roads count)
- **Column D:** अतिक्रमित व Geo-tag रस्त्यांची लांबी (Geo-tag Length) - **SKIPPED** (not in database)
- **Column E:** अतिक्रमण काढलेले रस्ते (Cleared Roads count)
- **Column F:** अतिक्रमण काढलेल्या रस्त्यांची लांबी (कि.मी.) (Cleared Length in km)
- **Column G:** लाभ झालेल्या शेतकऱ्यांची संख्या (Farmers Benefited count)
- **Column H:** शेरा (Remarks) - **SKIPPED** (not imported)

### Requirements:
- ✅ File must be `.xlsx` or `.xlsm` format
- ✅ First row should contain headers (will be skipped)
- ✅ Data starts from row 2 (or row specified in `--header-row`)
- ✅ Column B (Taluka) is required (cannot be empty)
- ✅ Numeric values can be empty (will default to 0)
- ✅ Serial number (Column A) and Remarks (Column H) are automatically skipped

---

## 🚀 Import Methods

### Method 1: Django Admin (Web Interface) - **Easiest**

1. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Go to Admin Panel:**
   - Open: `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials

3. **Navigate to पांढर रस्ते:**
   - Click on "पांढर रस्ते" in the admin panel
   - Select any records (or none)
   - From "Action" dropdown, select "Import from Excel file"
   - Click "Go"

4. **Upload Excel File:**
   - Click "Choose File" and select your `.xlsx` file
   - (Optional) Enter sheet name if not using first sheet
   - (Optional) Change header row number (default: 1)
   - Check/uncheck "Update existing records"
   - Click "Import Data"

5. **View Results:**
   - Success message will show number of records imported
   - Any errors will be displayed
   - Redirects to records list

---

### Method 2: Management Command (Command Line) - **For Automation**

#### Basic Usage:
```bash
python manage.py import_pandhar_raste /path/to/file.xlsx
```

#### Advanced Options:

**Specify Sheet Name:**
```bash
python manage.py import_pandhar_raste file.xlsx --sheet "Sheet1"
```

**Change Header Row:**
```bash
python manage.py import_pandhar_raste file.xlsx --header-row 2
```

**Skip Existing Records (Don't Update):**
```bash
python manage.py import_pandhar_raste file.xlsx --no-update
```

**Validate File Only (Don't Import):**
```bash
python manage.py import_pandhar_raste file.xlsx --validate-only
```

#### Example:
```bash
# Import from Excel file
python manage.py import_pandhar_raste C:\Users\Admin\Desktop\pandhar_raste_data.xlsx

# Output:
# Processing file: C:\Users\Admin\Desktop\pandhar_raste_data.xlsx
# ✓ File format validated: File format looks valid
# Starting import...
# ==================================================
# Import Summary:
# ==================================================
# ✓ Successfully imported/updated: 15 records
# ✓ No errors
# ==================================================
```

---

## 🔧 Import Behavior

### Update vs Create:

**Default Behavior (Update Existing):**
- If taluka already exists → **Updates** all fields
- If taluka doesn't exist → **Creates** new record

**With `--no-update` Flag:**
- If taluka already exists → **Skips** (doesn't change)
- If taluka doesn't exist → **Creates** new record

### Error Handling:

- **Empty rows** are automatically skipped
- **Invalid numeric values** default to 0
- **Missing taluka name** causes row to be skipped (error logged)
- **Database errors** are caught and reported

---

## 📝 Import Service API

If you want to use the import function in your own code:

```python
from data_ingestion.services.excel_importer import import_pandhar_raste_excel

# Import with default settings
result = import_pandhar_raste_excel('/path/to/file.xlsx')

# Import with custom options
result = import_pandhar_raste_excel(
    file_path='/path/to/file.xlsx',
    sheet_name='Sheet1',           # Optional: specific sheet
    header_row=1,                   # Row number with headers
    update_existing=True            # Update existing records
)

# Result structure:
# {
#     'success': 15,      # Number of records imported/updated
#     'skipped': 2,       # Number of records skipped
#     'errors': [...]     # List of error messages
# }
```

---

## ⚠️ Troubleshooting

### Error: "File not found"
- **Solution:** Check file path is correct
- Use absolute path: `C:\Users\...\file.xlsx`
- Or relative path from project root

### Error: "Invalid Excel file"
- **Solution:** Ensure file is `.xlsx` or `.xlsm` format
- Open file in Excel and save as `.xlsx` if needed

### Error: "Missing taluka name"
- **Solution:** Check that Column A has taluka names
- Remove empty rows
- Ensure header row is correct

### Error: "ModuleNotFoundError: No module named 'openpyxl'"
- **Solution:** Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Import shows 0 records
- **Check:** Header row number (might be wrong)
- **Check:** Sheet name (if using specific sheet)
- **Check:** Data actually starts after header row

---

## 📋 Example Excel File Structure

```
Row 1: [अ.क्र., Taluka, Geo-tag Roads, Geo-tag Length, Cleared Roads, Cleared Length, Farmers, शेरा]  ← Headers (skipped)
Row 2: [1, तालुका 1, 150, 45.2, 120, 45.2, 500, -]                                                  ← Data
Row 3: [2, तालुका 2, 200, 67.8, 180, 67.8, 750, -]                                                  ← Data
Row 4: [3, तालुका 3, 175, 52.3, 150, 52.3, 600, -]                                                  ← Data
...
```

**Note:** Serial number (Column A) and Remarks (Column H) are automatically skipped during import.

---

## ✅ Best Practices

1. **Backup Data:** Always backup database before bulk import
2. **Test First:** Use `--validate-only` to check file format
3. **Small Batches:** Import in smaller chunks for large files
4. **Check Results:** Review import summary for errors
5. **Update Strategy:** Use `--no-update` if you don't want to overwrite existing data

---

## 🔄 Workflow Example

```bash
# 1. Validate file first
python manage.py import_pandhar_raste data.xlsx --validate-only

# 2. If validation passes, import
python manage.py import_pandhar_raste data.xlsx

# 3. Check dashboard to verify data
# Visit: http://127.0.0.1:8000/dashboard/pandhar-raste/
```

---

## 📞 Support

If you encounter issues:
1. Check error messages in import summary
2. Validate Excel file format matches requirements
3. Ensure all dependencies are installed
4. Check Django logs for detailed errors

---

**End of Guide**

