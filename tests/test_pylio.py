import asyncio
import os
import unittest
from unittest import mock

from pylio import PylioAsync


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)

def AsyncMock(*args, **kwargs):
    """Create an async function mock."""
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro

class TestPylioAsyncSignin(unittest.TestCase):
    """ Test Helio API connector module signin
        via https://mainapi.net
    """

    def setUp(self):
        # token = '52d080b97fd87107c084791d213dd1b8'
        self.mainapi_token = os.getenv('MAINAPI_TOKEN')
        self.pylio_async = PylioAsync(self.mainapi_token)
        self.user = {
            'email': os.getenv('HELIO_EMAIL'),
            'password': os.getenv('HELIO_PASSWORD')
        }

    def test_signin_success(self):
        result = _run(self.pylio_async.signin(self.user['email'], self.user['password']))
        self.assertEqual(result.get('status', 0), 200)
        self.assertIsNotNone(result.get('token', ''))

    def test_signin_invalid_email_password(self):
        result = _run(self.pylio_async.signin(self.user['email'], 'asdsad'))
        self.assertEqual(result.get('status', 0), 400)
        self.assertEqual(result.get('message', ''), 'Invalid email and/or password')

    def test_signin_token_expired(self):
        self.pylio_async.update_token('12321321232')
        result = _run(self.pylio_async.signin(self.user['email'], self.user['password']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Mainapi token has been expired')
        self.pylio_async.update_token(self.mainapi_token)

    def test_signin_token_missing(self):
        self.pylio_async.update_token('')
        result = _run(self.pylio_async.signin(self.user['email'], self.user['password']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Mainapi token has been expired')
        self.pylio_async.update_token(self.mainapi_token)

    @unittest.skip("Only default return")
    def test_signin_unknown_error(self):
        result = _run(self.pylio_async.signin(self.user['email'], self.user['password']))
        self.assertEqual(result.get('status', 0), 500)
        self.assertEqual(result.get('message', ''), 'Unknown error')


class TestPylioAsyncSendEmail(unittest.TestCase):
    """ Test Helio API connector module send_email
        via https://mainapi.net
    """

    def setUp(self):
        # token = '52d080b97fd87107c084791d213dd1b8'
        self.mainapi_token = os.getenv('MAINAPI_TOKEN')
        self.pylio_async = PylioAsync(self.mainapi_token)
        user = {
            'email': os.getenv('HELIO_EMAIL'),
            'password': os.getenv('HELIO_PASSWORD')
        }
        user_not_setup = os.getenv('HELIO_EMAIL_NOT_SETUP')
        self.helio = _run(self.pylio_async.signin(user['email'], user['password']))
        self.helio_not_setup = _run(self.pylio_async.signin(user_not_setup, user['password']))
        self.mail = {
            'to': 'coba@gmail.com',
            'subject': 'Mail subject',
            'body': 'Content of the email.'
        }

    def test_send_email_success(self):
        result = _run(self.pylio_async.send_email(self.helio['token'], self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 200)
        self.assertEqual(result.get('message', ''), 'Email sent')
        self.assertTrue(result.get('send_id', None))

    def test_send_email_forbidden(self):
        """ Forbidden when user not setup their mail server to helio.
        """
        result = _run(self.pylio_async.send_email(self.helio_not_setup['token'], self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 403)
        self.assertEqual(result.get('message', ''), 'Setup your domain first')

    def test_send_email_helio_token_expired(self):
        result = _run(self.pylio_async.send_email('helio_token', self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Helio token has been expired')

    def test_send_email_helio_token_invalid(self):
        result = _run(self.pylio_async.send_email('', self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Helio token has been expired')

    def test_send_email_mainapi_token_expired(self):
        self.pylio_async.update_token('12321321232')
        result = _run(self.pylio_async.send_email('', self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Mainapi token has been expired')
        self.pylio_async.update_token(self.mainapi_token)

    def test_send_email_mainapi_token_missing(self):
        self.pylio_async.update_token('')
        result = _run(self.pylio_async.send_email('', self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 401)
        self.assertEqual(result.get('message', ''), 'Mainapi token has been expired')
        self.pylio_async.update_token(self.mainapi_token)

    @unittest.skip("Only default return")
    def test_send_email_unknown_error(self):
        result = _run(self.pylio_async.send_email(self.helio['token'], self.mail['to'], self.mail['subject'], self.mail['body']))
        self.assertEqual(result.get('status', 0), 500)
        self.assertEqual(result.get('message', ''), 'Unknown error')
