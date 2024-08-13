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

stupid = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

bot = t.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, 'Напишит свой текст сюда:')

@bot.message_handler()
def info(msg):
    markdowned = msg.text
    print(markdowned)
    for i in stupid:
        markdowned = markdowned.replace(i, '\\'+i)
    print(markdowned)
    if 'entities' in msg.json:
        markdowned = parse_dat_bih(markdowned, msg.json['entities'])
        #print(msg.json['entities'])

    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True)
    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True, parse_mode='MarkdownV2')


def parse_dat_bih(text, ent):
    to_add = 0
    old_offset = -1
    for el in ent:
        length = el['length']
        type_ = el['type']
        offset = el['offset']
        if old_offset != offset:
            offset += to_add
        else:
            length += len(mrkd_tps[type_])*2
        if type_ == 'text_link':
            text = text[:offset]+'['+text[offset:offset+length]+']('+el['url']+')'+text[offset+length:]
            to_add += 4
        else:
            text = text[:offset]+mrkd_tps[type_]+text[offset:offset+length]+mrkd_tps[type_]+text[offset+length:]
            to_add += len(mrkd_tps[type_])*2
        print(el)
        old_offset = el['offset']
    return text

bot.infinity_polling()
