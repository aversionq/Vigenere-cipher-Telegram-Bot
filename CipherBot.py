import telebot
import cfg
from telebot import types


bot = telebot.TeleBot(cfg.TOKEN)
alphabet_high_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alphabet_low_ru = alphabet_high_ru.lower()
alphabet_ru = alphabet_low_ru
alphabet_eng = 'abcdefghijklmnopqrstuvwxyz'
string_cipher = []
choice = ''


def ToViginere(string , key , alphabet_):
    string_new = ''
    key_repl = key.replace(' ','')
    # Определяем ключ, в зависимости от длины строки
    if len(string) > len(key_repl):
        to_time = len(string) // len(key_repl)
        to_div = len(string) % len(key_repl)
        new_key = key_repl*to_time + key_repl[:to_div]
    elif len(key_repl) > len(string):
        new_key = key_repl[:len(string)]
    else:
        new_key = key_repl
    t = 0
    new_key = new_key.lower()
    string = string.lower()
    # Замена символов
    for i in range(len(new_key)):
        if string[i] in alphabet_:
            ind_to_change = int(alphabet_.index(string[i])) + int(alphabet_.index(new_key[i + t]))
            if ind_to_change < len(alphabet_):
                letter_change = ind_to_change
            else:
                letter_change = ind_to_change - len(alphabet_)
            string_new += alphabet_[letter_change]
        else:
            t -= 1
            string_new += string[i]
    return string_new


def FromViginere(string , key , alphabet_):
    string_new = ''
    key_repl = key.replace(' ','')
    # Определяем ключ, в зависимости от длины строки
    if len(string) > len(key_repl):
        to_time = len(string) // len(key_repl)
        to_div = len(string) % len(key_repl)
        new_key = key_repl*to_time + key_repl[:to_div]
    elif len(key_repl) > len(string):
        new_key = key_repl[:len(string)]
    else:
        new_key = key_repl
    t = 0
    new_key = new_key.lower()
    string = string.lower()
    # Замена символов
    for i in range(len(new_key)):
        if string[i] in alphabet_:
            ind_to_change = int(alphabet_.index(string[i])) - int(alphabet_.index(new_key[i + t]))
            if ind_to_change < len(alphabet_):
                letter_change = ind_to_change
            else:
                letter_change = ind_to_change - len(alphabet_)
            string_new += alphabet_[letter_change]
        else:
            t -= 1
            string_new += string[i]
    return string_new


@bot.message_handler( commands = ['start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Привет, с помощью этого бота можно зашифровать/расшифровать текст с помошью шифра Виженера. /help - ознакомиться с командами')


@bot.message_handler(commands = ['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/toviginere - зашифровать текст с помощью шифра Виженера' + '\n' + '/fromviginere - расшифровать текст с помощью шифра Виженера')


@bot.message_handler(commands = ['toviginere'])
def text_to_viginere(message):
    global choice
    choice = message.text
    language_choose = types.ReplyKeyboardMarkup()
    language_choose.row('🇬🇧' , '🇷🇺')
    bot.send_message(message.chat.id, 'Выберите язык из всплывающего меню', reply_markup=language_choose)


@bot.message_handler(commands = ['fromviginere'])
def text_from_viginere(message):
    global choice
    choice = message.text
    language_choose1 = types.ReplyKeyboardMarkup()
    language_choose1.row('🇬🇧' , '🇷🇺')
    bot.send_message(message.chat.id, 'Выберите язык из всплывающего меню', reply_markup=language_choose1)


@bot.message_handler(content_types = ['text'])
def cipher(message):
    global choice
    global alphabet_to_use
    if choice == '/toviginere':
        if message.text == '🇷🇺':
            alphabet_to_use = alphabet_ru
            bot.send_message(message.chat.id, 'Введите текст, который нужно зашифровать')
        elif message.text == '🇬🇧':
            alphabet_to_use = alphabet_eng
            bot.send_message(message.chat.id, 'Введите текст, который нужно зашифровать')
        else:
            string_cipher.append(message.text)
            if len(string_cipher) < 2:
                bot.send_message(message.chat.id, 'Введите ключ')
            else:
                answer = ToViginere(string_cipher[0], string_cipher[1], alphabet_to_use)
                bot.send_message(message.chat.id, 'То, что вы ввели: ' + str(string_cipher[0]) +'\n' + 'Результат шифрования: ' + str(answer))
                string_cipher.clear()
                alphabet_to_use = ''
    elif choice == '/fromviginere':
        if message.text == '🇷🇺':
            alphabet_to_use = alphabet_ru
            bot.send_message(message.chat.id, 'Введите текст, который нужно расшифровать')
        elif message.text == '🇬🇧':
            alphabet_to_use = alphabet_eng
            bot.send_message(message.chat.id, 'Введите текст, который нужно расшифровать')
        else:
            string_cipher.append(message.text)
            if len(string_cipher) < 2:
                bot.send_message(message.chat.id, 'Введите ключ')
            else:
                answer = FromViginere(string_cipher[0], string_cipher[1], alphabet_to_use)
                bot.send_message(message.chat.id, 'То, что вы ввели: ' + str(string_cipher[0]) +'\n' + 'Результат расшифровки: ' + str(answer))
                string_cipher.clear()
                alphabet_to_use = ''


bot.polling(none_stop=True)