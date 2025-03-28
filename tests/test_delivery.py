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
    
def test_delivery_order_price_invalid_distance():
    """Test handling of delivery distance exceeding the allowed range."""
    response = client.get(
        "/api/v1/delivery-order-price",
        params={
            "venue_slug": "home-assignment-venue-helsinki",
            "cart_value": 1500,
            "user_lat": 90.0,  # Extreme latitude far from the venue
            "user_lon": 135.0,
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "distance is too long" in data["detail"]
    
def test_delivery_order_price_missing_params():
    """Test API response when required parameters are missing."""
    response = client.get(
        "/api/v1/delivery-order-price",
        params={"venue_slug": "home-assignment-venue-helsinki"},
    )
    assert response.status_code == 400  # Unprocessable Entity
    data = response.json()
    assert "detail" in data