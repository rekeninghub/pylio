import asyncio
import aiohttp
import copy

from .constant import *

class PylioAsync():

    def __init__(self, mainapi_token):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.mainapi_token = mainapi_token

    def update_token(self, mainapi_token):
        self.mainapi_token = mainapi_token

    async def signin(self, email, password):
        headers = copy.copy(self.headers)
        headers.update({
            'Authorization': 'Bearer ' + self.mainapi_token,
        })
        data = {
            'email': email,
            'password': password
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(HELIO_LOGIN_URL, json=data) as resp:
                response = await resp.json()
                status = response.get('status', 0)
                if status == 200:
                    token = response.get('result', {}).get('user', {}).get('token', '')
                    if token:
                        return {
                            'status': 200,
                            'token': token
                        }
                elif status == 400:
                    return {
                        'status': 400,
                        'message': 'Invalid email and/or password'
                    }
                # MainAPI error
                status = response.get('net', {}).get('mainapi', {}).get('fault', {}).get('code', 0)
                if status in [900901, 900902]:
                    return {
                        'status': 401,
                        'message': 'Mainapi token has been expired'
                    }
        return {
            'status': 500,
            'message': 'Unknown error'
        }

    async def send_email(self, helio_token, to, subject='', body=''):
        headers = copy.copy(self.headers)
        headers.update({
            'Authorization': 'Bearer ' + self.mainapi_token,
        })
        data = {
            'token': helio_token,
            'to': to,
            'subject': subject,
            'body': body
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(HELIO_SENDMAIL_URL, json=data) as resp:
                response = await resp.json()
                print(response)
                status = response.get('status', 0)
                if status == 200:
                    result = response.get('result', 0)
                    if not result:
                        return {
                            'status': 403,
                            'message': 'Setup your domain first'
                        }
                    return {
                        'status': 200,
                        'message': 'Email sent',
                        'send_id': result.get('send_convid', '')
                    }
                elif status == 401:
                    return {
                        'status': 401,
                        'message': 'Helio token has been expired'
                    }
                # MainAPI error
                status = response.get('net', {}).get('mainapi', {}).get('fault', {}).get('code', 0)
                if status in [900901, 900902]:
                    return {
                        'status': 401,
                        'message': 'Mainapi token has been expired'
                    }
        return {
            'status': 500,
            'message': 'Unknown error'
        }
