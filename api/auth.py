import json

from config_reader import config
from database import db_update
import aiohttp

path_registrate = config.host_name + 'auth/users/'
path_authentication = config.host_name + 'auth/token/login/'
path_authorization = config.host_name + 'auth/users/me/'


async def registrate(*args, **kwargs):
    headers = {'Content-Type': 'application/json'}
    data = {
        'email': kwargs.get('email'),
        'password': kwargs.get('password'),
        're_password': kwargs.get('re_password'),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=path_registrate,
                headers=headers,
                data=json.dumps(data),
        ) as response:
            if response.status == 201:
                return True
            else:
                data = await response.json()
                return data


async def authorization(auth_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Token {auth_token}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=path_authorization,
                headers=headers,
        ) as response:
            if response.status == 200:
                # data = await response.json()
                return True
            else:
                data = await response.json()
                return data


async def authentication(*args, **kwargs):
    headers = {'Content-Type': 'application/json'}
    data = {
        'email': kwargs.get('email'),
        'password': kwargs.get('password'),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=path_authentication,
                headers=headers,
                data=json.dumps(data),
        ) as response:
            if response.status == 200:
                data = await response.json()
                await db_update(tg_id=kwargs.get('tg_id'), auth_token=data.get('auth_token'))
                result = await authorization(auth_token=data.get('auth_token'))
                return result
            else:
                data = await response.json()
                return data