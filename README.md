# Delivery Order Price Calculator

This is a FastAPI-based application that calculates delivery order prices, including delivery fees and small order surcharges, based on venue and user location details. The application fetches venue data from an external API and calculates distances using the Haversine formula.

---

## Features

- Calculate total delivery order price.
- Includes delivery fees, small order surcharges, and cart value.
- Uses FastAPI for a robust and fast web framework.
- Validates requests and responses using Pydantic models.
- Fetches external venue data for dynamic calculations.

---

## Prerequisites

- Python 3.10 or higher.
- Virtual environment for dependency management.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd <repository-folder>
   ```

2. Start the FastAPI application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Access the application in your browser or API client:
   - **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
   - **Root Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## API Endpoints

### `GET /api/v1/delivery-order-price`

#### Request Body
```json
{
  "venue_slug": "home-assignment-venue-helsinki",
  "cart_value": 1500,
  "user_lat": 60.17094,
  "user_lon": 24.93087
}
```

#### Response
```json
{
  "total_price": 1690,
  "small_order_surcharge": 0,
  "cart_value": 1500,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

#### Example Usage
Using `curl`:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/delivery-order-price" \
-H "Content-Type: application/json" \
-d '{
  "venue_slug": "home-assignment-venue-helsinki",
  "cart_value": 1500,
  "user_lat": 60.17094,
  "user_lon": 24.93087
}'
```
OR

```bash
curl http://localhost:8000/api/v1/delivery-order-price\?venue_slug\=home-assignment-venue-helsinki\&cart_value\=1000\&user_lat\=60.17094\&user_lon\=24.93087
```

---

## Project Structure

```
project-folder/
├── app/
│   ├── __init__.py
│   ├── main.py               # Entry point of the FastAPI app
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── delivery.py       # API routes for delivery calculations
│   ├── services/
│   │   ├── __init__.py
│   │   ├── venue_service.py  # Handles external API calls
│   ├── utils/
│       ├── __init__.py
│       ├── calculate_distance.py  # Distance calculation logic
├── tests/
│   ├── test_delivery.py      # Unit tests for the API
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
```

---

## Testing

1. Install `pytest` if not already installed:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   pytest
   ```

---

## Improvements

Future improvements could include:

- Adding caching for external API calls.
- Implementing advanced error logging.
- Integrating with a database for persistent storage.
- Adding more comprehensive test cases.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

