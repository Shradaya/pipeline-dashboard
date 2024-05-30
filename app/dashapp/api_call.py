import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

async def fetch_data_async(endpoint, params):
    logging.debug(f"Fetching data from {endpoint} with filtered params {params}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params) as response:
                if response.status != 200:
                    error_message = f"Error {response.status}: {await response.text()}"
                    logging.error(f"Failed to fetch data from {endpoint}. {error_message}")
                    return None
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        logging.error(f"Network Error while fetching data from {endpoint}: {str(e)}")
        return None
    except asyncio.TimeoutError:
        logging.error(f"Timeout error while fetching data from {endpoint}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return None

def fetch_data(endpoint, params={}):
    return asyncio.run(fetch_data_async(endpoint, params))