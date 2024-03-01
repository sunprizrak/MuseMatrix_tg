import json
import aiohttp


class OpenAIController:
    path_chat_completion = 'http://127.0.0.1:8000/' + 'openai/chat_completion/'

    async def chat_completion(self, *args, **kwargs):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Token {kwargs.get('auth_token')}",
        }
        data = {'prompt': kwargs.get('prompt')}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=self.path_chat_completion,
                    headers=headers,
                    data=json.dumps(data),
            ) as response:
                if response.status == 201:
                    return True
                else:
                    data = await response.json()
                    return data

