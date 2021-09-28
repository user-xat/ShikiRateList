from source.ShikiOAuth import ShikiOAuth
import requests

class Shikimori:
    __url = r"https://shikimori.one"

    def __init__(self, access_token, refresh_token) -> None:
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.headers = {
            "User-Agent": 'ShikiRatesList',
            'Authorization': 'Bearer ' + self.access_token
        }
        self.user = self.__get('/api/users/whoami').json()

    def __get(self, req_url, params: dict = dict()) -> requests.Response:
        response = requests.get(
            url=Shikimori.__url + req_url,
            headers=self.headers,
            params=params)
        return response

    def __post(self, req_url, data: dict = dict()) -> requests.Response:
        response = requests.post(
            url=Shikimori.__url + req_url,
            headers=self.headers,
            json=data)
        return response

    def __put(self, req_url, data: dict = dict()) -> requests.Response:
        response = requests.put(
            url=Shikimori.__url + req_url,
            headers=self.headers,
            json=data)
        return response

    def __delete(self, req_url) -> requests.Response:
        response = requests.delete(
            url=Shikimori.__url + req_url,
            headers=self.headers)
        return response

    def get_user_rates(self) -> dict:
        url = f"/api/users/{self.user['id']}/anime_rates"
        params = {'limit': 1000}
        while True:
            usr_rates = self.__get(url, params)
            if usr_rates.status_code == 401:
                self.refresh_token()
            else:
                break
        return usr_rates.json()

    def post_user_rates(self, anime_id: int) -> dict:
        url = '/api/v2/user_rates'
        data = {
            'user_rate': {
                'user_id': self.user['id'],
                'target_id': int(anime_id),
                'target_type': "Anime"
            }
        }
        while True:
            usr_rates = self.__post(url, data)
            if usr_rates.status_code == 401:
                self.refresh_token()
            else:
                break
        return usr_rates.json()

    def put_user_rates(self, id: str, score:int, episodes: int) -> dict:
        url = f'/api/v2/user_rates/{id}'
        data = {
            'user_rate': {
                'score': score,
                'episodes': episodes
            }
        }
        while True:
            usr_rates = self.__put(url, data)
            if usr_rates.status_code == 401:
                self.refresh_token()
            else:
                break
        return usr_rates.json()

    def delete_user_rates(self, id: str) -> None:
        url = f'/api/v2/user_rates/{id}'
        while True:
            usr_rates = self.__delete(url)
            if usr_rates.status_code == 401:
                self.refresh_token()
            else:
                break
    
    def search_anime(self, title: str) -> dict:
        url = '/api/animes'
        params = {
            'search': title,
            'limit': 10
        }
        while True:
            anime_lst = self.__get(url, params)
            if anime_lst.status_code == 401:
                self.refresh_token()
            else:
                break
        return anime_lst.json()

    def refresh_token(self) -> None:
        tokens = ShikiOAuth.refresh_token(self.refresh_token)
        self.access_token = tokens[0]
        self.refresh_token = tokens[1]
        self.headers = {
            "User-Agent": 'ShikiRatesList',
            'Authorization': 'Bearer ' + self.access_token
        }

if __name__ == '__main__':
    pass
    #shiki = Shikimori()
    #shiki.post_user_rates('49410')
    #shiki.put_user_rates('108749539', 6, 5)
    #shiki.delete_user_rates('108749539')

    # def get_anime(self, id: int):
    # url = f'/api/animes/{id}'
    
    # anime = self.__get(url)
    # if anime.status_code == 401:
    #     self.refresh_token()
    # else:
    #     break
    # return anime.json()