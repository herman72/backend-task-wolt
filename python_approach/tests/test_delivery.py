import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delivery_order_price_success():
    """
    Test successful calculation of delivery order price.
    """
    
    response = client.get(
        "/api/v1/delivery-order-price",
        params={
            "venue_slug": "home-assignment-venue-helsinki",
            "cart_value": 1500,
            "user_lat": 60.17094,
            "user_lon": 24.93087,
        },
    )
    print(response.json())
    
    # Check the response status
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    # Validate response data structure
    data = response.json()
    assert isinstance(data, dict), "Response data should be a dictionary"
    assert "total_price" in data, "Missing 'total_price' in response data"
    assert "small_order_surcharge" in data, "Missing 'small_order_surcharge' in response data"
    assert "delivery" in data, "Missing 'delivery' in response data"
    
    # Validate delivery data structure
    delivery = data["delivery"]
    assert isinstance(delivery, dict), "'delivery' should be a dictionary"
    assert "fee" in delivery and delivery["fee"] is not None, "Missing or null 'fee' in delivery data"
    assert "distance" in delivery and delivery["distance"] is not None, "Missing or null 'distance' in delivery data"
    
