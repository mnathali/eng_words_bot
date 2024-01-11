import sqlite3

def check_word_presence(word: str, conn: sqlite3.Connection, table: str = 'set_of_words') -> bool:
    cursor = conn.cursor()
    select_query = f'''
            SELECT * from {table} WHERE word="{word}"
        '''
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result

def check_my_word_presence(word: str, conn: sqlite3.Connection, user_id: str, lang: str) -> bool:
    cursor = conn.cursor()
    select_query = f'''
            SELECT * from all_words WHERE word = '{word}' and user_id = {user_id} and lang = '{lang}'
        '''
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result

def fill_user_lang(user: str, conn: sqlite3.Connection, lang: str = "ru"):
    cursor = conn.cursor()
    insert_query = f'''
            INSERT INTO user_lang (user, lang) VALUES ({user}, '{lang}')
        '''
    try:
        cursor.execute(insert_query)
    except Exception as e:
        print(e)
    conn.commit()  

def get_user_lang(user: str, conn: sqlite3.Connection) -> str:
    cursor = conn.cursor()
    select_query = f'''
            SELECT * from user_lang WHERE user={user}
        '''
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result

def set_user_lang(user: str, conn: sqlite3.Connection, lang: str) -> str:
    cursor = conn.cursor()
    update_query = f'''
            UPDATE user_lang SET lang = "{lang}" WHERE user = {user}
        '''
    cursor.execute(update_query)
    conn.commit()

def add_new_word(user_id: int, word_defs: dict, conn: sqlite3.Connection, lang: str):
    cursor = conn.cursor()
    insert_query = f'''
            INSERT INTO all_words
            (user_id, lang, word, noun, verb, adjective, adverb, preposition, pronoun, numeral, translate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
    
    try:
        cursor.execute(insert_query, tuple(', '.join(piece)
                    for piece in [[str(user_id)], [lang]] + list(word_defs.values())))
    except Exception as e:
        print(e)
    conn.commit()  

def get_all_words(conn: sqlite3.Connection, table_name: str = 'set_of_words'):
    cursor = conn.cursor()
    select_query = f'''
            SELECT word from {table_name}
        '''
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result

def delete_word_from_table(user_id: str, word: str, conn: sqlite3.Connection, lang: str):
    cursor = conn.cursor()
    delete_query = f'''
            DELETE FROM all_words WHERE word = '{word}' and user_id = {user_id} and lang = '{lang}'
        '''
    try:
        cursor.execute(delete_query)
    except Exception as e:
        print(e)
    conn.commit()

def read_word(user_id: str, word: str, conn: sqlite3.Connection, lang: str) -> dict:
    cursor = conn.cursor()
    defs_dict = {'word':[], 'noun':[], 'verb':[], 'adjective':[], 'adverb':[],
            'preposition':[], 'pronoun':[], 'numeral':[], 'translate':[]}
    select_query = f'''
            SELECT word, noun, verb, adjective, adverb, preposition, pronoun, numeral, translate FROM all_words
            WHERE word = '{word}' and user_id = {user_id} and lang = '{lang}'
        '''
    try:
        cursor.execute(select_query)
        result = cursor.fetchone()
        for key, res in zip(defs_dict, result):
            if res:
                defs_dict[key].extend(res.split(', '))
    except Exception as e:
        print(e)
    conn.commit()
    return defs_dict

def get_my_words(conn: sqlite3.Connection, user_id: str, lang: str):
    cursor = conn.cursor()
    select_query = f'''
            SELECT word from all_words WHERE user_id = {user_id} and lang = '{lang}'
        '''
    cursor.execute(select_query)
    result = cursor.fetchall()
    return result
