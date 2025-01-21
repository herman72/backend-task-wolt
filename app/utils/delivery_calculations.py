import math

from fastapi import HTTPException

def calculate_delivery_distance(static_data: dict, user_lon: float, user_lat: float) -> float:
    """
    Calculate the distance between the user's location and the venue.
    Args:
        - static_data (dict): static data for the venue
        - user_lon (float): user longitude
        - user_lat (float): use latitude

    Raises:
        - HTTPException: If the venue coordinates are missing in the static data.

    Returns:
        float: The distance between the user and the venue in meters.
    """
    try:
        venue_coords = static_data["venue_raw"]["location"]["coordinates"]
        venue_lon, venue_lat = venue_coords
        return calculate_distance(venue_lon, venue_lat, user_lon, user_lat)
    except KeyError:
        raise HTTPException(status_code=500, detail="Invalid venue coordinates in static data")


def calculate_surcharge(cart_value: int, dynamic_data: dict) -> int:
    """
    Calculate the surcharge amount based on the cart value and venue data.
    Args:
        - cart_value (int): The value of the cart in cents.
        - dynamic_data (dict): dynamic data for the venue.

    Raises:
        - HTTPException: If the delivery specs are missing in the dynamic data.

    Returns:
        - int: The surcharge amount in cents.
    """
    try:
        min_order_value = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        return max(0, abs(min_order_value - cart_value))
    except KeyError:
        raise HTTPException(status_code=500, detail="Invalid delivery specs in dynamic data")


def calculate_delivery_fee(delivery_distance: float, dynamic_data: dict) -> int:
    """
    Calculate the delivery fee based on the delivery distance and venue data.
    Args:
        - delivery_distance (float): The distance between the user and the venue in meters.
        - dynamic_data (dict): dynamic data for the venue.

    Raises:
        - HTTPException: If the delivery pricing is missing in the dynamic data.
        - HTTPException: If the delivery distance is too long.

    Returns:
        - int: The delivery fee in cents.
    """
    try:
        base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
        distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
        delivey_fee_flag = False
        for range in distance_ranges:
            if range.get("min", 0) <= delivery_distance < range.get("max", 0):
                delivey_fee = base_price + range["a"] + round(range["b"] * delivery_distance / 10)
                delivey_fee_flag = True
        
        if delivey_fee_flag:
            return delivey_fee

        raise HTTPException(status_code=400, detail="Delivery distance is too long")
    except KeyError:
        raise HTTPException(status_code=500, detail="Invalid delivery pricing in dynamic data")

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
