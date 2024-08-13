import telebot as t
from TG_token import TOKEN

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
    #bot.send_message(msg.chat.id, "*Июльский дайджест лучших публикаций MyReviews*\n\nВ июле мы выпустили дизайн\-редактор 2\.0, чтобы сделать кастомизацию виджетов доступной для пользователей на всех тарифах\.\n\nПодборка материалов о новом редакторе:\n\n🔸 Р[ассказали, почему мы решили разработать редактор виджетов\n](https://vc.ru/services/1310440-my-obnovili-redaktor-vidzhetov-nadoelo-slushat-chto-u-konkurentov-luchshe)\n🔸 Во[плотили идеи Chat\-GPT в дизайне\n\n](https://myreviews.ru/instructions/widgets-design)🔸 Опу[бликовали самый полный обзор редактора и идеи стилизации виджетов на Timeweb Community\n\n⭐️](https://timeweb.com/ru/community/)️ Мы *часто пишем о важности отзывов, поэтому нам будет очень приятно получить обратную связь о том, как MyReviews помогает вашему бизнесу\n  *\n👉 Star[tpack\n👉 Г](https://startpack.ru/add-review/myreviews)еосе[рвисы и карты](https://myreviews.dev/firm/69f23622-f471-4d7a-906e-380d7113fe48/preview?from=short-link&url=https://myreviews.ru)", disable_web_page_preview=True, parse_mode='MarkdownV2')

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
