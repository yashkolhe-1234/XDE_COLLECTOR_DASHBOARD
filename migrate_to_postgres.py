"""
Automated script to migrate data from SQLite to PostgreSQL.

This script:
1. Exports data from SQLite
2. Switches to PostgreSQL
3. Imports data into PostgreSQL
4. Verifies the migration

Usage:
    python migrate_to_postgres.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Colors for terminal output (use ASCII-safe characters for Windows)
if sys.platform == 'win32':
    class Colors:
        GREEN = ''
        YELLOW = ''
        RED = ''
        BLUE = ''
        RESET = ''
        BOLD = ''
        CHECK = '[OK]'
        CROSS = '[X]'
        WARN = '[!]'
else:
    class Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        CHECK = '✓'
        CROSS = '✗'
        WARN = '⚠'

def print_step(step_num, message):
    """Print a formatted step message."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Step {step_num}:{Colors.RESET} {message}")

def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}{Colors.CHECK}{Colors.RESET} {message}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}{Colors.CROSS}{Colors.RESET} {message}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}{Colors.WARN}{Colors.RESET} {message}")

def run_command(command, description, check=True):
    """Run a shell command and handle errors."""
    print(f"  Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(description)
            return True, result.stdout
        else:
            print_error(f"{description} - {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - {str(e)}")
        return False, str(e)

def check_sqlite_exists():
    """Check if SQLite database exists."""
    sqlite_path = Path("db.sqlite3")
    if sqlite_path.exists():
        size = sqlite_path.stat().st_size
        print_success(f"SQLite database found ({size:,} bytes)")
        
        # Quick check if database has tables/data
        check_script = """
import sqlite3
import sys

try:
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    conn.close()
    
    if tables:
        print(f"Found {len(tables)} tables in SQLite database")
        for table in tables[:5]:
            print(f"  - {table[0]}")
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more")
    else:
        print("WARNING: No tables found in SQLite database")
        sys.exit(1)
except Exception as e:
    print(f"ERROR checking SQLite: {str(e)}")
    sys.exit(1)
"""
        with open("_temp_check_sqlite.py", "w", encoding='utf-8') as f:
            f.write(check_script)
        
        success, output = run_command("python _temp_check_sqlite.py", "Checking SQLite database content", check=False)
        if Path("_temp_check_sqlite.py").exists():
            Path("_temp_check_sqlite.py").unlink()
        
        if output:
            print(f"  {output.strip()}")
        
        return True
    else:
        print_warning("SQLite database not found. Nothing to migrate.")
        return False

def export_sqlite_data():
    """Export data from SQLite database."""
    print_step(1, "Exporting data from SQLite")
    
    # Check if SQLite exists
    if not check_sqlite_exists():
        return False, None
    
    # Use the standalone export script
    success, output = run_command("python export_from_sqlite.py", "Exporting data from SQLite")
    
    export_file = "data_backup.json"
    if success and Path(export_file).exists():
        file_size = Path(export_file).stat().st_size
        # Check if file has actual content (more than just [])
        with open(export_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content == '[]' or len(content) < 10:
                print_warning("Export file appears to be empty. SQLite database may not have data.")
                return False, None
        
        print_success(f"Data exported to {export_file} ({file_size:,} bytes)")
        if output:
            print(f"  {output.strip()}")
        return True, export_file
    else:
        print_error("Export file was not created or is empty")
        return False, None

def verify_postgres_connection():
    """Verify PostgreSQL connection."""
    print_step(2, "Verifying PostgreSQL connection")
    
    # Create a script to test PostgreSQL connection using Django
    test_script = """
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        if 'PostgreSQL' in version:
            print("PostgreSQL connection successful")
            print(f"Version: {version.split(',')[0]}")
            sys.exit(0)
        else:
            print(f"ERROR: Connected to wrong database type: {version}")
            sys.exit(1)
except Exception as e:
    print(f"ERROR: Cannot connect to PostgreSQL: {str(e)}")
    sys.exit(1)
"""
    
    # Write and run the test script
    with open("_temp_test_db.py", "w", encoding='utf-8') as f:
        f.write(test_script)
    
    success, output = run_command("python _temp_test_db.py", "Testing PostgreSQL connection", check=False)
    
    # Clean up
    if Path("_temp_test_db.py").exists():
        Path("_temp_test_db.py").unlink()
    
    if success:
        if output:
            print(f"  {output.strip()}")
        return True
    else:
        print_error("Cannot connect to PostgreSQL. Please check:")
        print("  - PostgreSQL service is running")
        print("  - .env file has correct credentials")
        print("  - Database 'collector_dashboard_db' exists")
        if output:
            print(f"  Error details: {output.strip()}")
        return False

def run_migrations():
    """Run migrations on PostgreSQL."""
    print_step(3, "Running migrations on PostgreSQL")
    
    success, _ = run_command("python manage.py migrate", "Creating tables in PostgreSQL")
    return success

def import_data(export_file):
    """Import data into PostgreSQL."""
    print_step(4, f"Importing data into PostgreSQL from {export_file}")
    
    if not Path(export_file).exists():
        print_error(f"Export file {export_file} not found")
        return False
    
    success, output = run_command(
        f'python manage.py loaddata {export_file}',
        "Importing data into PostgreSQL"
    )
    
    return success

def verify_data():
    """Verify that data was migrated correctly."""
    print_step(5, "Verifying migrated data")
    
    # Create a temporary Python script to check data
    verify_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboards.models import PandharRaste, EHaqq, AgriStack

print(f"PandharRaste records: {PandharRaste.objects.count()}")
print(f"EHaqq records: {EHaqq.objects.count()}")
print(f"AgriStack records: {AgriStack.objects.count()}")

total = PandharRaste.objects.count() + EHaqq.objects.count() + AgriStack.objects.count()
print(f"Total records: {total}")
"""
    
    with open("_temp_verify.py", "w") as f:
        f.write(verify_script)
    
    success, output = run_command("python _temp_verify.py", "Checking record counts")
    
    # Clean up
    if Path("_temp_verify.py").exists():
        Path("_temp_verify.py").unlink()
    
    if success:
        print("\n" + output)
        return True
    
    return False

def main():
    """Main migration function."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print("SQLite to PostgreSQL Migration Script")
    print("="*60 + Colors.RESET)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print_error("manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Export from SQLite
    success, export_file = export_sqlite_data()
    if not success or not export_file:
        print_error("Failed to export data from SQLite")
        sys.exit(1)
    
    # Step 2: Verify PostgreSQL connection
    if not verify_postgres_connection():
        print_error("PostgreSQL connection failed. Please fix the connection and try again.")
        sys.exit(1)
    
    # Step 3: Run migrations
    if not run_migrations():
        print_error("Failed to run migrations")
        sys.exit(1)
    
    # Step 4: Import data
    if not import_data(export_file):
        print_error("Failed to import data")
        sys.exit(1)
    
    # Step 5: Verify data
    if not verify_data():
        print_warning("Data verification had issues. Please check manually.")
    
    # Final message
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
    print("Migration Completed Successfully! 🎉")
    print("="*60 + Colors.RESET)
    print("\nNext steps:")
    print("  1. Test your application: python manage.py runserver")
    print("  2. Visit http://127.0.0.1:8000/admin/ to verify data")
    print("  3. Keep db.sqlite3 as a backup")
    print(f"  4. Export file saved as: {export_file} (you can delete it later)")
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Migration cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

