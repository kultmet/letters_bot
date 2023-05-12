import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

from constants import API_HOST


async def get_letter(data: dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f'{API_HOST}/requirements/',
            json={'text': data['requirements']},
            ssl=False
        ) as response:
            fuck = await response.json()
            data['requirements'] = fuck['filtered_data']
        async with session.post(
            f'{API_HOST}/cover_letters/', json=data, ssl=False
        ) as response:
            return await response.json()


async def get_skills(endpoint):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f'{API_HOST}/{endpoint}/'
            ) as response:
                return await response.json()
        except ClientConnectorError:
            pass


async def add_skill(data: dict, endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{API_HOST}/{endpoint}/', json=data
        ) as response:
            return await response.json()
