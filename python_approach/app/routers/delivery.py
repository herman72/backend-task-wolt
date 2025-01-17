from fastapi import APIRouter, HTTPException
from app.services.venue_service import fetch_venue_data
from app.utils.calculate_distance import calculate_distance
from python_approach.app.schemas.models import DeliveryRequest, DeliveryResponse

router = APIRouter()

@router.get("/delivery-order-price", tags=["Delivery"])
async def delivery_order_price_calculator(request_data: DeliveryRequest):
    
    try:
        
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
