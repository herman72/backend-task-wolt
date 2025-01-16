from fastapi import FastAPI, HTTPException, Query
import httpx
from utils import haversine

app = FastAPI()

API_BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"


def fetch_venue_data(venue_slug: str, endpoint: str):
    url = f"{API_BASE_URL}/{venue_slug}/{endpoint}"
    response = httpx.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"failed to fetch {endpoint} data for venue {venue_slug}")
    return response.json()


@app.get("/api/v1/delivery-order-price")
def delivery_order_price_calculator(
    venue_slug: str = Query(..., description="Slug of the venue"),
    cart_value: int = Query(..., gt=0, description="Value of the cart"),
    user_lat: float = Query(..., description="Latitude of the user"),
    user_lon: float = Query(..., description="Longitude of the user"),
):
    static_data = fetch_venue_data(venue_slug, "static")
    dynamic_data = fetch_venue_data(venue_slug, "dynamic")
    
    venue_coordinates = static_data["venue_raw"]["location"]["coordinates"]
    order_minimum_no_surcharge = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
    base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
    distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
    
    
    #calculating distance
    venue_lat, venue_lon = venue_coordinates
    haversine(user_lat, user_lon, venue_lat, venue_lon)
    
    
    
    
    
    
    # print()
    
    return {
        "venue_slug": venue_slug,
        "cart_value": cart_value,
        "user_lat": user_lat,
        "user_lon": user_lon,
        "delivery_price": static_response.json(),
    }