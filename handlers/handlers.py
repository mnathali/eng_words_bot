from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from difflib import get_close_matches
from database.db_manipulations import *
from config import main_data_base, config
from task_funcs import *
from lexicon import replies
import sqlite3
from callbacks import create_inline_kb

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        replies['start']
    )
    with sqlite3.connect(main_data_base) as conn:
        fill_user_lang(message.from_user.id, conn)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        replies['help'],
        parse_mode=ParseMode.HTML
    )

@router.message(Command(commands='add'))
async def process_add_command(message: Message):
    word = message.text[message.text.find(' ') + 1:].lower()
    reply = "The word was added"
    with sqlite3.connect(main_data_base) as conn:
        if check_word_presence(word, conn):
            mode = get_user_lang(message.from_user.id, conn)[-1]
            yandex_reply = YandexDict.lookup_class(
                api_key=config.yandex.api_key, word=word, target_lang=mode
                )
            if (yandex_reply):
                defs_dict = parse_dict_item(word, yandex_reply)
                add_new_word(message.from_user.id, defs_dict, conn, mode)
            else:
                defs_dict = {'word':[word], 'noun':[], 'verb':[], 'adjective':[], 'adverb':[],
                          'preposition':[], 'pronoun':[], 'numeral':[], 'translate':[translate_to(word, mode)]}
                if defs_dict['translate'].lower() != word.lower():
                    add_new_word(message.from_user.id, defs_dict, conn, mode)
                    reply += 'from the translator'
                else:
                    words = get_all_words(conn)
                    closest = get_close_matches(word, map(lambda word: word[0], words))
                    reply = "Unknown word. Maybe you meant one of these: " + ', '.join(closest)
        else:
            words = get_all_words(conn)
            closest = get_close_matches(word, map(lambda word: word[0], words))
            reply = "Unknown word. Maybe you meant one of these: " + ', '.join(closest)
    await message.answer(
        reply
    )

@router.message(Command(commands='list'))
async def process_list_command(message: Message):
    reply = '<b>Your words:</b>\n\n\t'
    words = []
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(message.from_user.id, conn)[-1]
        words = get_my_words(conn, str(message.from_user.id), lang)
    buttons = {}
    reply += '\n\t'.join(map(lambda w: w[0], words[:10]))
    if len(words) > 10:
        buttons = {'page': f'1/{len(words) // 10 + (1 if len(words) % 10 else 0)}', 'right': '>>'}
    keyboard = create_inline_kb(2, buttons)
    await message.answer(
        reply,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@router.message(Command(commands='delete'))
async def process_delete_command(message: Message):
    reply = 'The word was deleted'
    word = message.text[message.text.find(' ') + 1:].lower()
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(message.from_user.id, conn)[-1]
        if check_my_word_presence(word, conn, str(message.from_user.id) ,lang):
            delete_word_from_table(message.from_user.id, word, conn, lang)
        else:
            reply = "There is no such word in your list"
    await message.answer(
        reply,
    )

@router.message(Command(commands='example'))
async def process_example_command(message: Message):
    word = message.text[message.text.find(' ') + 1:].lower()
    sentence = get_example(word)
    await message.answer(
        sentence
    )

@router.message(Command(commands='random'))
async def process_random_command(message: Message):
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(message.from_user.id, conn)[-1]
        words = get_my_words(conn, str(message.from_user.id), lang)
        if words:
            words = list(map(lambda w: w[0], words))
            word = random.choice(words)
            defs_dict = read_word(message.from_user.id, word, conn, lang)
            defs_dict = dict(filter(lambda k_v: k_v[0] != 'word' and k_v[1], defs_dict.items()))
            reply = word.upper() + ':\n' +'\n'.join(['\t' + key + ':\n\t\t' + ', '.join(value) for key, value in defs_dict.items()])
        else:
            reply = 'Your "' + lang + '" list is empty'
    await message.answer(
        reply
    )

@router.message(Command(commands='dict'))
async def process_dict_command(message: Message):
    word = message.text[message.text.find(' ') + 1:].lower()
    with sqlite3.connect(main_data_base) as conn:
        user_lang = get_user_lang(message.from_user.id, conn)[-1]
    yandex_reply = YandexDict.lookup_class(
        api_key=config.yandex.api_key, word=word, target_lang=user_lang if user_lang else 'ru'
        )
    if (yandex_reply):
        defs_dict = parse_dict_item(word, yandex_reply)
        defs_dict = dict(filter(lambda k_v: k_v[0] != 'word' and k_v[1], defs_dict.items()))
        reply = word.upper() + ':\n' +'\n'.join(['\t' + key + ':\n\t\t' + ', '.join(value) for key, value in defs_dict.items()])
    else:
        with sqlite3.connect(main_data_base) as conn:
            words = get_all_words(conn)
        closest = get_close_matches(word, map(lambda word: word[0], words))
        reply = "The word not found in the dictionary. Maybe you meant one of these: " + ', '.join(closest)
    await message.answer(reply)

@router.message(Command(commands='translate'))
async def process_translate_command(message: Message):
    lang = 'ru'
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(message.from_user.id, conn)[-1]
    text = message.text[message.text.find(' ') + 1:].lower()
    translate = translate_to(text, lang=lang)
    await message.answer(
        translate
    )

@router.message(Command(commands='lang'))
async def process_lang_command(message: Message):
    lang = message.text.split()[-1].lower()
    modes = YandexDict.get_langs(api_key=config.yandex.api_key)
    available_modes = list(
        map(lambda mode: mode[3:],
            filter(lambda mode: 'en-' in mode and len(mode) == 5, modes))
        )
    if lang in available_modes:
        with sqlite3.connect(main_data_base) as conn:
            set_user_lang(message.from_user.id, conn, lang=lang)
        reply = 'The target language is set!'
    elif lang == '/lang':
        with sqlite3.connect(main_data_base) as conn:
            lang = get_user_lang(message.from_user.id, conn)[-1]
        reply = f'Current lang is {lang}'
    else:
        reply = f'Available languages:\n' + '\n'.join(available_modes)
    await message.answer(
        reply
    )

@router.message()
async def process_other_answers(message: Message):
    lang = 'ru'
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(message.from_user.id, conn)[-1]
    text = message.text
    translate = translate_to(text, lang=lang)
    await message.answer(
        translate
    )
