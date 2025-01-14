from fastapi import FastAPI, Query
import httpx

app = FastAPI()

API_BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

@app.get("/api/v1/delivery-order-price")
def delivery_order_price_calculator(
    venue_slug: str = Query(..., description="Slug of the venue"),
    cart_value: int = Query(..., description="Value of the cart"),
    user_lat: float = Query(..., description="Latitude of the user"),
    user_lon: float = Query(..., description="Longitude of the user"),
):
    static_data = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/static"
    dynamic_data = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/dynamic"
    
    response = httpx.get(static_data)
    
    
    # print()
    
    return {
        "venue_slug": venue_slug,
        "cart_value": cart_value,
        "user_lat": user_lat,
        "user_lon": user_lon,
        "delivery_price": response.json(),
    }