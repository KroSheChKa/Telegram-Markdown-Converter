import telebot as t
from TG_token import TOKEN
from alts import alt_symbs

mrkd_tps = {
    'bold': '*',
    'italic': '_',
    'underline': '__',
    'strikethrough': '~',
    'code': '`',
    'spoiler': '||',
    'pre': '```',
    'bot_command': '',
    'hashtag': ''
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
    else:
        for i in stupid:
            markdowned = markdowned.replace(i, '\\'+i)
        markdowned = markdowned.replace('\n', '\\n')

    bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True)
    #bot.send_message(msg.chat.id, f'{markdowned}', disable_web_page_preview=True, parse_mode='MarkdownV2')
    #bot.send_message(msg.chat.id, "👍 Новый отзыв на [Google](https://www.google.com/maps/place/Timeweb/@59.8888864,30.3263183,17z/data=!4m7!3m6!1s0x4696306cb3b0a325:0x3359a8d8add6587e!8m2!3d59.8888998!4d30.3295799!9m1!1b1)\n🏢 Организация: Example2\n👤 Пользователь: golova\n⭐️ Оценка: 5\n📝 Сообщение: Более полутора лет пользуюсь услугами TimeWeb и полностью удовлетворен\. Хостинг зарекомендовал себя как надежный, а техническая поддержка всегда оперативно решает все возникающие вопросы\. Особо стоит отметить бесплатный 10\-дневный период Free Web, который идеально подходит для тестирования сайта\. Панель управления удобная и интуитивно понятная, а цены приемлемые, с множеством тарифных планов на выбор\. Рекомендую TimeWeb всем, кто ищет качественный и надежный хостинг\.\n📅 Дата: 29\.07\.2024", disable_web_page_preview=True, parse_mode='MarkdownV2')

def parse_dat_bih(text, ent):
    text, deka = no_emojis(text)
    places = place(ent)
    splitted_dots = dots(text, places)
    symbols = symbols_to_paste(ent, text)
    text = combine(splitted_dots, symbols)
    text = return_emojis(text, deka)
    return text

def return_emojis(text, deka):
    for i in deka:
        if i == '\u200d':
            text = text.replace('■', i, 1)
        else:
            text = text.replace('¤¤', i, 1)
    return text

def no_emojis(text):
    print(text)
    deka = []
    step = 0
    last_symb = text[-1]
    while text[step] != last_symb:
        print(text[step],text[step] not in alt_symbs, len(text[step]))
        if text[step] == '\u200d':
            text = text[:step]+'■'+text[step+1:]
            step += 1
            deka.append('\u200d')
            continue

        if text[step] not in alt_symbs:
            deka.append(text[step])
            text = text[:step]+'¤¤'+text[step+1:]
        step += 1
    print(text, "".join(deka))
    return text, deka

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
    print(text,'AAAAAAAAA')
    to_add = 0
    for i in places:
        text.insert(i+to_add, '•')
        to_add += 1
    print(text,'AAAAAAAAA')
    return text

def symbols_to_paste(ent, text):
    s = ['']*(len(text)+25)
    for i in ent:
        print(i)
        if i['type'] == 'text_link':
            s[i['offset']] += '['
            s[i['length'] + i['offset']] += '](' + i['url'] + ')'
            continue
        else:
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
    splitted_dots = splitted_dots.replace('•', '')
    splitted_dots = splitted_dots.replace('\n', '\\n')
    return splitted_dots


bot.infinity_polling()
