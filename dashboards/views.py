from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'dashboards/home.html', {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "Dashboard",
    })


from .sidebar import SIDEBAR_ITEMS


def pandhar_raste_dashboard(request):
    import json
    from .services.pandhar_raste_service import (
        get_pandhar_raste_kpis,
        get_pandhar_raste_chart_data,
        get_pandhar_raste_table_data
    )
    
    # Get KPIs, chart data, and table data
    kpis = get_pandhar_raste_kpis()
    chart_data = get_pandhar_raste_chart_data()
    table_data = get_pandhar_raste_table_data()
    
    # Serialize chart data to JSON for safe template rendering
    chart_data_json = {
        'geo_tag_roads': {
            'labels': json.dumps(chart_data['geo_tag_roads']['labels']),
            'data': json.dumps(chart_data['geo_tag_roads']['data'])
        },
        'cleared_roads': {
            'labels': json.dumps(chart_data['cleared_roads']['labels']),
            'data': json.dumps(chart_data['cleared_roads']['data'])
        },
        'cleared_length_km': {
            'labels': json.dumps(chart_data['cleared_length_km']['labels']),
            'data': json.dumps(chart_data['cleared_length_km']['data'])
        },
        'farmers_benefited': {
            'labels': json.dumps(chart_data['farmers_benefited']['labels']),
            'data': json.dumps(chart_data['farmers_benefited']['data'])
        }
    }
    
    return render(request, "dashboards/pandhar_raste.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "पांढर रस्ते",
        "kpis": kpis,
        "chart_data": chart_data_json,
        "table_data": table_data,
    })


def e_haqq_dashboard(request):
    import json
    from .models import EHaqq
    
    # Get all taluka data
    talukas = EHaqq.objects.all().order_by('taluka')
    
    # Calculate KPIs (totals)
    kpis = {
        'total_applications': sum(t.total_applications for t in talukas),
        'approved_applications': sum(t.approved_applications for t in talukas),
        'rejected_applications': sum(t.rejected_applications for t in talukas),
        'pending_applications': sum(t.pending_applications for t in talukas),
    }
    
    # Calculate overall percentages (weighted average)
    total_all = kpis['total_applications'] or 1
    overall_approved = (kpis['approved_applications'] / total_all * 100) if total_all > 0 else 0
    overall_rejected = (kpis['rejected_applications'] / total_all * 100) if total_all > 0 else 0
    overall_pending = (kpis['pending_applications'] / total_all * 100) if total_all > 0 else 0
    
    # Prepare chart data
    labels = [t.taluka for t in talukas] if talukas.exists() else []
    approved_data = [t.approved_applications for t in talukas] if talukas.exists() else []
    rejected_data = [t.rejected_applications for t in talukas] if talukas.exists() else []
    pending_data = [t.pending_applications for t in talukas] if talukas.exists() else []
    
    # Period work data (sorted for ranking)
    period_work_data = [t.period_work_count for t in talukas] if talukas.exists() else []
    period_work_labels = [t.taluka for t in talukas] if talukas.exists() else []
    
    # Serialize chart data to JSON
    chart_data_json = {
        'labels': json.dumps(labels),
        'approved_data': json.dumps(approved_data),
        'rejected_data': json.dumps(rejected_data),
        'pending_data': json.dumps(pending_data),
        'approved_percentage': json.dumps(round(overall_approved, 2)),
        'rejected_percentage': json.dumps(round(overall_rejected, 2)),
        'pending_percentage': json.dumps(round(overall_pending, 2)),
        'period_work_data': json.dumps(period_work_data),
        'period_work_labels': json.dumps(period_work_labels),
    }
    
    return render(request, "dashboards/e_haqq.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "ई-हक्क",
        "kpis": kpis,
        "chart_data": chart_data_json,
        "table_data": talukas,
    })


def e_ferfar_dashboard(request):
    return render(request, "dashboards/e_ferfar.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "ई-फेरफार",
    })


def e_ferfar_2_dashboard(request):
    return render(request, "dashboards/e_ferfar_2.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "ई-फेरफार 2",
    })


def e_chavdi_dashboard(request):
    return render(request, "dashboards/e_chavdi.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "ई-चावडी",
    })


def agristack_dashboard(request):
    import json
    from .models import AgriStack
    
    # Get all taluka data
    talukas = AgriStack.objects.all().order_by('taluka')
    
    # Calculate KPIs (totals)
    kpis = {
        'total_villages': sum(t.total_villages for t in talukas),
        'total_farmers': sum(t.total_farmers for t in talukas),
        'farmers_with_id_created': sum(t.farmers_with_id_created for t in talukas),
        'farmers_pending_id': sum(t.farmers_pending_id for t in talukas),
    }
    
    # Prepare chart data
    labels = [t.taluka for t in talukas] if talukas.exists() else []
    farmers_with_id = [t.farmers_with_id_created for t in talukas] if talukas.exists() else []
    farmers_pending = [t.farmers_pending_id for t in talukas] if talukas.exists() else []
    total_farmers = [t.total_farmers for t in talukas] if talukas.exists() else []
    total_villages = [t.total_villages for t in talukas] if talukas.exists() else []
    completion_percentages = [t.completion_percentage for t in talukas] if talukas.exists() else []
    
    # Overall totals for donut chart
    overall_created = kpis['farmers_with_id_created']
    overall_pending = kpis['farmers_pending_id']
    
    # Serialize chart data to JSON
    chart_data_json = {
        'labels': json.dumps(labels),
        'farmers_with_id': json.dumps(farmers_with_id),
        'farmers_pending': json.dumps(farmers_pending),
        'total_farmers': json.dumps(total_farmers),
        'total_villages': json.dumps(total_villages),
        'completion_percentages': json.dumps(completion_percentages),
        'overall_created': json.dumps(overall_created),
        'overall_pending': json.dumps(overall_pending),
    }
    
    return render(request, "dashboards/agristack.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "ॲग्रीस्टॅक",
        "kpis": kpis,
        "chart_data": chart_data_json,
        "table_data": talukas,
    })


def pandhar_raste_manage(request):
    """
    Manage page for PandharRaste data (view, add, edit, delete, import).
    Requires authentication.
    """
    from django.shortcuts import redirect
    from .models import PandharRaste
    
    # Check authentication
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    # Get all taluka data
    talukas = PandharRaste.objects.all().order_by('taluka')
    
    return render(request, "dashboards/pandhar_raste_manage.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "पांढर रस्ते - डेटा व्यवस्थापन",
        "talukas": talukas,
    })


def pandhar_raste_add(request):
    """
    Add new taluka data.
    """
    from django.shortcuts import redirect
    from django.contrib import messages
    from .forms import PandharRasteForm
    
    # Check authentication
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    if request.method == 'POST':
        form = PandharRasteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'तालुका "{form.cleaned_data["taluka"]}" चा डेटा यशस्वीरित्या जोडला गेला.')
            return redirect('pandhar_raste_manage')
        else:
            messages.error(request, 'कृपया त्रुटी दुरुस्त करा.')
    else:
        form = PandharRasteForm()
    
    return render(request, "dashboards/pandhar_raste_form.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "नवीन तालुका जोडा",
        "form": form,
        "form_title": "नवीन तालुका डेटा जोडा",
    })


def pandhar_raste_edit(request, pk):
    """
    Edit existing taluka data.
    """
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from .forms import PandharRasteForm
    from .models import PandharRaste
    
    # Check authentication
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    taluka = get_object_or_404(PandharRaste, pk=pk)
    
    if request.method == 'POST':
        form = PandharRasteForm(request.POST, instance=taluka)
        if form.is_valid():
            form.save()
            messages.success(request, f'तालुका "{form.cleaned_data["taluka"]}" चा डेटा यशस्वीरित्या अपडेट केला गेला.')
            return redirect('pandhar_raste_manage')
        else:
            messages.error(request, 'कृपया त्रुटी दुरुस्त करा.')
    else:
        form = PandharRasteForm(instance=taluka)
    
    return render(request, "dashboards/pandhar_raste_form.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": f"तालुका संपादन - {taluka.taluka}",
        "form": form,
        "form_title": f"तालुका संपादन: {taluka.taluka}",
    })


def pandhar_raste_delete(request, pk):
    """
    Delete taluka data with confirmation.
    """
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from .models import PandharRaste
    
    # Check authentication
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    taluka = get_object_or_404(PandharRaste, pk=pk)
    taluka_name = taluka.taluka
    
    if request.method == 'POST':
        taluka.delete()
        messages.success(request, f'तालुका "{taluka_name}" चा डेटा यशस्वीरित्या हटवला गेला.')
        return redirect('pandhar_raste_manage')
    
    return render(request, "dashboards/pandhar_raste_delete.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": "तालुका डेटा हटवा",
        "taluka": taluka,
    })


def pandhar_raste_import(request):
    """
    Import data from Excel file.
    """
    from django.shortcuts import redirect
    from django.contrib import messages
    from data_ingestion.services.excel_importer import import_pandhar_raste_excel, ExcelImportError
    import tempfile
    import os
    
    # Check authentication
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, 'कृपया Excel फाइल निवडा.')
            return redirect('pandhar_raste_manage')
        
        excel_file = request.FILES['excel_file']
        
        # Validate file extension
        if not excel_file.name.endswith(('.xlsx', '.xlsm')):
            messages.error(request, 'फाइल .xlsx किंवा .xlsm स्वरूपात असावी.')
            return redirect('pandhar_raste_manage')
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            for chunk in excel_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        
        try:
            # Import data
            result = import_pandhar_raste_excel(
                file_path=tmp_file_path,
                sheet_name=request.POST.get('sheet_name') or None,
                header_row=int(request.POST.get('header_row', 1)),
                update_existing=True
            )
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            # Show success message
            if result['success'] > 0:
                messages.success(request, f'{result["success"]} रेकॉर्ड यशस्वीरित्या आयात केले.')
            
            if result['skipped'] > 0:
                messages.warning(request, f'{result["skipped"]} रेकॉर्ड वगळले गेले.')
            
            if result['errors']:
                error_count = len(result['errors'])
                error_preview = '\n'.join(result['errors'][:5])
                if error_count > 5:
                    error_preview += f'\n... आणि {error_count - 5} अधिक त्रुटी'
                messages.error(request, f'{error_count} त्रुटी आढळल्या:\n{error_preview}')
            
        except ExcelImportError as e:
            os.unlink(tmp_file_path)
            messages.error(request, f'आयात अयशस्वी: {str(e)}')
        except Exception as e:
            os.unlink(tmp_file_path)
            messages.error(request, f'अनपेक्षित त्रुटी: {str(e)}')
    
    return redirect('pandhar_raste_manage')


def pandhar_raste_detail(request, taluka):
    """
    Detail view for a specific taluka showing road-level data.
    """
    from django.shortcuts import get_object_or_404
    from .models import PandharRaste
    from .services.pandhar_raste_detail_service import (
        generate_road_level_data,
        calculate_insights,
        get_road_incharge_data,
        calculate_road_insights
    )
    import json
    
    # Fetch taluka summary (case-insensitive)
    taluka_summary = get_object_or_404(
        PandharRaste,
        taluka__iexact=taluka
    )
    
    # Generate road-level dummy data
    roads = generate_road_level_data(taluka_summary)
    
    # Calculate insights
    insights = calculate_insights(taluka_summary, roads)
    
    # Generate incharge data
    incharge_data = get_road_incharge_data(taluka_summary, roads)
    
    # Prepare road data with incharge assignments and insights
    roads_with_details = []
    for road in roads:
        road_id = road['road_id']
        incharge = incharge_data['assignments'].get(road_id, {})
        road_insights = calculate_road_insights(road, roads, taluka_summary)
        
        roads_with_details.append({
            **road,
            'incharge': incharge,
            'road_insights': road_insights,
        })
    
    # Serialize for JavaScript (for modal)
    roads_json = json.dumps(roads_with_details)
    
    return render(request, "dashboards/pandhar_raste_detail.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": f"पांढर रस्ते - {taluka_summary.taluka}",
        "taluka_summary": taluka_summary,
        "roads": roads_with_details,
        "roads_json": roads_json,
        "insights": insights,
    })
