from typing import Optional
from fastapi import APIRouter, Body, HTTPException, Query
from app.services.venue_service import fetch_venue_data
from app.utils.helper import calculate_distance
from app.schemas.models import DeliveryRequest, DeliveryResponse

router = APIRouter()

@router.get("/delivery-order-price", tags=["Delivery"])
async def delivery_order_price_calculator(venue_slug: str = Query(None, description="The venue slug for the delivery."),
    cart_value: int = Query(None, gt=0, description="Cart value in cents."),
    user_lat: float = Query(None, ge=-90, le=90, description="User's latitude."),
    user_lon: float = Query(None, ge=-180, le=180, description="User's longitude."),
    body: Optional[DeliveryRequest] = Body(None)):
    
    try:
        
        if body:
            request_data = body
        elif venue_slug and cart_value and user_lat and user_lon:
            request_data = DeliveryRequest(
                venue_slug=venue_slug,
                cart_value=cart_value,
                user_lat=user_lat,
                user_lon=user_lon
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid input: Either provide query parameters or a JSON body.")
        
        static_data = await fetch_venue_data(request_data.venue_slug, "static")
        dynamic_data = await fetch_venue_data(request_data.venue_slug, "dynamic")

        venue_coords = static_data["venue_raw"]["location"]["coordinates"]
        venue_lon, venue_lat = venue_coords
        delivery_distance = calculate_distance(venue_lon, venue_lat, request_data.user_lon, request_data.user_lat)

        min_order_value = dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        small_order_surcharge = max(0, min_order_value - request_data.cart_value)

        base_price = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
        distance_ranges = dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]

        delivery_fee = None
        for range in distance_ranges:
            if range["min"] <= delivery_distance < range["max"] or range["max"] == 0:
                delivery_fee = base_price + range["a"] + round(range["b"] * delivery_distance / 10)
                break

        if delivery_fee is None:
            raise HTTPException(status_code=400, detail="Delivery distance is too long")

        total_price = request_data.cart_value + small_order_surcharge + delivery_fee
        
        # Prepare the response
        response = DeliveryResponse(
            total_price=total_price,
            small_order_surcharge=small_order_surcharge,
            cart_value=request_data.cart_value,
            delivery={"fee": delivery_fee, "distance": round(delivery_distance)}
        )

        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
