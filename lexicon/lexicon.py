help_reply = '''The bot is like your notebook for words you want to memorize in English.

To track a new word use <b>/add</b> command followed by a new word. If this word is \
in the bots dictionary the word is saved to your table.

To get a random word from your saved list use <b>/random</b> command. You can use \
this command to repeat a random word from your list.

To see the whole list of your words use <b>/list</b> command. You can use this command \
to see all your words. Novigating through your list, If you can recall words \
meaning quickly it is recommended to delete this word from your list with \
<b>/delete</b> command followed by a word you want to delete.

There is also just a <b>/dict</b> command followed by a word. You can use it to see the \
content of the dictionary for this word and word could not be in your list.

To translate your text use <b>/translate</b> command followed by your text \
or send it to bot with no commands.

To see an example of sentance with a word in it use <b>/example</b> command \
followed by a word you want to see in a sentence.

Use <b>/lang</b> command to see current target language and <b>/lang</b> followed by another \
target language to change it.'''

start_reply = \
'Hi! This bot can help you to memorize english words \
you want to track and repeat. Use /help command to see the usage.'

replies = {
    'help': help_reply,
    'start': start_reply,

}
