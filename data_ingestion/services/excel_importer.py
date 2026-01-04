"""
Excel import service for dashboard data.
Handles reading Excel files and importing into database.
"""
import openpyxl
from django.db import transaction
from dashboards.models import PandharRaste, EHaqq, AgriStack


class ExcelImportError(Exception):
    """Custom exception for Excel import errors"""
    pass


def import_pandhar_raste_excel(file_path, sheet_name=None, header_row=1, update_existing=True):
    """
    Import PandharRaste data from Excel file.
    
    Expected Excel format:
    - Row 1: Headers (will be skipped)
    - Row 2+: Data rows with columns:
        Column A: अ.क्र. (Serial Number) - SKIPPED
        Column B: Taluka name
        Column C: अतिक्रमित व Geo-tag केलेले रस्ते (Geo-tag Roads count)
        Column D: अतिक्रमित व Geo-tag रस्त्यांची लांबी (Geo-tag Length in km)
        Column E: अतिक्रमण काढलेले रस्ते (Cleared Roads count)
        Column F: अतिक्रमण काढलेल्या रस्त्यांची लांबी (Cleared Length in km)
        Column G: लाभ झालेल्या शेतकऱ्यांची संख्या (Farmers Benefited count)
        Column H: शेरा (Remarks) - SKIPPED
    
    Args:
        file_path (str): Path to Excel file (.xlsx)
        sheet_name (str, optional): Name of sheet to read. If None, reads first sheet.
        header_row (int): Row number containing headers (1-indexed). Default is 1.
        update_existing (bool): If True, update existing records. If False, skip duplicates.
    
    Returns:
        dict: {
            'success': int,  # Number of records imported/updated
            'skipped': int,   # Number of records skipped
            'errors': list    # List of error messages
        }
    """
    errors = []
    success_count = 0
    skipped_count = 0
    
    try:
        # Open Excel workbook
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        
        # Get sheet (first sheet if not specified)
        if sheet_name:
            sheet = workbook[sheet_name]
        else:
            sheet = workbook.active
        
        # Start database transaction
        with transaction.atomic():
            # Iterate through rows (skip header row)
            for row_num, row in enumerate(sheet.iter_rows(min_row=header_row + 1, values_only=True), start=header_row + 1):
                # Skip empty rows
                if not row or not any(row):
                    continue
                
                try:
                    # Extract data from row
                    # Column A (row[0]): Serial Number - SKIP
                    # Column B (row[1]): Taluka name
                    # Column C (row[2]): Geo-tag Roads
                    # Column D (row[3]): Geo-tag Length - SKIP (not in model)
                    # Column E (row[4]): Cleared Roads
                    # Column F (row[5]): Cleared Length
                    # Column G (row[6]): Farmers Benefited
                    # Column H (row[7]): Remarks - SKIP
                    
                    # Extract taluka from Column B (index 1)
                    taluka = str(row[1]).strip() if len(row) > 1 and row[1] else None
                    
                    # Validate taluka name
                    if not taluka or taluka.lower() in ['', 'none', 'null', 'nan']:
                        # Skip if serial number is in taluka column (header row might be included)
                        if len(row) > 0 and str(row[0]).strip().lower() in ['अ.क्र.', 'sr. no.', 'serial no.', 'serial number', '1', '2', '3']:
                            continue  # Likely header row, skip silently
                        errors.append(f"Row {row_num}: Missing taluka name")
                        continue
                    
                    # Extract numeric values (handle None, empty strings, etc.)
                    # Column C (index 2): Geo-tag Roads
                    try:
                        geo_tag_roads = int(row[2]) if len(row) > 2 and row[2] is not None else 0
                    except (ValueError, TypeError):
                        geo_tag_roads = 0
                    
                    # Column D (index 3): Geo-tag Length
                    try:
                        geo_tag_length_km = float(row[3]) if len(row) > 3 and row[3] is not None else 0.0
                    except (ValueError, TypeError):
                        geo_tag_length_km = 0.0
                    
                    # Column E (index 4): Cleared Roads
                    try:
                        cleared_roads = int(row[4]) if len(row) > 4 and row[4] is not None else 0
                    except (ValueError, TypeError):
                        cleared_roads = 0
                    
                    # Column F (index 5): Cleared Length
                    try:
                        cleared_length_km = float(row[5]) if len(row) > 5 and row[5] is not None else 0.0
                    except (ValueError, TypeError):
                        cleared_length_km = 0.0
                    
                    # Column G (index 6): Farmers Benefited
                    try:
                        farmers_benefited = int(row[6]) if len(row) > 6 and row[6] is not None else 0
                    except (ValueError, TypeError):
                        farmers_benefited = 0
                    
                    # Create or update record
                    if update_existing:
                        PandharRaste.objects.update_or_create(
                            taluka=taluka,
                            defaults={
                                'geo_tag_roads': geo_tag_roads,
                                'geo_tag_length_km': geo_tag_length_km,
                                'cleared_roads': cleared_roads,
                                'cleared_length_km': cleared_length_km,
                                'farmers_benefited': farmers_benefited
                            }
                        )
                        success_count += 1
                    else:
                        # Only create if doesn't exist
                        obj, created = PandharRaste.objects.get_or_create(
                            taluka=taluka,
                            defaults={
                                'geo_tag_roads': geo_tag_roads,
                                'geo_tag_length_km': geo_tag_length_km,
                                'cleared_roads': cleared_roads,
                                'cleared_length_km': cleared_length_km,
                                'farmers_benefited': farmers_benefited
                            }
                        )
                        if created:
                            success_count += 1
                        else:
                            skipped_count += 1
                            errors.append(f"Row {row_num}: Taluka '{taluka}' already exists (skipped)")
                
                except Exception as e:
                    errors.append(f"Row {row_num}: Error processing row - {str(e)}")
                    continue
        
        workbook.close()
        
        return {
            'success': success_count,
            'skipped': skipped_count,
            'errors': errors
        }
    
    except FileNotFoundError:
        raise ExcelImportError(f"File not found: {file_path}")
    except openpyxl.utils.exceptions.InvalidFileException:
        raise ExcelImportError(f"Invalid Excel file: {file_path}")
    except Exception as e:
        raise ExcelImportError(f"Error reading Excel file: {str(e)}")


def validate_excel_format(file_path):
    """
    Validate that Excel file has the expected format.
    
    Args:
        file_path (str): Path to Excel file
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
        
        # Check if sheet has data
        if sheet.max_row < 2:
            return False, "Excel file must have at least 2 rows (header + data)"
        
        # Check if first row has data
        first_row = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]
        if not any(first_row):
            return False, "First row appears to be empty"
        
        workbook.close()
        return True, "File format looks valid"
    
    except Exception as e:
        return False, f"Error validating file: {str(e)}"


def import_e_haqq_excel(file_path, sheet_name=None, header_row=1, update_existing=True):
    """
    Import EHaqq data from Excel file.
    
    Expected Excel format:
    - Row 1: Headers (will be skipped)
    - Row 2+: Data rows with columns:
        Column A: अ.क्र. (Serial Number) - SKIPPED
        Column B: तालुका (Taluka name)
        Column C: एकूण अर्ज (Total Applications)
        Column D: स्वीकारित अर्ज (Approved Applications)
        Column E: अस्वीकारित अर्ज (Rejected Applications)
        Column F: प्रलंबित अर्ज (Pending Applications)
        Column G: स्वीकारित अर्ज (%) (Approved Percentage)
        Column H: अस्वीकारित अर्ज (%) (Rejected Percentage)
        Column I: प्रलंबित अर्ज (%) (Pending Percentage)
        Column J: 28.10.2025 ते 03.11.2025 कालावधीतील कामकाज (Period Work Count)
    
    Args:
        file_path (str): Path to Excel file (.xlsx)
        sheet_name (str, optional): Name of sheet to read. If None, reads first sheet.
        header_row (int): Row number containing headers (1-indexed). Default is 1.
        update_existing (bool): If True, update existing records. If False, skip duplicates.
    
    Returns:
        dict: {
            'success': int,  # Number of records imported/updated
            'skipped': int,   # Number of records skipped
            'errors': list    # List of error messages
        }
    """
    errors = []
    success_count = 0
    skipped_count = 0
    
    try:
        # Open Excel workbook
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        
        # Get sheet (first sheet if not specified)
        if sheet_name:
            sheet = workbook[sheet_name]
        else:
            sheet = workbook.active
        
        # Start database transaction
        with transaction.atomic():
            # Iterate through rows (skip header row)
            for row_num, row in enumerate(sheet.iter_rows(min_row=header_row + 1, values_only=True), start=header_row + 1):
                # Skip empty rows
                if not row or not any(row):
                    continue
                
                try:
                    # Extract data from row
                    # Column A (row[0]): Serial Number - SKIP
                    # Column B (row[1]): Taluka name
                    # Column C (row[2]): Total Applications
                    # Column D (row[3]): Approved Applications
                    # Column E (row[4]): Rejected Applications
                    # Column F (row[5]): Pending Applications
                    # Column G (row[6]): Approved Percentage
                    # Column H (row[7]): Rejected Percentage
                    # Column I (row[8]): Pending Percentage
                    # Column J (row[9]): Period Work Count
                    
                    # Extract taluka from Column B (index 1)
                    taluka = str(row[1]).strip() if len(row) > 1 and row[1] else None
                    
                    # Validate taluka name
                    if not taluka or taluka.lower() in ['', 'none', 'null', 'nan']:
                        # Skip if serial number is in taluka column (header row might be included)
                        if len(row) > 0 and str(row[0]).strip().lower() in ['अ.क्र.', 'sr. no.', 'serial no.', 'serial number', '1', '2', '3']:
                            continue  # Likely header row, skip silently
                        errors.append(f"Row {row_num}: Missing taluka name")
                        continue
                    
                    # Extract numeric values (handle None, empty strings, etc.)
                    # Column C (index 2): Total Applications
                    try:
                        total_applications = int(row[2]) if len(row) > 2 and row[2] is not None else 0
                    except (ValueError, TypeError):
                        total_applications = 0
                    
                    # Column D (index 3): Approved Applications
                    try:
                        approved_applications = int(row[3]) if len(row) > 3 and row[3] is not None else 0
                    except (ValueError, TypeError):
                        approved_applications = 0
                    
                    # Column E (index 4): Rejected Applications
                    try:
                        rejected_applications = int(row[4]) if len(row) > 4 and row[4] is not None else 0
                    except (ValueError, TypeError):
                        rejected_applications = 0
                    
                    # Column F (index 5): Pending Applications
                    try:
                        pending_applications = int(row[5]) if len(row) > 5 and row[5] is not None else 0
                    except (ValueError, TypeError):
                        pending_applications = 0
                    
                    # Column G (index 6): Approved Percentage
                    try:
                        approved_percentage = float(row[6]) if len(row) > 6 and row[6] is not None else 0.0
                    except (ValueError, TypeError):
                        approved_percentage = 0.0
                    
                    # Column H (index 7): Rejected Percentage
                    try:
                        rejected_percentage = float(row[7]) if len(row) > 7 and row[7] is not None else 0.0
                    except (ValueError, TypeError):
                        rejected_percentage = 0.0
                    
                    # Column I (index 8): Pending Percentage
                    try:
                        pending_percentage = float(row[8]) if len(row) > 8 and row[8] is not None else 0.0
                    except (ValueError, TypeError):
                        pending_percentage = 0.0
                    
                    # Column J (index 9): Period Work Count
                    try:
                        period_work_count = int(row[9]) if len(row) > 9 and row[9] is not None else 0
                    except (ValueError, TypeError):
                        period_work_count = 0
                    
                    # Create or update record
                    if update_existing:
                        EHaqq.objects.update_or_create(
                            taluka=taluka,
                            defaults={
                                'total_applications': total_applications,
                                'approved_applications': approved_applications,
                                'rejected_applications': rejected_applications,
                                'pending_applications': pending_applications,
                                'approved_percentage': round(approved_percentage, 2),
                                'rejected_percentage': round(rejected_percentage, 2),
                                'pending_percentage': round(pending_percentage, 2),
                                'period_work_count': period_work_count
                            }
                        )
                        success_count += 1
                    else:
                        # Only create if doesn't exist
                        obj, created = EHaqq.objects.get_or_create(
                            taluka=taluka,
                            defaults={
                                'total_applications': total_applications,
                                'approved_applications': approved_applications,
                                'rejected_applications': rejected_applications,
                                'pending_applications': pending_applications,
                                'approved_percentage': round(approved_percentage, 2),
                                'rejected_percentage': round(rejected_percentage, 2),
                                'pending_percentage': round(pending_percentage, 2),
                                'period_work_count': period_work_count
                            }
                        )
                        if created:
                            success_count += 1
                        else:
                            skipped_count += 1
                            errors.append(f"Row {row_num}: Taluka '{taluka}' already exists (skipped)")
                
                except Exception as e:
                    errors.append(f"Row {row_num}: Error processing row - {str(e)}")
                    continue
        
        workbook.close()
        
        return {
            'success': success_count,
            'skipped': skipped_count,
            'errors': errors
        }
    
    except FileNotFoundError:
        raise ExcelImportError(f"File not found: {file_path}")
    except openpyxl.utils.exceptions.InvalidFileException:
        raise ExcelImportError(f"Invalid Excel file: {file_path}")
    except Exception as e:
        raise ExcelImportError(f"Error reading Excel file: {str(e)}")


def import_agristack_excel(file_path, sheet_name=None, header_row=1, update_existing=True):
    """
    Import AgriStack data from Excel file.
    
    Expected Excel format:
    - Row 1: Headers (will be skipped)
    - Row 2+: Data rows with columns:
        Column A: अ.क्र. (Serial Number) - SKIPPED
        Column B: तालुका (Taluka name)
        Column C: एकूण गावे (Total Villages)
        Column D: एकूण शेतकरी (Total Farmers)
        Column E: फार्मर आयडी तयार केलेले शेतकरी (Farmers with ID created)
        Column F: फार्मर आयडी तयार करण्यावर शिल्लक शेतकरी (Farmers pending ID)
        Column G: टक्केवारी (Completion Percentage)
    
    Args:
        file_path (str): Path to Excel file (.xlsx)
        sheet_name (str, optional): Name of sheet to read. If None, reads first sheet.
        header_row (int): Row number containing headers (1-indexed). Default is 1.
        update_existing (bool): If True, update existing records. If False, skip duplicates.
    
    Returns:
        dict: {
            'success': int,  # Number of records imported/updated
            'skipped': int,   # Number of records skipped
            'errors': list    # List of error messages
        }
    """
    errors = []
    success_count = 0
    skipped_count = 0
    
    try:
        # Open Excel workbook
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        
        # Get sheet (first sheet if not specified)
        if sheet_name:
            sheet = workbook[sheet_name]
        else:
            sheet = workbook.active
        
        # Start database transaction
        with transaction.atomic():
            # Iterate through rows (skip header row)
            for row_num, row in enumerate(sheet.iter_rows(min_row=header_row + 1, values_only=True), start=header_row + 1):
                # Skip empty rows
                if not row or not any(row):
                    continue
                
                try:
                    # Extract data from row
                    # Column A (row[0]): Serial Number - SKIP
                    # Column B (row[1]): Taluka name
                    # Column C (row[2]): Total Villages
                    # Column D (row[3]): Total Farmers
                    # Column E (row[4]): Farmers with ID created
                    # Column F (row[5]): Farmers pending ID
                    # Column G (row[6]): Completion Percentage
                    
                    # Extract taluka from Column B (index 1)
                    taluka = str(row[1]).strip() if len(row) > 1 and row[1] else None
                    
                    # Validate taluka name
                    if not taluka or taluka.lower() in ['', 'none', 'null', 'nan']:
                        # Skip if serial number is in taluka column (header row might be included)
                        if len(row) > 0 and str(row[0]).strip().lower() in ['अ.क्र.', 'sr. no.', 'serial no.', 'serial number', '1', '2', '3']:
                            continue  # Likely header row, skip silently
                        errors.append(f"Row {row_num}: Missing taluka name")
                        continue
                    
                    # Extract numeric values (handle None, empty strings, etc.)
                    # Column C (index 2): Total Villages
                    try:
                        total_villages = int(row[2]) if len(row) > 2 and row[2] is not None else 0
                    except (ValueError, TypeError):
                        total_villages = 0
                    
                    # Column D (index 3): Total Farmers
                    try:
                        total_farmers = int(row[3]) if len(row) > 3 and row[3] is not None else 0
                    except (ValueError, TypeError):
                        total_farmers = 0
                    
                    # Column E (index 4): Farmers with ID created
                    try:
                        farmers_with_id_created = int(row[4]) if len(row) > 4 and row[4] is not None else 0
                    except (ValueError, TypeError):
                        farmers_with_id_created = 0
                    
                    # Column F (index 5): Farmers pending ID
                    try:
                        farmers_pending_id = int(row[5]) if len(row) > 5 and row[5] is not None else 0
                    except (ValueError, TypeError):
                        farmers_pending_id = 0
                    
                    # Column G (index 6): Completion Percentage
                    try:
                        completion_percentage = float(row[6]) if len(row) > 6 and row[6] is not None else 0.0
                    except (ValueError, TypeError):
                        completion_percentage = 0.0
                    
                    # Create or update record
                    if update_existing:
                        AgriStack.objects.update_or_create(
                            taluka=taluka,
                            defaults={
                                'total_villages': total_villages,
                                'total_farmers': total_farmers,
                                'farmers_with_id_created': farmers_with_id_created,
                                'farmers_pending_id': farmers_pending_id,
                                'completion_percentage': round(completion_percentage, 2)
                            }
                        )
                        success_count += 1
                    else:
                        # Only create if doesn't exist
                        obj, created = AgriStack.objects.get_or_create(
                            taluka=taluka,
                            defaults={
                                'total_villages': total_villages,
                                'total_farmers': total_farmers,
                                'farmers_with_id_created': farmers_with_id_created,
                                'farmers_pending_id': farmers_pending_id,
                                'completion_percentage': round(completion_percentage, 2)
                            }
                        )
                        if created:
                            success_count += 1
                        else:
                            skipped_count += 1
                            errors.append(f"Row {row_num}: Taluka '{taluka}' already exists (skipped)")
                
                except Exception as e:
                    errors.append(f"Row {row_num}: Error processing row - {str(e)}")
                    continue
        
        workbook.close()
        
        return {
            'success': success_count,
            'skipped': skipped_count,
            'errors': errors
        }
    
    except FileNotFoundError:
        raise ExcelImportError(f"File not found: {file_path}")
    except openpyxl.utils.exceptions.InvalidFileException:
        raise ExcelImportError(f"Invalid Excel file: {file_path}")
    except Exception as e:
        raise ExcelImportError(f"Error reading Excel file: {str(e)}")

