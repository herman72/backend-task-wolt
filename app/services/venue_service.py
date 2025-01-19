import httpx
from httpx import RequestError, HTTPStatusError
from fastapi import HTTPException
from app.config import API_BASE_URL

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
            response.raise_for_status()
            return response.json()
    # Handle HTTP errors such as 404 or 500
    except HTTPStatusError as http_err:
        raise HTTPException(
            status_code=http_err.response.status_code,
            detail=f"Failed to fetch {endpoint} data for venue {venue_slug}: {http_err.response.text}",
        )
    # Handle request errors such as connection issues
    except RequestError as req_err:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while connecting to the API: {str(req_err)}",
        )