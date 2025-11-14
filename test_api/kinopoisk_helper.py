import requests

class KinopoiskAPITester:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers.copy()

    def search_movie(self, params, use_token=True):
        if not use_token:
            self.headers.pop('X-API-KEY', None)
            
        response = requests.get(self.base_url, params=params, headers=self.headers)
        return response.json(), response.status_code

    def check_status_code(self, actual_code, expected_code):
        return actual_code == expected_code

    def verify_movies_found(self, movies_data, expected_count):
        return len(movies_data['docs']) >= expected_count

    def find_movie_by_title(self, movie_title, movies_data):
        for movie in movies_data['docs']:
            if movie_title.lower() in movie['name'].lower():
                return True
        return False
    