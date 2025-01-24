from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
import requests_mock

class OAuthLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.callback_url = reverse('callback')
        self.profile_url = reverse('profile')
        self.logout_url = reverse('logout')

    @requests_mock.Mocker()
    def test_github_login_redirect(self, mock):
        mock.get('https://github.com/login/oauth/authorize', text='mocked response')

        # Login process
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('github.com/login/oauth/authorize', response.url)

    @patch('requests_oauthlib.OAuth2Session.fetch_token')
    @patch('requests_oauthlib.OAuth2Session.get')
    def test_github_callback(self, mock_get, mock_fetch_token):

        mock_fetch_token.return_value = {'access_token': 'mocked_access_token'}
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = {'login': 'mocked_user'}

        session = self.client.session
        session['oauth_state'] = 'mocked_state'
        session.save()

        response = self.client.get(self.callback_url, {'state': 'mocked_state', 'code': 'mocked_code'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully authenticated', response.json()['message'])

        session = self.client.session
        self.assertIn('oauth_token', session)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['login'], 'mocked_user')

    def test_logout(self):
        # Simulate a logged-in user by setting the session data
        session = self.client.session
        session['oauth_token'] = {'access_token': 'mocked_token'}
        session.save()

        # Verify the user is logged in
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

        # Perform logout
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Verify the session is cleared
        session = self.client.session
        self.assertNotIn('oauth_token', session)