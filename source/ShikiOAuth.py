import requests
from requests_oauthlib import OAuth2Session
import webbrowser
import json
from cryptocode import encrypt, decrypt


class ShikiOAuth:
    __client_id = r'Qrb310C4MRPAaTR0pvZbWZ2HG97KvYMKzU2Dlp9endA'
    __client_secret = r'qTN9_Y3SnaiwHQirocsiKLP6xK_PTFYRlpD5xDjt6rA'
    __redirect_uri = r'urn:ietf:wg:oauth:2.0:oob'
    __authorize_base_url = r'https://shikimori.one/oauth/authorize'
    __token_url = r'https://shikimori.one/oauth/token'
    __scope = ['user_rates']

    def __init__(self) -> None:
        self.__shiki = OAuth2Session(client_id=ShikiOAuth.__client_id, scope=ShikiOAuth.__scope, redirect_uri=ShikiOAuth.__redirect_uri)
        authorize_url, _ = self.__shiki.authorization_url(ShikiOAuth.__authorize_base_url)
        webbrowser.open_new_tab(authorize_url)

    def get_access_token(self, authorize_code: str) -> str:
        access_token = requests.post(
            url=ShikiOAuth.__token_url,
            headers={"User-Agent": "ShikiRatesList"},
            params={
                'grant_type': "authorization_code",
                'client_id': ShikiOAuth.__client_id,
                'client_secret': ShikiOAuth.__client_secret,
                'code': authorize_code,
                'redirect_uri': ShikiOAuth.__redirect_uri
            }
        )
        return access_token.json()
    
    @staticmethod
    def save_tokens(tokens: dict) -> None:
        tokens['access_token'] = encrypt(tokens['access_token'], ShikiOAuth.__client_secret)
        tokens['refresh_token'] = encrypt(tokens['refresh_token'], ShikiOAuth.__client_secret)

        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=3)

    @staticmethod
    def load_token() -> dict:
        try:
            with open('tokens.json', 'r') as file:
                tokens = json.load(file)
        except Exception:
            return None
        tokens['access_token'] = decrypt(tokens['access_token'], ShikiOAuth.__client_secret)
        tokens['refresh_token'] = decrypt(tokens['refresh_token'], ShikiOAuth.__client_secret)
        return tokens
    
    @staticmethod
    def refresh_token(refresh_token) -> tuple:
        url = ShikiOAuth.__token_url
        headers = {'User-Agent': 'ShikiRatesList'}
        params = {
            'grant_type': 'refresh_token',
            'client_id': ShikiOAuth.__client_id,
            'client_secret': ShikiOAuth.__client_secret,
            'refresh_token': refresh_token
        }
        new_tokens = requests.post(url=url, headers=headers, params=params)
        new_tokens = new_tokens.json()
        ShikiOAuth.save_tokens(new_tokens)
        return new_tokens['access_token'], new_tokens['refresh_token']

        

if __name__ == '__main__':
    # oauth = ShikiOAuth()
    # authorize_code = input()
    # ac = oauth.get_access_token(authorize_code)
    token = ShikiOAuth.load_token()

