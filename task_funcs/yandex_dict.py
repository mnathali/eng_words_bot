import requests, json

link = 'https://dictionary.yandex.net/api/v1/dicservice.json/'

class YandexDict:

    def __init__(self, api_key, source_lang='en', target_lang='ru') -> None:
        langs = self.get_langs(api_key=api_key)
        if not f'{source_lang}-{target_lang}' in langs:
            raise Exception('YandexDict: Unknown language')
        self.__api_key = api_key
        self.source_lang = source_lang
        self.target_lang = target_lang

    def lookup(self, word):
        content = requests.get(
            f'{link}lookup?key={self.__api_key}&lang={self.source_lang}-{self.target_lang}&text={word}'
            )
        yandex_dict_reply = json.loads(content.content)
        if (yandex_dict_reply["def"]):
            return yandex_dict_reply["def"]

    @classmethod
    def lookup_class(cls, api_key, word, source_lang='en', target_lang='ru'):
        content = requests.get(
            f'{link}lookup?key={api_key}&lang={source_lang}-{target_lang}&text={word}'
            )
        yandex_dict_reply = json.loads(content.content)
        if (yandex_dict_reply["def"]):
            return yandex_dict_reply["def"]
        
    @classmethod
    def get_langs(cls, api_key):
        response = requests.get(f'{link}getLangs?key={api_key}')
        langs = eval(response.content)
        return langs
