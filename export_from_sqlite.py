"""
Standalone script to export data from SQLite.
This script temporarily uses SQLite database for export.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django with SQLite
BASE_DIR = Path(__file__).resolve().parent

# Temporarily override database to SQLite
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Override database connection to use SQLite
from django.conf import settings
from django.db import connections

# Close existing connections
connections.close_all()

# Create SQLite connection
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

# Reconnect with SQLite
connections.close_all()

# Now export data
from django.core.management import call_command
from io import StringIO

print("Exporting data from SQLite...")
output = StringIO()

try:
    call_command('dumpdata', 
                 '--exclude', 'auth.permission',
                 '--exclude', 'contenttypes',
                 '--indent', '2',
                 stdout=output)
    
    data = output.getvalue()
    
    # Write to file
    export_file = 'data_backup.json'
    with open(export_file, 'w', encoding='utf-8') as f:
        f.write(data)
    
    # Check if we got actual data
    import json
    parsed = json.loads(data)
    count = len(parsed)
    print(f"✓ Exported {count} objects to {export_file}")
    
    if count == 0:
        print("WARNING: No data found in SQLite database")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

