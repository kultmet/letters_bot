import aiohttp
import asyncio
import json

import datetime
from constants import API_HOST


async def get_letter(data:dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{API_HOST}/cover_letters/', json=data
        ) as response:
            return await response.json()


async def get_skills(data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{API_HOST}/recognize_req/', json=data
        ) as response:
            return await response.json()
        

#++++++NEW CONCEPTION+++++++++

async def recognize_req(data: dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f'{API_HOST}/recognize_req/',
            json={'text': data['text']},
            ssl=False
        ) as response:
            return await response.json()

async def get_letter2(data:dict):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(
            f'{API_HOST}/split_req/',
            json={'text': data['requirements']},
            ssl=False
        ) as response:
            fuck = await response.json()
            data['requirements'] = fuck['filtered_data']
        async with session.post(
            f'{API_HOST}/cover_letters/', json=data, ssl=False
        ) as response:
            return await response.json()


if __name__ == '__main__':
    #  print(asyncio.run(get_letter2({'company': 'Шарага', 'position': 'разраб', 'interest': 'рокетам', 'requirements': 'PostgreSQL\nPython\nKafka\nDocker\nDjango Framework\nMongoDB\nRabbitMQ\nElasticsearch\nRedis\nCelery\nNginx',})))
    # print(asyncio.run(get_skills({'text': 'PostgreSQL\nPython\nKafka\nDocker\nDjango Framework\nMongoDB\nRabbitMQ\nElasticsearch\nRedis\nCelery\nNginx',})))
    start = datetime.datetime.now()
    print(
        asyncio.run(
            get_letter(
                {
                'company': 'Шарага',
                'position': 'разраб',
                'interest': 'рокетам',
                'requirements': [
                    "Python","Kafka",
                    "Docker",
                    "Django Framework",
                    "MongoDB",
                    "RabbitMQ",
                    "Elasticsearch",
                    "Redis",
                    "Celery",
                    "Nginx"
                ]
                }
            )
        )
    )
    stop = datetime.datetime.now()
    print(stop - start)
