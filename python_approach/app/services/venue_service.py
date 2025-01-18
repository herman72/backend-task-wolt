import httpx
from fastapi import HTTPException

API_BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

async def fetch_venue_data(venue_slug: str, endpoint: str) -> dict:
    """
    Fetch data for a specific venue from the given endpoint.
    This function interacts with the Wolt API to retrieve static or dynamic data for a venue.

    Args:
        - venue_slug (str): The unique identifier for the venue.
        - endpoint (str): The specific endpoint to fetch data from (e.g., "static" or "dynamic").

    Returns:
        - dict: The JSON response from the API containing venue data.

    Raises:
        - HTTPException: If the API request fails or returns a non-200 status code.
    """
    # Construct the full URL for the API request
    url = f"{API_BASE_URL}/{venue_slug}/{endpoint}"
    try:
        # Use an asynchronous HTTP client to fetch the data
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            # Check if the response status code indicates success
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch {endpoint} data for venue {venue_slug}")
            return response.json()
        
    except httpx.RequestError as e:
        # Handle request errors such as connection issues
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching data: {str(e)}")
