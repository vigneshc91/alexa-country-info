import requests
from constants import AppConstants

class Country:
    URL = AppConstants.URL

    def info(self, name):
        req = requests.get(url=self.URL.format(name))
        data = req.json()
        return data