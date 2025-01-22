import asyncio
import logging

import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_URL = "https://api.opendata.esett.com"


async def get_balance_responsible_parties(code=None, country=None, name=None):
    params = {}
    if code:
        params["code"] = code
    if country:
        params["country"] = country
    if name:
        params["name"] = name

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}/EXP01/BalanceResponsibleParties", params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return await response.text()
        except Exception as e:
            # Handle any exceptions that may occur during the request
            return {"error": str(e)}


async def ingest_data(code, country, name):
    data = await get_balance_responsible_parties(code, country, name)
    print("Retrieved Data:", data)
    return data


async def main():
    # Example test call to ingest_data
    print("Testing ingest_data function...")
    await ingest_data(code="7080005051286", country="FI", name="")


if __name__ == "__main__":
    asyncio.run(main())