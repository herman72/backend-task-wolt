import httpx
from fastapi import HTTPException

API_BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"

async def fetch_venue_data(venue_slug: str, endpoint: str):
    url = f"{API_BASE_URL}/{venue_slug}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch {endpoint} data for venue {venue_slug}")
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching data: {str(e)}")
