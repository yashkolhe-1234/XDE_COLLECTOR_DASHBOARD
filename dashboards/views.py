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


def pandhar_raste_detail(request, taluka):
    """
    Detail view for a specific taluka showing road-level data.
    """
    from django.shortcuts import get_object_or_404
    from .models import PandharRaste
    from .services.pandhar_raste_detail_service import (
        generate_road_level_data,
        calculate_insights
    )
    
    # Fetch taluka summary (case-insensitive)
    taluka_summary = get_object_or_404(
        PandharRaste,
        taluka__iexact=taluka
    )
    
    # Generate road-level dummy data
    roads = generate_road_level_data(taluka_summary)
    
    # Calculate insights
    insights = calculate_insights(taluka_summary, roads)
    
    return render(request, "dashboards/pandhar_raste_detail.html", {
        "sidebar_items": SIDEBAR_ITEMS,
        "page_title": f"पांढर रस्ते - {taluka_summary.taluka}",
        "taluka_summary": taluka_summary,
        "roads": roads,
        "insights": insights,
    })
