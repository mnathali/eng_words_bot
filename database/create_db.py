import nltk
from nltk.corpus import words
import sqlite3
import os
import requests, json, tqdm
from bs4 import BeautifulSoup

nltk.download('words')

main_data_base = 'main_database.db'
phrasal_verbs_link = 'https://skyeng.ru/articles/vse-sekrety-frazovyh-glagolov-v-anglijskom/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru',
    'Connection': 'keep-alive',
    'Host': 'skyeng.ru',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
}

def parse_phrasal_verbs() -> dict:
    items = []
    content = requests.get(phrasal_verbs_link, headers=headers)
    soup = BeautifulSoup(content.content, 'html.parser')
    table = soup.find('table', {'ssmarticle': ''})
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if not cells:
            continue
        cells = list(map(lambda eng, ru : (eng.text, ru.text), *cells))
        items += cells
    return dict(items)


def fill_phrasal_verbs(data_base, data: dict):
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        insert_query = 'INSERT INTO phrasal_verbs (verb, definition) VALUES (?, ?)'
        words_data = [(verb, definition) for verb, definition in data.items()]
        cursor.executemany(insert_query, words_data)
        conn.commit()

def create_phrasal_verbs_table(data_base):
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS phrasal_verbs (
                verb TEXT PRIMARY KEY,
                definition TEXT NOT NULL
            );
            '''
        cursor.execute(create_table_query)
        conn.commit()

def create_table(data_base):
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS set_of_words (
                id INTEGER PRIMARY KEY,
                word TEXT NOT NULL
            );
            '''
        cursor.execute(create_table_query)
        conn.commit()

def create_user_lang_table(data_base) -> None:
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS user_lang (
                user INTEGER PRIMARY KEY,
                lang TEXT CHECK(LENGTH(lang) = 2)
            );
            '''
        cursor.execute(create_table_query)
        conn.commit()

def create_words_table(data_base: str) -> None:
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        create_table_query = f'''
                CREATE TABLE IF NOT EXISTS all_words (
                    user_id INTEGER,
                    lang CHECK(LENGTH(lang) = 2),
                    word TEXT NOT NULL,
                    noun TEXT,
                    verb TEXT,
                    adjective TEXT,
                    adverb TEXT,
                    preposition TEXT,
                    pronoun TEXT,
                    numeral TEXT,
                    translate TEXT,
                    PRIMARY KEY (user_id, lang, word)
                );
            '''
        cursor.execute(create_table_query)
        conn.commit()    


def fill_data_table(english_words, data_base):
    with sqlite3.connect(data_base) as conn:
        cursor = conn.cursor()
        insert_query = 'INSERT INTO set_of_words (word) VALUES (?)'
        words_data = [(word,) for word in english_words]
        cursor.executemany(insert_query, words_data)
        conn.commit()

if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    db = script_path.split('/')[:-1] + ['..'] + [main_data_base]
    db = '/'.join(db)
    create_table(db)
    create_user_lang_table(db)
    english_words = set(words.words())
    # method = 'lookup'
    # lang = 'lang=en-ru'
    # drop_st = set()
    # for word in tqdm.tqdm(english_words):
    #     content = requests.get(main_link + method + "?" + YANDEX_API_KEY + "&" + lang + "&text=" + word)
    #     yandex_dict_reply = json.loads(content.content)
    #     if not yandex_dict_reply['def']:
    #         drop_st.add(word)
    # english_words -= drop_st
    create_words_table(main_data_base)
    create_phrasal_verbs_table(db)
    phrasal_verbs = parse_phrasal_verbs()
    fill_phrasal_verbs(main_data_base, phrasal_verbs)
    fill_data_table(english_words, main_data_base)
