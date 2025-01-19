from pydantic import BaseModel, Field

class DeliveryRequest(BaseModel):
    """
    Represents the request payload for calculating the delivery order price.

    Args:
        - venue_slug (str): The unique identifier for the venue.
        - cart_value (int): Total value of items in cents. Must be greater than 0.
        - user_lat (float): Latitude of the user's location. Must be between -90 and 90.
        - user_lon (float): Longitude of the user's location. Must be between -180 and 180.
    """
    venue_slug: str = Field(..., description="The unique identifier for the venue.")
    cart_value: int = Field(..., gt=0, description="Total value of items in cents.")
    user_lat: float = Field(..., ge=-90, le=90, description="Latitude of the user's location.")
    user_lon: float = Field(..., ge=-180, le=180, description="Longitude of the user's location.")

class DeliveryResponse(BaseModel):
    """
    Represents the response payload for the delivery order price calculation.

    Args:
        - total_price (int): The total price including cart value, delivery fee, and any surcharges.
        - small_order_surcharge (int): Additional charge for small orders below a minimum threshold.
        - cart_value (int): The value of the cart in cents.
        - delivery (dict): Details about the delivery, including fee and distance.
    """
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: dict  # Contains "fee" (int) and "distance" (int)
