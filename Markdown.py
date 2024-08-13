import telebot as t
from TG_token import TOKEN

mrkd_tps = {
    'bold': '*',
    'italic': '_',
    'underline': '__',
    'strikethrough': '~',
    'code': '`',
    'spoiler': '||',
}

bot = t.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, 'Напишит свой текст сюда:')

@bot.message_handler()
def info(msg):
    markdowned = msg.text
    if 'entities' in msg.json:
        markdowned = parse_dat_bih(msg.text, msg.json['entities'])
        #print(msg.json['entities'])
    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True)
    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True, parse_mode='MarkdownV2')


def parse_dat_bih(text, ent):
    to_add = 0
    for el in ent:
        offset = el['offset']+to_add
        length = el['length']
        type_ = el['type']
        if type_ == 'text_link':
            print('yep')
            text = text[:offset]+'['+text[offset:offset+length]+']('+el['url']+')'+text[offset+length:]
            to_add += 4
        else:
            text = text[:offset]+mrkd_tps[type_]+text[offset:offset+length]+mrkd_tps[type_]+text[offset+length:]
            to_add += len(mrkd_tps[type_])*2
        print(el)
    return text

bot.infinity_polling()