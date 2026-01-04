"""
Service for पांढर रस्ते dashboard.
Handles KPI calculations and chart data preparation.
"""
from django.db.models import Sum
from ..models import PandharRaste


def get_pandhar_raste_kpis():
    """
    Calculate total KPIs by summing all taluka-wise values.
    
    Returns:
        dict: {
            'total_geo_tag_roads': int,
            'total_cleared_roads': int,
            'total_cleared_length_km': float,
            'total_farmers_benefited': int
        }
    """
    aggregates = PandharRaste.objects.aggregate(
        total_geo_tag_roads=Sum('geo_tag_roads'),
        total_cleared_roads=Sum('cleared_roads'),
        total_cleared_length_km=Sum('cleared_length_km'),
        total_farmers_benefited=Sum('farmers_benefited')
    )
    
    # Handle None values (when no data exists)
    return {
        'total_geo_tag_roads': aggregates['total_geo_tag_roads'] or 0,
        'total_cleared_roads': aggregates['total_cleared_roads'] or 0,
        'total_cleared_length_km': round(aggregates['total_cleared_length_km'] or 0.0, 2),
        'total_farmers_benefited': aggregates['total_farmers_benefited'] or 0
    }


def get_pandhar_raste_chart_data():
    """
    Prepare chart data for all 4 charts.
    
    Returns:
        dict: {
            'geo_tag_roads': {'labels': [...], 'data': [...]},
            'cleared_roads': {'labels': [...], 'data': [...]},
            'cleared_length_km': {'labels': [...], 'data': [...]},
            'farmers_benefited': {'labels': [...], 'data': [...]}
        }
    """
    talukas = PandharRaste.objects.all().order_by('taluka')
    
    # Handle empty data gracefully
    if not talukas.exists():
        return {
            'geo_tag_roads': {'labels': [], 'data': []},
            'cleared_roads': {'labels': [], 'data': []},
            'cleared_length_km': {'labels': [], 'data': []},
            'farmers_benefited': {'labels': [], 'data': []}
        }
    
    labels = [t.taluka for t in talukas]
    
    return {
        'geo_tag_roads': {
            'labels': labels,
            'data': [t.geo_tag_roads for t in talukas]
        },
        'cleared_roads': {
            'labels': labels,
            'data': [t.cleared_roads for t in talukas]
        },
        'cleared_length_km': {
            'labels': labels,
            'data': [round(t.cleared_length_km, 2) for t in talukas]
        },
        'farmers_benefited': {
            'labels': labels,
            'data': [t.farmers_benefited for t in talukas]
        }
    }


def get_pandhar_raste_table_data():
    """
    Get all taluka-wise data for the detailed table.
    
    Returns:
        QuerySet: All PandharRaste objects ordered by taluka
    """
    return PandharRaste.objects.all().order_by('taluka')

