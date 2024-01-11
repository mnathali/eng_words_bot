import requests
from translate import Translator
import random
from bs4 import BeautifulSoup

def get_example(word: str):
    page = requests.get(f'https://sentence.yourdictionary.com/{word}')
    soup = BeautifulSoup(page.content, 'html.parser')
    definitions = soup.find_all('p', class_='sentence-item__text')
    if definitions:
        sentence = random.choice(definitions)
        return sentence.text
    sentence = 'There are no examples.'
    return sentence


def translate_to(text, lang="ru") -> str:
    translator = Translator(to_lang=lang)
    translation = translator.translate(text)
    return translation

def parse_dict_item(word: str, yandex_reply: list) -> dict:
    parsed_item = {'word':[word], 'noun':[], 'verb':[], 'adjective':[], 'adverb':[],
                          'preposition':[], 'pronoun':[], 'numeral':[], 'translate':[]}
    trs = [item for sublist in yandex_reply for item in sublist['tr']]
    for one_def in trs:
        parsed_item[one_def['pos']] += [one_def['text']]
    return parsed_item
