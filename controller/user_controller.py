import json
from database import db_create, db_update, db_read

import aiohttp


class UserController:
    path_registrate = 'http://127.0.0.1:8000/' + 'auth/users/'
    path_authentication = 'http://127.0.0.1:8000/' + 'auth/token/login/'
    path_authorization = 'http://127.0.0.1:8000/' + 'auth/users/me/'

    def __init__(self, tg_id):
        self.tg_id = tg_id

    async def create(self):
        await db_create(tg_id=self.tg_id)

    async def get_auth_token(self):
        auth_token = await db_read(tg_id=self.tg_id)
        return auth_token

    async def registrate(self, *args, **kwargs):
        headers = {'Content-Type': 'application/json'}
        data = {
            'email': kwargs.get('email'),
            'password': kwargs.get('password'),
            're_password': kwargs.get('re_password'),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=self.path_registrate,
                    headers=headers,
                    data=json.dumps(data),
            ) as response:
                if response.status == 201:
                    return True
                else:
                    data = await response.json()
                    return data

    async def authorization(self, auth_token):
        headers = {
             'Content-Type': 'application/json',
             'Authorization': f"Token {auth_token}",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.path_authorization,
                headers=headers,
            ) as response:
                if response.status == 200:
                    # data = await response.json()
                    return True
                else:
                    data = await response.json()
                    return data

    async def authentication(self, *args, **kwargs):
        headers = {'Content-Type': 'application/json'}
        data = {
            'email': kwargs.get('email'),
            'password': kwargs.get('password'),
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=self.path_authentication,
                    headers=headers,
                    data=json.dumps(data),
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await db_update(tg_id=self.tg_id, auth_token=data.get('auth_token'))
                    result = await self.authorization(auth_token=data.get('auth_token'))
                    return result
                else:
                    data = await response.json()
                    return data