"""
Service for generating dummy road-level data for PandharRaste detail page.
Generates data dynamically based on taluka summary totals.
"""
import hashlib


def generate_road_level_data(taluka_summary):
    """
    Generate dummy road-level data based on taluka summary totals.
    
    Args:
        taluka_summary: PandharRaste model instance
        
    Returns:
        list: List of dictionaries, each representing a road with:
            - road_id: str (e.g., "AMB-GEO-001")
            - road_name: str (dummy name)
            - length_km: float
            - status: str ("Cleared" or "Pending")
            - cleared_length_km: float (0.0 if pending)
            - farmers_benefited: int
    """
    taluka = taluka_summary.taluka
    geo_tag_roads = taluka_summary.geo_tag_roads
    geo_tag_length_km = taluka_summary.geo_tag_length_km
    cleared_roads = taluka_summary.cleared_roads
    cleared_length_km = taluka_summary.cleared_length_km
    farmers_benefited = taluka_summary.farmers_benefited
    
    # Generate taluka code (first 3 uppercase letters)
    taluka_code = taluka.upper()[:3] if len(taluka) >= 3 else taluka.upper().ljust(3, 'X')
    
    # Use taluka name as seed for deterministic generation
    seed = hashlib.md5(taluka.encode('utf-8')).hexdigest()
    seed_int = int(seed[:8], 16)
    
    roads = []
    
    if geo_tag_roads == 0:
        return roads
    
    # Calculate base length per road
    base_length = geo_tag_length_km / geo_tag_roads if geo_tag_roads > 0 else 0.0
    
    # Generate roads
    for i in range(1, geo_tag_roads + 1):
        road_id = f"{taluka_code}-GEO-{i:03d}"
        road_name = f"{taluka} Road {i}"
        
        # Determine status
        is_cleared = i <= cleared_roads
        status = "Cleared" if is_cleared else "Pending"
        
        # Distribute length with slight variation (deterministic based on seed)
        variation = ((seed_int + i) % 100) / 1000.0  # Small variation (0-0.1)
        length_km = base_length + variation
        
        # For cleared roads, distribute cleared length
        if is_cleared and cleared_roads > 0:
            cleared_base = cleared_length_km / cleared_roads if cleared_roads > 0 else 0.0
            cleared_variation = ((seed_int + i * 2) % 100) / 1000.0
            cleared_length_road = cleared_base + cleared_variation
        else:
            cleared_length_road = 0.0
        
        # Distribute farmers (equal distribution with small variation)
        farmers_per_road = farmers_benefited / geo_tag_roads if geo_tag_roads > 0 else 0
        farmers_variation = ((seed_int + i * 3) % 10) - 5  # -5 to +5 variation
        farmers_road = max(0, int(farmers_per_road + farmers_variation))
        
        roads.append({
            'road_id': road_id,
            'road_name': road_name,
            'length_km': round(length_km, 2),
            'status': status,
            'cleared_length_km': round(cleared_length_road, 2) if is_cleared else 0.0,
            'farmers_benefited': farmers_road,
        })
    
    # Adjust totals to match exactly (fix rounding errors)
    total_length = sum(r['length_km'] for r in roads)
    if total_length != geo_tag_length_km and len(roads) > 0:
        diff = geo_tag_length_km - total_length
        adjustment_per_road = diff / len(roads)
        for road in roads:
            road['length_km'] = round(road['length_km'] + adjustment_per_road, 2)
    
    total_cleared_length = sum(r['cleared_length_km'] for r in roads)
    if total_cleared_length != cleared_length_km and cleared_roads > 0:
        diff = cleared_length_km - total_cleared_length
        cleared_roads_list = [r for r in roads if r['status'] == 'Cleared']
        if cleared_roads_list:
            adjustment_per_road = diff / len(cleared_roads_list)
            for road in cleared_roads_list:
                road['cleared_length_km'] = round(road['cleared_length_km'] + adjustment_per_road, 2)
    
    total_farmers = sum(r['farmers_benefited'] for r in roads)
    if total_farmers != farmers_benefited and len(roads) > 0:
        diff = farmers_benefited - total_farmers
        # Distribute difference to first few roads
        remaining_diff = diff
        for road in roads:
            if remaining_diff == 0:
                break
            if remaining_diff > 0:
                road['farmers_benefited'] += 1
                remaining_diff -= 1
            else:
                if road['farmers_benefited'] > 0:
                    road['farmers_benefited'] -= 1
                    remaining_diff += 1
    
    return roads


def calculate_insights(taluka_summary, roads):
    """
    Calculate insights/analysis metrics for the detail page.
    
    Args:
        taluka_summary: PandharRaste model instance
        roads: List of road dictionaries
        
    Returns:
        dict: Insights with percentages and averages
    """
    geo_tag_roads = taluka_summary.geo_tag_roads
    cleared_roads = taluka_summary.cleared_roads
    geo_tag_length_km = taluka_summary.geo_tag_length_km
    farmers_benefited = taluka_summary.farmers_benefited
    
    clearance_percentage = (cleared_roads / geo_tag_roads * 100) if geo_tag_roads > 0 else 0.0
    average_road_length = (geo_tag_length_km / geo_tag_roads) if geo_tag_roads > 0 else 0.0
    average_farmers_per_road = (farmers_benefited / geo_tag_roads) if geo_tag_roads > 0 else 0.0
    cleared_length_percentage = (taluka_summary.cleared_length_km / geo_tag_length_km * 100) if geo_tag_length_km > 0 else 0.0
    
    return {
        'clearance_percentage': round(clearance_percentage, 2),
        'average_road_length': round(average_road_length, 2),
        'average_farmers_per_road': round(average_farmers_per_road, 2),
        'cleared_length_percentage': round(cleared_length_percentage, 2),
    }

