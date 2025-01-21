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

## API Usage

### Endpoint

**GET /api/v1/delivery-order-price**

### Query Parameters

| Parameter    | Type    | Description                          | Example                        |
|--------------|---------|--------------------------------------|--------------------------------|
| `venue_slug` | string  | Unique identifier for the venue      | `home-assignment-venue-helsinki` |
| `cart_value` | integer | Total value of items in the cart     | `1000`                         |
| `user_lat`   | float   | Latitude of the user's location      | `60.17094`                     |
| `user_lon`   | float   | Longitude of the user's location     | `24.93087`                     |

### Example Request

```bash
curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
```

### Example Response

```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

### Valid venue slug

Finland: `home-assignment-venue-helsinki`

Sweden: `home-assignment-venue-stockholm`

Germany: `home-assignment-venue-berlin`

Japan: `home-assignment-venue-tokyo`

---

## Project Structure

```
project-folder/
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── config.py             # Configuration settings
│   ├── routers/
│   │   ├── delivery.py       # API routes for delivery calculations
│   ├── services/
│   │   ├── venue_service.py  # Handles external API requests
│   ├── utils/
│       ├── delivery_calculations.py  # Delivery logic
├── tests/
│   ├── test_delivery.py      # Unit tests
├── requirements.txt          # Dependencies
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

