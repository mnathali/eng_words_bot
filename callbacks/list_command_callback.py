from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode
import sqlite3
from database.db_manipulations import *
from keyboars.create_keyboard import create_inline_kb
from config import main_data_base

router = Router()

@router.callback_query(F.data.in_(['right', 'left', 'page']))
async def process_callback_buttons(callback: CallbackQuery):
    reply = '<b>Your words:</b>\n\n\t'
    words = []
    offset = 1 if callback.data == 'right' else -1
    if callback.data == 'page':
        offset = 0
    cur_page = next(filter(lambda key: key.callback_data == 'page',
                      callback.message.reply_markup.inline_keyboard[0]))
    with sqlite3.connect(main_data_base) as conn:
        lang = get_user_lang(callback.from_user.id, conn)[-1]
        words = get_my_words(conn, str(callback.from_user.id), lang)
    n_cur_page = int(cur_page.text.split('/')[0])
    begin, end = (10 * (n_cur_page - 1 + offset),
                  10 * (n_cur_page - 1 + offset) + 10)
    buttons = {}
    if n_cur_page - 1 + offset > 0:
        buttons['left'] = '<<'
    buttons['page'] = (str(n_cur_page + offset)
                    + f'/{len(words) // 10 + (1 if len(words) % 10 else 0)}')
    if len(words) > 10 * (n_cur_page - 1 + offset) + 10:
        buttons['right'] = '>>'
    words = list(map(lambda w: w[0], words[begin:end]))
    reply += '\n\t'.join(map(lambda w: w, words))
    keyboard = create_inline_kb(len(buttons), buttons)
    present_words = callback.message.text.replace('Your words:', '').split()
    if not all(map(lambda w: w in present_words, words)):
        await callback.message.edit_text(
                text=reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML
            )
    else:
        await callback.answer()
