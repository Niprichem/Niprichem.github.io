from pprint import pprint
import requests


class YMUser:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'CONTENT-Type': 'application/x-yametrika+json'
        }

    def get_counters(self):
        headers = self.get_headers()
        response = requests.get(
            'http://api-metrika.yandex.ru/management/v1/counters',
            headers=headers,  # params('pretty': 1)
        )
        return response.json()['counters']

    def get_counter_info(self, counter_id):
        headers = self.get_headers()
        response = requests.get(
            'http://api-metrika.yandex.ru/management/v1/counters/',
            {}.format(counter_id), headers=self.get_headers()
        )
        return response.json()['counters']


class Counter(YMUser):

    STAT_URL = 'http://api-metrika.yandex.ru/stat/v1/data'

    def __init__(self, id_, token):
        self.id = id_
        super().__init__(token)

    def get_visits(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()

    def get_views(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()

    def get_visitors(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:percentNewVisitors'
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()


if __name__ == '__main__':
    TOKEN = 'AQAAAAAYiShcAASt2DOBo9p4AkKrg52OlvkyhLM'
    achernyakov = YMUser(TOKEN)
    counters = achernyakov.get_counters()
    pprint(counters)
    for c in counters:
        counter = Counter(c['id'], TOKEN)
        pprint(counter.get_visits())
        pprint(counter.get_views())
        pprint(counter.get_visitors())
