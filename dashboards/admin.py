from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import PandharRaste, EHaqq, AgriStack
import os
from data_ingestion.services.excel_importer import (
    import_pandhar_raste_excel,
    import_e_haqq_excel,
    import_agristack_excel,
    validate_excel_format,
    ExcelImportError
)

# Register your models here.


@admin.register(PandharRaste)
class PandharRasteAdmin(admin.ModelAdmin):
    list_display = ('taluka', 'geo_tag_roads', 'geo_tag_length_km', 'cleared_roads', 'cleared_length_km', 'farmers_benefited')
    list_filter = ('taluka',)
    search_fields = ('taluka',)
    ordering = ('taluka',)
    actions = ['import_from_excel_action']
    
    def import_from_excel_action(self, request, queryset):
        """
        Admin action to import data from Excel file.
        Redirects to upload page.
        """
        return redirect('admin:import_pandhar_raste_excel')
    
    import_from_excel_action.short_description = "Import from Excel file"
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), 
                 name='import_pandhar_raste_excel'),
        ]
        return custom_urls + urls
    
    def import_excel_view(self, request):
        """
        View for uploading and importing Excel file.
        """
        if request.method == 'POST':
            if 'excel_file' not in request.FILES:
                messages.error(request, 'Please select an Excel file.')
                return render(request, 'admin/import_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            excel_file = request.FILES['excel_file']
            
            # Validate file extension
            if not excel_file.name.endswith(('.xlsx', '.xlsm')):
                messages.error(request, 'File must be .xlsx or .xlsm format.')
                return render(request, 'admin/import_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                for chunk in excel_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            try:
                # Validate file format
                is_valid, message = validate_excel_format(tmp_file_path)
                if not is_valid:
                    messages.error(request, f'Invalid file format: {message}')
                    os.unlink(tmp_file_path)
                    return render(request, 'admin/import_excel.html', {
                        'opts': self.model._meta,
                        'has_view_permission': True,
                    })
                
                # Import data
                update_existing = request.POST.get('update_existing', 'on') == 'on'
                result = import_pandhar_raste_excel(
                    file_path=tmp_file_path,
                    sheet_name=request.POST.get('sheet_name') or None,
                    header_row=int(request.POST.get('header_row', 1)),
                    update_existing=update_existing
                )
                
                # Clean up temp file
                os.unlink(tmp_file_path)
                
                # Show success message
                if result['success'] > 0:
                    messages.success(request, 
                        f'Successfully imported {result["success"]} records.')
                
                if result['skipped'] > 0:
                    messages.warning(request, 
                        f'Skipped {result["skipped"]} existing records.')
                
                if result['errors']:
                    error_count = len(result['errors'])
                    error_preview = '\n'.join(result['errors'][:5])
                    if error_count > 5:
                        error_preview += f'\n... and {error_count - 5} more errors'
                    messages.error(request, f'Encountered {error_count} errors:\n{error_preview}')
                
                return redirect('admin:dashboards_pandharraste_changelist')
            
            except ExcelImportError as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Import failed: {str(e)}')
                return render(request, 'admin/import_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            except Exception as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Unexpected error: {str(e)}')
                return render(request, 'admin/import_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
        
        # GET request - show upload form
        return render(request, 'admin/import_excel.html', {
            'opts': self.model._meta,
            'has_view_permission': True,
        })


@admin.register(EHaqq)
class EHaqqAdmin(admin.ModelAdmin):
    list_display = ('taluka', 'total_applications', 'approved_applications', 'rejected_applications', 
                    'pending_applications', 'approved_percentage', 'period_work_count')
    list_filter = ('taluka',)
    search_fields = ('taluka',)
    ordering = ('taluka',)
    actions = ['import_from_excel_action']
    
    def import_from_excel_action(self, request, queryset):
        """
        Admin action to import data from Excel file.
        Redirects to upload page.
        """
        return redirect('admin:import_e_haqq_excel')
    
    import_from_excel_action.short_description = "Import from Excel file"
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), 
                 name='import_e_haqq_excel'),
        ]
        return custom_urls + urls
    
    def import_excel_view(self, request):
        """
        View for uploading and importing Excel file.
        """
        if request.method == 'POST':
            if 'excel_file' not in request.FILES:
                messages.error(request, 'Please select an Excel file.')
                return render(request, 'admin/import_e_haqq_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            excel_file = request.FILES['excel_file']
            
            # Validate file extension
            if not excel_file.name.endswith(('.xlsx', '.xlsm')):
                messages.error(request, 'File must be .xlsx or .xlsm format.')
                return render(request, 'admin/import_e_haqq_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                for chunk in excel_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            try:
                # Validate file format
                is_valid, message = validate_excel_format(tmp_file_path)
                if not is_valid:
                    messages.error(request, f'Invalid file format: {message}')
                    os.unlink(tmp_file_path)
                    return render(request, 'admin/import_e_haqq_excel.html', {
                        'opts': self.model._meta,
                        'has_view_permission': True,
                    })
                
                # Import data
                update_existing = request.POST.get('update_existing', 'on') == 'on'
                result = import_e_haqq_excel(
                    file_path=tmp_file_path,
                    sheet_name=request.POST.get('sheet_name') or None,
                    header_row=int(request.POST.get('header_row', 1)),
                    update_existing=update_existing
                )
                
                # Clean up temp file
                os.unlink(tmp_file_path)
                
                # Show success message
                if result['success'] > 0:
                    messages.success(request, 
                        f'Successfully imported {result["success"]} records.')
                
                if result['skipped'] > 0:
                    messages.warning(request, 
                        f'Skipped {result["skipped"]} existing records.')
                
                if result['errors']:
                    error_count = len(result['errors'])
                    error_preview = '\n'.join(result['errors'][:5])
                    if error_count > 5:
                        error_preview += f'\n... and {error_count - 5} more errors'
                    messages.error(request, f'Encountered {error_count} errors:\n{error_preview}')
                
                return redirect('admin:dashboards_ehaqq_changelist')
            
            except ExcelImportError as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Import failed: {str(e)}')
                return render(request, 'admin/import_e_haqq_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            except Exception as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Unexpected error: {str(e)}')
                return render(request, 'admin/import_e_haqq_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
        
        # GET request - show upload form
        return render(request, 'admin/import_e_haqq_excel.html', {
            'opts': self.model._meta,
            'has_view_permission': True,
        })


@admin.register(AgriStack)
class AgriStackAdmin(admin.ModelAdmin):
    list_display = ('taluka', 'total_villages', 'total_farmers', 'farmers_with_id_created', 
                    'farmers_pending_id', 'completion_percentage')
    list_filter = ('taluka',)
    search_fields = ('taluka',)
    ordering = ('taluka',)
    actions = ['import_from_excel_action']
    
    def import_from_excel_action(self, request, queryset):
        """
        Admin action to import data from Excel file.
        Redirects to upload page.
        """
        return redirect('admin:import_agristack_excel')
    
    import_from_excel_action.short_description = "Import from Excel file"
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.admin_site.admin_view(self.import_excel_view), 
                 name='import_agristack_excel'),
        ]
        return custom_urls + urls
    
    def import_excel_view(self, request):
        """
        View for uploading and importing Excel file.
        """
        if request.method == 'POST':
            if 'excel_file' not in request.FILES:
                messages.error(request, 'Please select an Excel file.')
                return render(request, 'admin/import_agristack_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            excel_file = request.FILES['excel_file']
            
            # Validate file extension
            if not excel_file.name.endswith(('.xlsx', '.xlsm')):
                messages.error(request, 'File must be .xlsx or .xlsm format.')
                return render(request, 'admin/import_agristack_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                for chunk in excel_file.chunks():
                    tmp_file.write(chunk)
                tmp_file_path = tmp_file.name
            
            try:
                # Validate file format
                is_valid, message = validate_excel_format(tmp_file_path)
                if not is_valid:
                    messages.error(request, f'Invalid file format: {message}')
                    os.unlink(tmp_file_path)
                    return render(request, 'admin/import_agristack_excel.html', {
                        'opts': self.model._meta,
                        'has_view_permission': True,
                    })
                
                # Import data
                update_existing = request.POST.get('update_existing', 'on') == 'on'
                result = import_agristack_excel(
                    file_path=tmp_file_path,
                    sheet_name=request.POST.get('sheet_name') or None,
                    header_row=int(request.POST.get('header_row', 1)),
                    update_existing=update_existing
                )
                
                # Clean up temp file
                os.unlink(tmp_file_path)
                
                # Show success message
                if result['success'] > 0:
                    messages.success(request, 
                        f'Successfully imported {result["success"]} records.')
                
                if result['skipped'] > 0:
                    messages.warning(request, 
                        f'Skipped {result["skipped"]} existing records.')
                
                if result['errors']:
                    error_count = len(result['errors'])
                    error_preview = '\n'.join(result['errors'][:5])
                    if error_count > 5:
                        error_preview += f'\n... and {error_count - 5} more errors'
                    messages.error(request, f'Encountered {error_count} errors:\n{error_preview}')
                
                return redirect('admin:dashboards_agristack_changelist')
            
            except ExcelImportError as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Import failed: {str(e)}')
                return render(request, 'admin/import_agristack_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            except Exception as e:
                os.unlink(tmp_file_path)
                messages.error(request, f'Unexpected error: {str(e)}')
                return render(request, 'admin/import_agristack_excel.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
        
        # GET request - show upload form
        return render(request, 'admin/import_agristack_excel.html', {
            'opts': self.model._meta,
            'has_view_permission': True,
        })
