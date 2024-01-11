
help_reply = '''The bot is like your notebook for words you want to memorize in English.\n
        To track a new word use /add command followed by a new word. If this word is 
        in the bots dictionary the word is saved to your table.\n"
        To get a random word from your saved list use /random command. You can use 
        this command to repeat a random word from your list.\n
        To see the whole list of your words use /list command. You can use this command 
        "to see all your words. Novigating through your list, If you can recall words "
        meaning quickly it is recommended to delete this word from your list with 
        /delete command followed by a word you want to delete.\n
        There is also just a /dict command followed by a word. You can use it to see the 
        content of the dictionary for this word and word could not be in your list.\n
        To translate your text use /translate command followed by your text.\n
        To see an example of sentance with a word in it use /example command 
        followed by a word you want to see in a sentence.\n
        Use /lang command to see current target language and /lang followed by another
        target language to change it.'''

start_reply = \
'Hi! This bot can help you to memorize english words \
you want to track and repeat. Use /help command to see the usage.'

replies = {
    'help': help_reply,
    'start': start_reply,

}