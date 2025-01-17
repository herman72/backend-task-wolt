from pydantic import BaseModel, Field

class DeliveryRequest(BaseModel):
    venue_slug: str = Field(..., description="The unique identifier for the venue.")
    cart_value: int = Field(..., gt=0, description="Total value of items in cents.")
    user_lat: float = Field(..., ge=-90, le=90, description="Latitude of the user's location.")
    user_lon: float = Field(..., ge=-180, le=180, description="Longitude of the user's location.")

class DeliveryResponse(BaseModel):
    total_price: int
    small_order_surcharge: int
    cart_value: int
    delivery: dict
