from fastapi import APIRouter, HTTPException, Query
from app.services.venue_service import fetch_venue_data
from app.utils.delivery_calculations import calculate_delivery_distance, calculate_delivery_fee, calculate_surcharge
from app.schemas.models import DeliveryRequest, DeliveryResponse

router = APIRouter()

def validate_input(venue_slug: str, cart_value: int, user_lat: float, user_lon: float) -> DeliveryRequest:
    """
    Validate the input parameters for the delivery order price calculator.
    Args:
        - venue_slug (str): The slug identifying the venue.
        - cart_value (int): The value of the cart in cents.
        - user_lat (float): Latitude of the user's location.
        - user_lon (float): Longitude of the user's location.

    Raises:
        - HTTPException: If any of the required parameters are missing.

    Returns:
        - DeliveryRequest: 
    """
    if not (venue_slug and cart_value and user_lat and user_lon):
        raise HTTPException(
            status_code=400, detail="Invalid input: Provide all required query parameters."
        )
    return DeliveryRequest(
        venue_slug=venue_slug,
        cart_value=cart_value,
        user_lat=user_lat,
        user_lon=user_lon,
    )

@router.get("/delivery-order-price", tags=["Delivery"])
async def delivery_order_price_calculator(venue_slug: str = Query(None, description="The venue slug for the delivery."),
    cart_value: int = Query(None, gt=0, description="Cart value in cents."),
    user_lat: float = Query(None, ge=-90, le=90, description="User's latitude."),
    user_lon: float = Query(None, ge=-180, le=180, description="User's longitude.")) -> DeliveryResponse:
    
    """
    Calculate the delivery order price based on the given input parameters or request body.

    Args:
        - venue_slug (str): The slug identifying the venue.
        - cart_value (int): The value of the cart in cents.
        - user_lat (float): Latitude of the user's location.
        - user_lon (float): Longitude of the user's location.

    Returns:
        - DeliveryResponse: An object containing the calculated delivery fee, surcharge, and total price.

    Raises:
        - HTTPException: If input validation fails or an unexpected error occurs.
    """
    
    request_data = validate_input(venue_slug, cart_value, user_lat, user_lon)
    
    # Fetch venue data (static and dynamic)
    static_data = await fetch_venue_data(request_data.venue_slug, "static")
    dynamic_data = await fetch_venue_data(request_data.venue_slug, "dynamic")

    # Calculate delivery distance
    delivery_distance = calculate_delivery_distance(
    static_data, request_data.user_lon, request_data.user_lat
)
    # Calculate small order surcharge
    small_order_surcharge = calculate_surcharge(
    request_data.cart_value, dynamic_data
)
    # Calculate delivery fee
    delivery_fee = calculate_delivery_fee(
    delivery_distance, dynamic_data
)
    # Calculate the total price
    total_price = request_data.cart_value + small_order_surcharge + delivery_fee
    
    # Prepare the response
    response = DeliveryResponse(
        total_price=total_price,
        small_order_surcharge=small_order_surcharge,
        cart_value=request_data.cart_value,
        delivery={"fee": delivery_fee, "distance": round(delivery_distance)}
    )

    return response