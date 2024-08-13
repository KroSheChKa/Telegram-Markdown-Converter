import telebot as t
from TG_token import TOKEN

mrkd_tps = {
    'bold': '*',
    'italic': '_',
    'underline': '__',
    'strikethrough': '~',
    'code': '`',
    'spoiler': '||',
    'pre': '```'
}
special = ['blockquote', 'mention', 'text_link', ('expandable_blockquote', ['**>', '||'])]
stupid = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

bot = t.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, 'Write sum')

@bot.message_handler()
def info(msg):
    markdowned = msg.text

    if 'entities' in msg.json:
        markdowned = parse_dat_bih(markdowned, msg.json['entities'])
        #print(msg.json['entities'])

    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True)
    #bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True, parse_mode='MarkdownV2')
    #bot.send_message(msg.chat.id, "", disable_web_page_preview=True, parse_mode='MarkdownV2')

def parse_dat_bih(text, ent):
    places = place(ent)
    splitted_dots = dots(text, places)
    symbols = symbols_to_paste(ent, text)
    text = combine(splitted_dots, symbols)
    return text

def place(ent):
    s = set()
    for i in ent:
        s.add(i['offset'])
        s.add(i['offset']+i['length'])
    s = sorted(list(s))
    print(s)
    return s

def dots(text, places):
    text = [i for i in text]
    to_add = 0
    for i in places:
        text.insert(i+to_add, '•')
        to_add += 1
    print(text)
    return text

def symbols_to_paste(ent, text):
    s = ['']*(len(text)+1)
    for i in ent:
        if i['type'] == 'text_link':
            s[i['offset']] += '['
            s[i['length'] + i['offset']] += '](' + i['url'] + ')'
            continue
        print(i)
        s[i['offset']] += mrkd_tps[i['type']]
        s[i['length'] + i['offset']] = mrkd_tps[i['type']] + s[i['length'] + i['offset']]
    s = [j for j in s if j]
    print(s,'1')
    flag = 0
    for i in range(len(s)):
        if '___' in s[i]:
            if flag:
                s[i] = s[i].replace('___', '_**__')
            else:
                s[i] = s[i].replace('___', '__**_')
            flag = not flag
    print(s, 'ya')
    return s

def combine(splitted_dots, symbols):
    splitted_dots = "".join(splitted_dots)

    for i in stupid:
        splitted_dots = splitted_dots.replace(i, '\\'+i)

    print(splitted_dots,'2')
    for i in symbols:
        splitted_dots = splitted_dots.replace('•', i, 1)
    print(splitted_dots)
    splitted_dots = splitted_dots.replace('\n', '\\n')
    return splitted_dots


bot.infinity_polling()
