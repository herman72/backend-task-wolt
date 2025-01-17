import math

def calculate_distance(lon1: float, lat1: float, 
                       lon2: float, lat2: float) -> float:
    """
    Calculate the great-circle distance between two points on the Earth.

    This function uses the Haversine formula to compute the shortest distance over the Earth's surface
    between two geographical points specified by their latitude and longitude.

    Args:
        - lon1 (float): Longitude of the first point in decimal degrees.
        - lat1 (float): Latitude of the first point in decimal degrees.
        - lon2 (float): Longitude of the second point in decimal degrees.
        - lat2 (float): Latitude of the second point in decimal degrees.

    Returns:
        - float: The distance between the two points in meters.
    """
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Apply the Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of Earth in Meters.
    radius = 6371 * 1000
    distance = radius * c

    return distance
