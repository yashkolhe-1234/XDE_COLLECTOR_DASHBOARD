"""
Django management command to import EHaqq data from Excel file.

Usage:
    python manage.py import_e_haqq /path/to/file.xlsx
    python manage.py import_e_haqq /path/to/file.xlsx --sheet "Sheet1"
    python manage.py import_e_haqq /path/to/file.xlsx --no-update
    python manage.py import_e_haqq /path/to/file.xlsx --validate-only
"""
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from data_ingestion.services.excel_importer import (
    import_e_haqq_excel,
    validate_excel_format,
    ExcelImportError
)


class Command(BaseCommand):
    help = 'Import ई-हक्क (EHaqq) data from Excel file (.xlsx)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to Excel file (.xlsx)'
        )
        parser.add_argument(
            '--sheet',
            type=str,
            default=None,
            help='Name of sheet to import (default: first sheet)'
        )
        parser.add_argument(
            '--header-row',
            type=int,
            default=1,
            help='Row number containing headers (1-indexed, default: 1)'
        )
        parser.add_argument(
            '--no-update',
            action='store_true',
            help='Skip existing records instead of updating them'
        )
        parser.add_argument(
            '--validate-only',
            action='store_true',
            help='Only validate file format, do not import'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        sheet_name = options['sheet']
        header_row = options['header_row']
        update_existing = not options['no_update']
        validate_only = options['validate_only']

        # Convert to Path object for easier handling
        file_path = Path(file_path)

        # Check if file exists
        if not file_path.exists():
            raise CommandError(f'File not found: {file_path}')

        # Check if file is Excel
        if file_path.suffix.lower() not in ['.xlsx', '.xlsm']:
            raise CommandError(f'File must be .xlsx or .xlsm format. Got: {file_path.suffix}')

        self.stdout.write(self.style.SUCCESS(f'Processing file: {file_path}'))

        # Validate file format
        is_valid, message = validate_excel_format(str(file_path))
        if not is_valid:
            raise CommandError(f'Invalid file format: {message}')

        self.stdout.write(self.style.SUCCESS(f'✓ File format validated: {message}'))

        if validate_only:
            self.stdout.write(self.style.SUCCESS('Validation complete. Use without --validate-only to import.'))
            return

        # Import data
        try:
            self.stdout.write('Starting import...')
            result = import_e_haqq_excel(
                file_path=str(file_path),
                sheet_name=sheet_name,
                header_row=header_row,
                update_existing=update_existing
            )

            # Display results
            self.stdout.write(self.style.SUCCESS('\n' + '='*50))
            self.stdout.write(self.style.SUCCESS('Import Summary:'))
            self.stdout.write(self.style.SUCCESS('='*50))
            self.stdout.write(self.style.SUCCESS(f'✓ Successfully imported/updated: {result["success"]} records'))
            
            if result['skipped'] > 0:
                self.stdout.write(self.style.WARNING(f'⚠ Skipped: {result["skipped"]} records'))
            
            if result['errors']:
                self.stdout.write(self.style.ERROR(f'\n✗ Errors encountered: {len(result["errors"])}'))
                for error in result['errors'][:10]:  # Show first 10 errors
                    self.stdout.write(self.style.ERROR(f'  - {error}'))
                if len(result['errors']) > 10:
                    self.stdout.write(self.style.ERROR(f'  ... and {len(result["errors"]) - 10} more errors'))
            else:
                self.stdout.write(self.style.SUCCESS('✓ No errors'))
            
            self.stdout.write(self.style.SUCCESS('='*50))

        except ExcelImportError as e:
            raise CommandError(f'Import failed: {str(e)}')
        except Exception as e:
            raise CommandError(f'Unexpected error: {str(e)}')

