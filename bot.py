import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import os
import threading
import time
import datetime
from yoomoney import Client
import sqlite3
from yoomoney import Quickpay
from collections import defaultdict
dislikes_count = defaultdict(int)
dislikes_timestamp = defaultdict(list)
def parse_custom_datetime(datetime_str):
    parts = datetime_str.split('.')
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    hour = int(parts[3])
    return datetime.datetime(year, month, day, hour)

def calculate_future_date(days, user):
    with sqlite3.connect(config.bd) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT activvip FROM users WHERE id=?', (user,))
        result = cursor.fetchone()
        
        if result:
            refers_value = result[0]
        
        if refers_value is None or refers_value == '0':
            current_date = datetime.datetime.now()
            future_date = current_date + datetime.timedelta(days=days)
            return future_date
        else:
            current_date = parse_custom_datetime(refers_value)
            future_date = current_date + datetime.timedelta(days=days)
            return future_date
dirname = str(os.getcwd()) + "\\users"
if not os.path.exists(dirname):
    os.mkdir(dirname)
dirname = str(os.getcwd()) + "\\chats"
if not os.path.exists(dirname):
    os.mkdir(dirname)
start1 = 0
filetype = ""
block = []
SELECTING_ACTION = 0
proverka = []
waiting_chat_ids = []
id_admin = config.id
admins = []
partner_pairs = []
save_paths = {}
ocenka = []
rassil = 0
age = []
oplata = []
ager = []
vremmem = []
conn = sqlite3.connect(config.bd)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        refer TEXT,
        refers INT,
        reiting INT,
        vip INT,
        activvip TEXT,
        gender TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INT
    )
''')
def check_vip_expiry(update, context):
    while True:
        current_date = datetime.datetime.now()

        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, activvip FROM users')
            users = cursor.fetchall()

            for user in users:
                user_id, activvip = user
                
                if activvip is None or activvip == '0':
                    continue 
                
                vip_expiry_date = datetime.datetime.strptime(activvip, '%d.%m.%Y.%H')
                
                if vip_expiry_date <= current_date:
                    cursor.execute('UPDATE users SET activvip=?, vip=? WHERE id=?', (None, 0, user_id))
                    conn.commit()
                    
                    try:
                        context.bot.send_message(user_id, "Ваша vip подписка истекла")
                        print("Подписка " + str(user_id) + " истекла")
                    except:
                        pass
        time.sleep(3600)

conn.commit()
def start(update, context):
    global start1
    if int(start1) == 0:
        thread = threading.Thread(target=check_vip_expiry, args=(update, context))
        thread.start()
        start1 = 1
    user = update.message.from_user
    chat_id = update.message.chat_id
    referral_code = context.args[0] if context.args else None
    with sqlite3.connect(config.bd) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user.id,))
        existing_user = cursor.fetchone()

        if existing_user is None:
            if not referral_code == None and not referral_code == user.id:
                cursor.execute('INSERT INTO users (id, username, first_name, last_name, refer, refers, reiting, vip, activvip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (user.id, user.username, user.first_name, user.last_name, referral_code, 0, 0, 0, 0))
                thread = threading.Thread(target=refer, args=(update, context, referral_code, chat_id))
                thread.start()
            elif referral_code == None:
                cursor.execute('INSERT INTO users (id, username, first_name, last_name, refer, refers, reiting, vip, activvip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (user.id, user.username, user.first_name, user.last_name, user.id, 0, 0, 0, 0))
            conn.commit()
    sasasas = check_channel(update, context)
    if not sasasas == False or str(chat_id) == id_admin:
        chat_id = update.message.chat_id
        reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
        try:
            update.message.reply_text("Привет, если хочешь пообщаться, нажми кнопку 'Подобрать собеседника ❤️'\n\nЕсли у вас возникли проблемы или другие вопросы @sov_support_bot", reply_markup=reply_markup)
        except:
            pass
    else:
        thread = threading.Thread(target=check_channel1, args=(update, context))
        thread.start()
        keyboard = [[InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/anonymous_bot_update")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            context.bot.send_message(chat_id, "Чтобы разблокировать бота надо подписаться на канал!", reply_markup=reply_markup) #Чтобы разблокировать бота надо подписатся на канал!
        except:
            pass
def block1(update, context, id):
    time.sleep(3660)
    block.remove(id)
    try:
        context.bot.send_message(id, "Мут был снят")
    except:
        pass
def refer(update, context, referral_code, chat_id):
    user = update.message.from_user
    ssasa = 0
    if referral_code == "6469901152":
        try:
            context.bot.send_message(referral_code, "Отличная работа вы привели нового реферала! " + str(chat_id))
        except:
            pass
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user.id,))
        existing_user = cursor.fetchone()
        cursor.execute('SELECT refers FROM users WHERE id=?', (referral_code,))
        result = cursor.fetchone()
        if result:
            refers_value = result[0]
        cursor.execute('UPDATE users SET refers=? WHERE id=?', (int(refers_value) + int(1), referral_code))
        conn.commit()
    else:
        while True:
            ssasa = ssasa + 1
            if check_channel(update, context) == False:
                ssasa = 0
            if ssasa == 10800:
                break
            time.sleep(1)
        try:
            context.bot.send_message(referral_code, "Отличная работа вы привели нового реферала!")
        except:
            pass
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user.id,))
        existing_user = cursor.fetchone()
        cursor.execute('SELECT refers FROM users WHERE id=?', (referral_code,))
        result = cursor.fetchone()
        if result:
            refers_value = result[0]
        cursor.execute('UPDATE users SET refers=? WHERE id=?', (int(refers_value) + int(1), referral_code))
        conn.commit()
def handle_common(update: Update, context, filetype: str):
    chat_id = update.message.chat_id
    partner = None
    
    for sas in partner_pairs:
        if str(chat_id) in str(sas[0]):
            partner = str(sas[1])
            papcka = str(sas[2])
            break
        elif str(chat_id) in str(sas[1]):
            partner = str(sas[0])
            papcka = str(sas[2])
            break
            
    if partner:
        forward_media(update, context, filetype, partner)

def handle_photo(update: Update, context: CallbackContext):
    handle_common(update, context, 'photo')

def handle_video(update: Update, context: CallbackContext):
    handle_common(update, context, 'video')

def handle_voice(update: Update, context: CallbackContext):
    handle_common(update, context, 'voice')

def handle_sticker(update: Update, context: CallbackContext):
    handle_common(update, context, 'sticker')

def handle_document(update: Update, context: CallbackContext):
    handle_common(update, context, 'document')

def handle_audio(update: Update, context: CallbackContext):
    handle_common(update, context, 'audio')

def handle_contact(update: Update, context: CallbackContext):
    handle_common(update, context, 'contact')

def handle_location(update: Update, context: CallbackContext):
    handle_common(update, context, 'location')

def handle_game(update: Update, context: CallbackContext):
    handle_common(update, context, 'game')

def handle_video_note(update: Update, context: CallbackContext):
    handle_common(update, context, 'video_note')
def handle_caption(update: Update, context: CallbackContext):
    handle_common(update, context, 'caption')
def handle_animation(update: Update, context: CallbackContext):
    handle_common(update, context, 'animation')
def check_channel1(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    boom = 1
    chat_id = update.message.chat_id
    proverka.append(chat_id)
    user_id = update.effective_user.id
    channel_id = "@anonymous_bot_update"
    while boom < 3600:
        boom = boom + 1
        try:
            chat_member = context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if chat_member.status == 'member' or chat_member.status == 'administrator': #chat_member.status == 'member' or
                reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
                try:
                    context.bot.send_message(chat_id, 'Спасибо за подписку!\nПривет, если хочешь пообщаться, нажми кнопку "Подобрать собеседника ❤️"', reply_markup=reply_markup)
                except:
                    pass
                with sqlite3.connect(config.bd) as conn:
                    cursor = conn.cursor()

                cursor.execute('SELECT gender FROM users WHERE id=?', (chat_id,))
                result = cursor.fetchone()
                if result:
                    refers_value = result[0]
                if refers_value == None:
                    keyboard = [
                        [InlineKeyboardButton("Мужской", callback_data="M")],
                        [InlineKeyboardButton("Женский", callback_data="W")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.send_message(chat_id, "Перед началом общения, пожалуйста, укажите свой пол", reply_markup=reply_markup)
                proverka.remove(chat_id)
                boom = 1
                break
            else:
                time.sleep(1)
        except:
            update.message.reply_text("Ошибка проверки")

def check_channel(update, context):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    channel_id = "@anonymous_bot_update"
    try:
        chat_member = context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if chat_member.status == 'member' or chat_member.status == 'administrator': #chat_member.status == 'member' or
            return True
        else:
            return False
    except:
        update.message.reply_text("Ошибка проверки")

def forward_media(update: Update, context, filetype: str, partner_id: str):
    message = update.message
    
    if getattr(message, filetype):
        media = getattr(message, filetype)
        
        if filetype == 'photo':
            context.bot.send_photo(partner_id, photo=media[-1].file_id)
        elif filetype == 'video':
            context.bot.send_video(partner_id, video=media.file_id)
        elif filetype == 'voice':
            context.bot.send_voice(partner_id, voice=media.file_id)
        elif filetype == 'sticker':
            context.bot.send_sticker(partner_id, sticker=media.file_id)
        elif filetype == 'document':
            context.bot.send_document(partner_id, document=media.file_id)
        elif filetype == 'audio':
            context.bot.send_audio(partner_id, audio=media.file_id)
        elif filetype == 'animation':
            context.bot.send_animation(partner_id, animation=media.file_id)
        elif filetype == 'caption':
            context.bot.send_message(partner_id, text=media.caption)
        elif filetype == 'contact':
            context.bot.send_contact(partner_id, phone_number=media.phone_number, first_name=media.first_name)
        elif filetype == 'location':
            context.bot.send_location(partner_id, latitude=media.latitude, longitude=media.longitude)
        elif filetype == 'video_note':
            context.bot.send_video_note(partner_id, video_note=media.file_id)
        elif filetype == 'game':
            context.bot.send_game(partner_id, game_short_name=media.game_short_name)
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    global rassil
    with sqlite3.connect(config.bd) as conn:
        cursor = conn.cursor()
    if "M" == query.data and not query.message.chat_id in vremmem or "W" == query.data and not query.message.chat_id in vremmem:
        if "M" == query.data:
            cursor.execute('UPDATE users SET gender=? WHERE id=?', ("M", query.message.chat_id))
            conn.commit()
            context.bot.send_message(query.message.chat_id, "Информация заполнена")
            vremmem.append(query.message.chat_id)
        elif "W" == query.data:
            cursor.execute('UPDATE users SET gender=? WHERE id=?', ("W", query.message.chat_id))
            conn.commit()
            context.bot.send_message(query.message.chat_id, "Информация заполнена")
            vremmem.append(query.message.chat_id)
    elif "rassil" == query.data:
        rassil = 1
        try:
            context.bot.send_message(query.message.chat_id, "Напиши сообщение")
        except:
            pass
    elif "proverka" == query.data:
        query = update.callback_query
        query.answer()
        user_id = query.message.chat_id
        token = ""
        client = Client(token)
        skip = 0
        sasdfw = str(query.message.chat_id) + str(1)
        history = client.operation_history(label=sasdfw)
        for operation in history.operations:
            sassss = operation.operation_id
            cursor.execute("SELECT * FROM payments WHERE id = ?", (operation.operation_id,))
            result = cursor.fetchone()
            if result:
                pass
            else:
                    if operation.status == "success":
                        future_date = calculate_future_date(1, query.message.chat_id)
                        cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                        conn.commit()
                        cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id,))
                        conn.commit()
                        cursor.execute('INSERT INTO payments (id) VALUES (?)',
                            (int(sassss),))
                        conn.commit()
                        try:
                            context.bot.send_message(user_id, "Отлично подписка оформлена на 1 день\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                        except:
                            pass
        sasdfw = str(query.message.chat_id) + str(7)
        history = client.operation_history(label=sasdfw)
        for operation in history.operations:
            sassss = operation.operation_id
            cursor.execute("SELECT * FROM payments WHERE id = ?", (operation.operation_id,))
            result = cursor.fetchone()
            if result:
                pass
            else:
                        if operation.status == "success":
                            future_date = calculate_future_date(7, query.message.chat_id)
                            cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                            conn.commit()
                            cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id,))
                            conn.commit()
                            cursor.execute('INSERT INTO payments (id) VALUES (?)',
                                (int(sassss),))
                            conn.commit()
                            try:
                                context.bot.send_message(str(user_id), "Отлично подписка оформлена на 7 дней\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                            except:
                                pass
        sasdfw = str(query.message.chat_id) + str(30)
        history = client.operation_history(label=sasdfw)
        for operation in history.operations:
                sassss = operation.operation_id
                cursor.execute("SELECT * FROM payments WHERE id = ?", (operation.operation_id,))
                result = cursor.fetchone()
                if result:
                    pass
                else:
                        if operation.status == "success":
                            future_date = calculate_future_date(30, query.message.chat_id)
                            cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                            conn.commit()
                            cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id,))
                            conn.commit()
                            cursor.execute('INSERT INTO payments (id) VALUES (?)',
                                (int(sassss),))
                            conn.commit()
                            try:
                                context.bot.send_message(str(user_id), "Отлично подписка оформлена на 30 дней\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                            except:
                                pass
    elif "MR" == query.data or "WR" == query.data:
        if "MR" == query.data:
            cursor.execute('UPDATE users SET gender=? WHERE id=?', ("M", query.message.chat_id))
            conn.commit()
            context.bot.send_message(query.message.chat_id, "Отлично пол изменен")
        elif "WR" == query.data:
            cursor.execute('UPDATE users SET gender=? WHERE id=?', ("W", query.message.chat_id))
            conn.commit()
            context.bot.send_message(query.message.chat_id, "Отлично пол изменен")
    elif query.data == "pol" or query.data == "vipstroicka":
        if query.data == "pol":
            keyboard = [
                [InlineKeyboardButton("Мужской", callback_data="MR")],
                [InlineKeyboardButton("Женский", callback_data="WR")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                context.bot.send_message(query.message.chat_id, "Выберете новый пол", reply_markup=reply_markup)
            except:
                pass
    elif "byee" == query.data:
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()

        cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
        result = cursor.fetchone()
        if result:
            refers_value = result[0]
        # if refers_value == 0:
        keyboard = [
            [InlineKeyboardButton("Yoomoney", callback_data="Yoomoney")],
            [InlineKeyboardButton("Рефералы в боте", callback_data="refs")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            context.bot.send_message(query.message.chat_id, "Выберете платежную систему", reply_markup=reply_markup)
        except:
            pass
        # else:
        #     try:
        #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
        #     except:
        #         pass
    elif "Yoomoney" == query.data or "refs" == query.data:
        if "refs" == query.data:
            keyboard = [
                [InlineKeyboardButton("1 день - 2 реферала", callback_data="refs1")],
                [InlineKeyboardButton("7 дней - 10 рефералов", callback_data="refs2")],
                [InlineKeyboardButton("30 дней - 30 рефералов", callback_data="refs3")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                context.bot.send_message(query.message.chat_id, "Выберете срок подписки", reply_markup=reply_markup)
            except:
                pass
        if "Yoomoney" == query.data:
            keyboard = [
                [InlineKeyboardButton("1 день -  19 руб", callback_data="Yoomoney1")],
                [InlineKeyboardButton("7 дней - 100 руб", callback_data="Yoomoney2")],
                [InlineKeyboardButton("30 дней - 379 руб", callback_data="Yoomoney3"),]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                context.bot.send_message(query.message.chat_id, "Выберете срок подписки", reply_markup=reply_markup)
            except:
                pass
    elif "refs1" == query.data or "refs2" == query.data or "refs3" == query.data:
        if "refs1" == query.data:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()

            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()
            cursor.execute('SELECT refers FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            if refers_value >= 2:
                future_date = calculate_future_date(1, query.message.chat_id)
                cursor.execute('UPDATE users SET refers=? WHERE id=?', (int(refers_value) - int(2), query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id,))
                conn.commit()
                try:
                    context.bot.send_message(str(query.message.chat_id), "Отлично подписка оформлена на 1 день\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                except:
                    pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass

        if "refs2" == query.data:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()

            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()

            cursor.execute('SELECT refers FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            if refers_value >= 10:
                future_date = calculate_future_date(7, query.message.chat_id)
                cursor.execute('UPDATE users SET refers=? WHERE id=?', (int(refers_value) - int(10), query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id))
                conn.commit()
                    
                try:
                    context.bot.send_message(str(query.message.chat_id), "Отлично подписка оформлена на 7 дней\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                except:
                    pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass
        if "refs3" == query.data:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()

            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()
            cursor.execute('SELECT refers FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            if refers_value >= 30:
                future_date = calculate_future_date(30, query.message.chat_id)
                cursor.execute('UPDATE users SET refers=? WHERE id=?', (int(refers_value) - int(30), query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET vip=? WHERE id=?', (1, query.message.chat_id))
                conn.commit()
                cursor.execute('UPDATE users SET activvip=? WHERE id=?', (str(future_date.strftime('%d.%m.%Y.%H')), query.message.chat_id))
                conn.commit()
                
                try:
                    context.bot.send_message(str(query.message.chat_id), "Отлично подписка оформлена на 30 дней\nПодписка истекает " + str(future_date.strftime('%d.%m.%Y в %H часов')))
                except:
                    pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass
    elif "Yoomoney1" == query.data or "Yoomoney2" == query.data or "Yoomoney3" == query.data:
        if "Yoomoney1" == query.data:
            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            sasss = str(query.message.chat_id) + str(1)
            quickpay = Quickpay(
                receiver=config.receiver,
                quickpay_form="shop",
                targets="vip 1 день",
                paymentType="SB",
                sum=19,
                label=sasss
                )
            try:
                keyboard = [
                    [InlineKeyboardButton("Оплатить", url=quickpay.base_url)],
                    [InlineKeyboardButton("Проверить", callback_data="proverka")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(str(query.message.chat_id), "Оплата подписки vip 1 день", reply_markup=reply_markup)
            except:
                pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass
        if "Yoomoney2" == query.data:
            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            sasss = str(query.message.chat_id) + str(7)
            quickpay = Quickpay(
                receiver=config.receiver,
                quickpay_form="shop",
                targets="vip 7 дней",
                paymentType="SB",
                sum=100,
                label=sasss
                )
            try:
                keyboard = [
                    [InlineKeyboardButton("Оплатить", url=quickpay.base_url)],
                    [InlineKeyboardButton("Проверить", callback_data="proverka")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(str(query.message.chat_id), "Оплата подписки vip 7 дней", reply_markup=reply_markup)
            except:
                pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass
        if "Yoomoney3" == query.data:
            cursor.execute('SELECT vip FROM users WHERE id=?', (query.message.chat_id,))
            result = cursor.fetchone()
            if result:
                refers_value = result[0]
            # if refers_value == 0:
            sasss = str(query.message.chat_id) + str(30)
            quickpay = Quickpay(
                receiver=config.receiver,
                quickpay_form="shop",
                targets="vip 30 дней",
                paymentType="SB",
                sum=379,
                label=sasss
                )
            try:
                keyboard = [
                    [InlineKeyboardButton("Оплатить", url=quickpay.base_url)],
                    [InlineKeyboardButton("Проверить", callback_data="proverka")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(str(query.message.chat_id), "Оплата подписки vip 30 дней", reply_markup=reply_markup)
            except:
                pass
            # else:
            #     try:
            #         context.bot.send_message(query.message.chat_id, "Кажется у вас уже есть подписка")
            #     except:
            #         pass
    elif query.data == "thumb_up" or query.data == "thumb_down":
        passs = 0
        passs1 = 0
        for ocenk in ocenka:
            if ocenk[0] == str(query.message.chat_id):
                passs1 = ocenk[1]
                passs = 1
                break
    
        if passs == 1:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()  
                cursor.execute('SELECT reiting FROM users WHERE id=?', (passs1,))
                result = cursor.fetchone()
                cursor.execute('SELECT vip FROM users WHERE id=?', (passs1,))
                result2 = cursor.fetchone()
                
                if result:
                    refers_value = result[0]
                    refers_value1 = result2[0]
                    if query.data == "thumb_up":
                        cursor.execute('UPDATE users SET reiting=? WHERE id=?', (int(refers_value) + 1, passs1))
                        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
                    elif query.data == "thumb_down":
                        if not passs1 in block:
                            dislikes_count[passs1] += 1
                            dislikes_timestamp[passs1].append(datetime.datetime.now())
                            if dislikes_count[passs1] >= 5:
                                dislikes_count[passs1] = 0
                                print(f"Пользователь {passs1} получил 5 дизлайков!")
                                if refers_value1 == 0:
                                    context.bot.send_message(str(passs1), "Вы получили мут на чат за очень низкий рейтинг!")
                                    block.append(passs1)
                                    thread = threading.Thread(target=block1, args=(update, context, passs1))
                                    thread.start()
                                elif refers_value1 == 1:
                                    context.bot.send_message(str(passs1), "У вас плохой рейтинг ведите себя хорошо!")
                            with sqlite3.connect(config.bd) as conn:
                                cursor = conn.cursor()
                                cursor.execute('SELECT reiting FROM users WHERE id=?', (passs1,))
                                result = cursor.fetchone()

                                if result:
                                    refers_value = result[0]
                                    cursor.execute('UPDATE users SET reiting=? WHERE id=?', (int(refers_value) - 1, passs1))
                                    conn.commit()
                    conn.commit()
                    ocenka.remove((str(query.message.chat_id), str(passs1)))
                    try:
                        context.bot.send_message(str(query.message.chat_id), "Спасибо за оценку!")
                    except:
                        pass



def handle_message(update, context):
    okey = 0
    global save_paths
    global rassil
    message = update.message.text
    chat_id = update.message.chat_id
    id_user = update.message.chat.id
    member = update.message.from_user.username
    name1 = update.message.from_user.first_name
    global proverka
    with sqlite3.connect(config.bd) as conn:
        cursor = conn.cursor()
    sasasas = check_channel(update, context)
    if chat_id in admins and rassil == 1:
        cursor.execute('SELECT id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        for user_id in user_ids:
            try:
                context.bot.send_message(user_id, message)
            except Exception as e:
                pass
        rassil = 0
        context.bot.send_message(chat_id, "Сообщение отправлено!")
    elif not str(chat_id) == str(id_admin) and not str(chat_id) == str(id_admin) and str(chat_id) in proverka:
        keyboard = [[InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/anonymous_bot_update")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            context.bot.send_message(chat_id, "Чтобы разблокировать бота надо подписаться на канал!", reply_markup=reply_markup)
        except:
            pass
    elif not sasasas == True and not str(chat_id) == str(id_admin) and not str(chat_id) in proverka:
        thread = threading.Thread(target=check_channel1, args=(update, context))
        thread.start()
        keyboard = [[InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/anonymous_bot_update")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            context.bot.send_message(chat_id, "Чтобы разблокировать бота надо подписаться на канал!", reply_markup=reply_markup)
        except:
            pass
    elif message == "❌Отменить поиск❌" and chat_id in waiting_chat_ids:
        waiting_chat_ids.remove(chat_id)
        reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
        try:
            context.bot.send_message(chat_id, "❌Поиск отменен❌", reply_markup=reply_markup)
        except:
            pass
    elif message == "👁‍🗨Данные пользователя👁‍🗨" and chat_id in admins:
        okeoke = 0
        for partne in partner_pairs:
            if partne[0] == chat_id:
                passs1 = partne[1]
                okeoke = 1
            elif partne[1] == chat_id:
                passs1 = partne[0]
                okeoke = 1
        if okeoke == 1:
            cursor.execute('SELECT username, first_name, refer, refers, reiting, vip, activvip FROM users WHERE id=?', (passs1,))
            partner_result = cursor.fetchone()

            if partner_result:
                username, first_name, refer, refers, reiting, vip, activvip = partner_result
            context.bot.send_message(chat_id, f"Пользователь {passs1} \n\nId: {passs1}\nНик: {username}\nИмя:{first_name}\nПринадлежность: {refer}\nКоличество рефералов: {refers}\nРейтинг: {reiting}\nВип подписка: {vip}\nДата окончания подписки: {activvip}")
    elif message == "Подобрать собеседника ❤️" and chat_id not in waiting_chat_ids:
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()

        cursor.execute('SELECT gender, vip FROM users WHERE id=?', (chat_id,))
        result = cursor.fetchone()

        if result:
            gender, vip_status = result

        if gender is None:
            keyboard = [
                [InlineKeyboardButton("Мужской", callback_data="M")],
                [InlineKeyboardButton("Женский", callback_data="W")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, "Перед началом общения, пожалуйста, укажите свой пол", reply_markup=reply_markup)
        else:
            if str(chat_id) not in block:
                reply_markup = ReplyKeyboardMarkup([["❌Отменить поиск❌"]], resize_keyboard=True)
                try:
                    context.bot.send_message(chat_id, "Поиск собеседника", reply_markup=reply_markup)
                except:
                    pass
                waiting_chat_ids.append(chat_id)

                if int(len(waiting_chat_ids)) > 1:
                    for partner_id in waiting_chat_ids:
                        if partner_id != str(chat_id):
                            cursor.execute('SELECT gender, vip FROM users WHERE id=?', (partner_id,))
                            partner_result = cursor.fetchone()

                            if partner_result:
                                partner_gender, partner_vip_status = partner_result

                            if partner_id != chat_id:
                                if ((int(vip_status) == 1 and int(partner_vip_status) == 0) or (int(vip_status) == 0 and int(partner_vip_status) == 1)) and gender != partner_gender:
                                    now = datetime.datetime.now()
                                    smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                    partner_pairs.append((partner_id, chat_id, smac))
                                    dirname = os.path.join(os.getcwd(), "chats", smac)

                                    if not os.path.exists(dirname):
                                        os.mkdir(dirname)
                                    if chat_id in admins and partner_id in admins:
                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif chat_id in admins:
                                        reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif partner_id in admins:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                        except:
                                            pass
                                    else:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                    chat_id_result = cursor.fetchone()
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                    partner_result_reiting = cursor.fetchone()
                                    if chat_id_result:
                                        usudsu = chat_id_result[0]
                                    if partner_result_reiting:
                                        usudsu12 = partner_result_reiting[0]
                                    if usudsu < -1:
                                        try:
                                            context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    if usudsu12 < -1:
                                        try:
                                            context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    waiting_chat_ids.remove(partner_id)
                                    waiting_chat_ids.remove(chat_id)
                                    break
                                elif ((int(vip_status) == 1 and int(partner_vip_status) == 1) or (int(vip_status) == 1 and int(partner_vip_status) == 1)) and gender != partner_gender:
                                    now = datetime.datetime.now()
                                    smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                    partner_pairs.append((partner_id, chat_id, smac))
                                    dirname = os.path.join(os.getcwd(), "chats", smac)

                                    if not os.path.exists(dirname):
                                        os.mkdir(dirname)
                                    if chat_id in admins and partner_id in admins:
                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif chat_id in admins:
                                        reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif partner_id in admins:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                        except:
                                            pass
                                    else:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                    chat_id_result = cursor.fetchone()
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                    partner_result_reiting = cursor.fetchone()
                                    if chat_id_result:
                                        usudsu = chat_id_result[0]
                                    if partner_result_reiting:
                                        usudsu12 = partner_result_reiting[0]
                                    if usudsu < -1:
                                        try:
                                            context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    if usudsu12 < -1:
                                        try:
                                            context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    waiting_chat_ids.remove(partner_id)
                                    waiting_chat_ids.remove(chat_id)
                                    break
                                elif int(vip_status) == 0 and int(partner_vip_status) == 0:
                                    now = datetime.datetime.now()
                                    smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                    partner_pairs.append((partner_id, chat_id, smac))
                                    dirname = os.path.join(os.getcwd(), "chats", smac)

                                    if not os.path.exists(dirname):
                                        os.mkdir(dirname)

                                    if chat_id in admins and partner_id in admins:
                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif chat_id in admins:
                                        reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                        try:
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    elif partner_id in admins:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                        except:
                                            pass
                                    else:
                                        try:
                                            reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                            context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                            context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                        except:
                                            pass
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                    chat_id_result = cursor.fetchone()
                                    cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                    partner_result_reiting = cursor.fetchone()
                                    if chat_id_result:
                                        usudsu = chat_id_result[0]
                                    if partner_result_reiting:
                                        usudsu12 = partner_result_reiting[0]
                                    if usudsu < -1:
                                        try:
                                            context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    if usudsu12 < -1:
                                        try:
                                            context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                        except:
                                            pass
                                    waiting_chat_ids.remove(partner_id)
                                    waiting_chat_ids.remove(chat_id)
                                    break
                                    
            else:
                try:
                    context.bot.send_message(chat_id, "Похоже у вас мут попробуйте пойже")
                except:
                    pass
    elif "⚙Настойки⚙" == message:
        sasa = ""
        try:
            with sqlite3.connect(config.bd) as conn:
                cursor = conn.cursor()

            cursor.execute('SELECT gender FROM users WHERE id=?', (chat_id,))
            result = cursor.fetchone()

            if result:
                gender = result
            if str(gender) == "('M',)":
                sasa = "Ваш пол 'Мужской'"
            elif str(gender) == "('W',)":
                sasa = "Ваш пол 'Женский'"
        except:
            sasa = ""
        if chat_id in admins:
            keyboard = [
                        [InlineKeyboardButton("Пол", callback_data="pol")],
                        # [InlineKeyboardButton("Рассылка", callback_data="rassil")]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, "*Настройки*\n"+ str(sasa) +"\nВыберете пункт меню", reply_markup=reply_markup)
        else:
            keyboard = [
                        [InlineKeyboardButton("Пол", callback_data="pol")]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id, "*Настройки*\n"+ str(sasa) +"\nВыберете пункт меню", reply_markup=reply_markup)
    elif message == "Реферальная система💲":
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()
        cursor.execute('SELECT refers FROM users WHERE id=?', (chat_id,))
        result = cursor.fetchone()
        if result:
            refers_value = result[0]
        try:
            context.bot.send_message(chat_id, "Приветствую " + str(name1) + " ваша реферальная ссылка:\nhttps://t.me/anonymous_sova_bot?start=" + str(chat_id) + "\n\nВаши рефералы:"+ str(refers_value) + "\nДля того чтобы рефералы добавились реферал должен быть зарегистрирован в боте и обязательно подписан на канал бота не менее 3 часов!")
        except:
            pass
    elif message == "Следующий собеседник➡" and not chat_id in waiting_chat_ids:
        if not str(chat_id) in block:
            for sas in partner_pairs:
                if str(chat_id) in str(sas[0]):
                    partner = str(sas[1])
                    papa = sas
                    okey = 1
                elif str(chat_id) in str(sas[1]):
                    partner = str(sas[0])
                    papa = sas
                    okey = 1
            if okey == 1:
                passs = 0
                partner_pairs.remove(papa)
                for ocenk in ocenka:
                    if ocenk[1] == chat_id:
                        passs = 1
                        break
                    elif ocenk[0] == chat_id:
                        passs = 1
                        break
                if passs == 0:
                    ocenka.append((str(chat_id), str(partner)))
                    ocenka.append((str(partner), str(chat_id)))
                reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
                try:
                    context.bot.send_message(partner, "Ваш партнер завершил разговор с вами 😢", reply_markup=reply_markup)
                except:
                    pass
                keyboard = [
                    [InlineKeyboardButton("👍", callback_data="thumb_up"),
                    InlineKeyboardButton("👎", callback_data="thumb_down")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                try:
                    context.bot.send_message(partner, "Оцените вашего партнера", reply_markup=reply_markup)
                    context.bot.send_message(chat_id, "Оцените вашего партнера", reply_markup=reply_markup)
                    reply_markup = ReplyKeyboardMarkup([["❌Отменить поиск❌"]], resize_keyboard=True)
                    context.bot.send_message(chat_id, "Поиск нового собеседника подождите...", reply_markup=reply_markup)
                except:
                    pass
                with sqlite3.connect(config.bd) as conn:
                    cursor = conn.cursor()

                cursor.execute('SELECT gender, vip FROM users WHERE id=?', (chat_id,))
                result = cursor.fetchone()

                if result:
                    gender, vip_status = result
                if gender is None:
                    keyboard = [
                        [InlineKeyboardButton("Мужской", callback_data="M"),
                        InlineKeyboardButton("Женский", callback_data="W")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    context.bot.send_message(chat_id, "Перед началом общения пожалуйста укажите свой пол", reply_markup=reply_markup)
                else:
                    if str(chat_id) not in block:
                            reply_markup = ReplyKeyboardMarkup([["❌Отменить поиск❌"]], resize_keyboard=True)
                            try:
                                context.bot.send_message(chat_id, "Поиск собеседника", reply_markup=reply_markup)
                            except:
                                pass
                            waiting_chat_ids.append(chat_id)
                            if int(len(waiting_chat_ids)) > 1:
                                for partner_id in waiting_chat_ids:
                                    if partner_id != str(chat_id):  
                                        cursor.execute('SELECT gender, vip FROM users WHERE id=?', (partner_id,))
                                        partner_result = cursor.fetchone()

                                        if partner_result:
                                            partner_gender, partner_vip_status = partner_result
                                        if partner_id != chat_id:  
                                            if ((int(vip_status) == 1 and int(partner_vip_status) == 0) or (int(vip_status) == 0 and int(partner_vip_status) == 1)) and gender != partner_gender:
                                                now = datetime.datetime.now()
                                                smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                                partner_pairs.append((partner_id, chat_id, smac))
                                                dirname = os.path.join(os.getcwd(), "chats", smac)

                                                if not os.path.exists(dirname):
                                                    os.mkdir(dirname)

                                                if chat_id in admins and partner_id in admins:
                                                    reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif chat_id in admins:
                                                    reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif partner_id in admins:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                                chat_id_result = cursor.fetchone()
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                                partner_result_reiting = cursor.fetchone()
                                                if chat_id_result:
                                                    usudsu = chat_id_result[0]
                                                if partner_result_reiting:
                                                    usudsu12 = partner_result_reiting[0]
                                                if usudsu < -1:
                                                    try:
                                                        context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass
                                                if usudsu12 < -1:
                                                    try:
                                                        context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass

                                                waiting_chat_ids.remove(partner_id)
                                                waiting_chat_ids.remove(chat_id)
                                                break
                                            elif ((int(vip_status) == 1 and int(partner_vip_status) == 1) or (int(vip_status) == 1 and int(partner_vip_status) == 1)) and gender != partner_gender:
                                                now = datetime.datetime.now()
                                                smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                                partner_pairs.append((partner_id, chat_id, smac))
                                                dirname = os.path.join(os.getcwd(), "chats", smac)

                                                if not os.path.exists(dirname):
                                                    os.mkdir(dirname)

                                                if chat_id in admins and partner_id in admins:
                                                    reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif chat_id in admins:
                                                    reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif partner_id in admins:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                                chat_id_result = cursor.fetchone()
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                                partner_result_reiting = cursor.fetchone()
                                                if chat_id_result:
                                                    usudsu = chat_id_result[0]
                                                if partner_result_reiting:
                                                    usudsu12 = partner_result_reiting[0]
                                                if usudsu < -1:
                                                    try:
                                                        context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass
                                                if usudsu12 < -1:
                                                    try:
                                                        context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass
                                                waiting_chat_ids.remove(partner_id)
                                                waiting_chat_ids.remove(chat_id)
                                                break
                                            elif int(vip_status) == 0 and int(partner_vip_status) == 0:
                                                now = datetime.datetime.now()
                                                smac = f"{partner_id}_и_{chat_id}_{now.strftime('%d.%m.%Y_%H-%M-%S')}"
                                                partner_pairs.append((partner_id, chat_id, smac))
                                                dirname = os.path.join(os.getcwd(), "chats", smac)

                                                if not os.path.exists(dirname):
                                                    os.mkdir(dirname)

                                                if chat_id in admins and partner_id in admins:
                                                    reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['‍👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif chat_id in admins:
                                                    reply_markup32 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                    try:
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup32)
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                elif partner_id in admins:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        reply_markup12 = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"], ['👁‍🗨Данные пользователя👁‍🗨']], resize_keyboard=True)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup12)
                                                    except:
                                                        pass
                                                else:
                                                    try:
                                                        reply_markup = ReplyKeyboardMarkup([["Следующий собеседник➡", "Завершить разговор😢"]], resize_keyboard=True)
                                                        context.bot.send_message(chat_id, "Собеседник найден", reply_markup=reply_markup)
                                                        context.bot.send_message(partner_id, "Собеседник найден", reply_markup=reply_markup)
                                                    except:
                                                        pass
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (chat_id,))
                                                chat_id_result = cursor.fetchone()
                                                cursor.execute('SELECT reiting FROM users WHERE id=?', (partner_id,))
                                                partner_result_reiting = cursor.fetchone()
                                                if chat_id_result:
                                                    usudsu = chat_id_result[0]
                                                if partner_result_reiting:
                                                    usudsu12 = partner_result_reiting[0]
                                                if usudsu < -1:
                                                    try:
                                                        context.bot.send_message(partner_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass
                                                if usudsu12 < -1:
                                                    try:
                                                        context.bot.send_message(chat_id, "Внимание‼\nУ вашего собеседника минусовой рейтинг будте осторожны!")
                                                    except:
                                                        pass
                                                waiting_chat_ids.remove(partner_id)
                                                waiting_chat_ids.remove(chat_id)
                                                break
                                                    
                    else:
                        try:
                            context.bot.send_message(chat_id, "Похоже у вас мут попробуйте пойже")
                        except:
                            pass
    elif message == "Завершить разговор😢":
        passs = 0
        for sas in partner_pairs:
            if str(chat_id) in str(sas[0]):
                partner = str(sas[1])
                papa = sas
                okey = 1
            elif str(chat_id) in str(sas[1]):
                partner = str(sas[0])
                papa = sas
                okey = 1
        if okey == 1:
            partner_pairs.remove(papa)
            for ocenk in ocenka:
                if ocenk[1] == chat_id:
                    passs = 1
                    break
                elif ocenk[0] == chat_id:
                    passs = 1
                    break
            if passs == 0:
                ocenka.append((str(chat_id), str(partner)))
                ocenka.append((str(partner), str(chat_id)))
            reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
            try:
                context.bot.send_message(partner, "Ваш партнер завершил разговор с вами 😢", reply_markup=reply_markup)
            except:
                pass
            keyboard = [
                [InlineKeyboardButton("👍", callback_data="thumb_up"),
                InlineKeyboardButton("👎", callback_data="thumb_down")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            try:
                context.bot.send_message(partner, "Оцените вашего партнера", reply_markup=reply_markup)
                context.bot.send_message(chat_id, "Оцените вашего партнера", reply_markup=reply_markup)
                reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
                context.bot.send_message(chat_id, "Привет, если хочешь пообщаться, нажми кнопку 'Подобрать собеседника ❤️'\n\nЕсли у вас возникли проблемы или другие вопросы @sov_support_bot", reply_markup=reply_markup)
            except:
                pass
    elif message == "👑Vip👑":
        with sqlite3.connect(config.bd) as conn:
            cursor = conn.cursor()
        cursor.execute('SELECT vip FROM users WHERE id=?', (chat_id,))
        result = cursor.fetchone()
        if result:
            refers_value = result[0]
        if refers_value == 1:
            activ = "активна"
        elif refers_value == 0:
            activ = "не активна"
        keyboard = [
            [InlineKeyboardButton("Купить", callback_data="byee")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            context.bot.send_message(chat_id, "Ваша подписка сейчас " + activ + ".\n\nС подпиской vip вы можете получить\n-🔏защиту от мута🔏\n\n-👫полный фильтр по полу👫\n\n-🚫отключение рекламы🚫", reply_markup=reply_markup)
        except:
            pass
    elif not chat_id == None:
        message = update.message.text
        chat_id = update.message.chat_id
        id_user = update.message.chat.id
        member = update.message.from_user.username
        name21 = update.message.from_user.first_name
        okey = 0
        partner = None
        if not chat_id is None:
            for sas in partner_pairs:
                if str(chat_id) in str(sas[0]):
                    partner = str(sas[1])
                    papcka = str(sas[2])
                    okey = 1
                elif str(chat_id) in str(sas[1]):
                    partner = str(sas[0])
                    papcka = str(sas[2])
                    okey = 1
            
            if okey == 1:
                if update.message.text:
                    now = datetime.datetime.now()
                    suslik = now.strftime('%H-%M-%S')
                    sas333 = str(suslik) + str([chat_id]) + str((name21)) + str(message)
                    sas222 = str(suslik) + str([chat_id]) + str((name21)) +  str([member]) + str(message)
                    with open(str(os.getcwd()) + "\\chats\\"+papcka+"\\messages.txt", 'a', encoding='utf-8') as file:
                        if member == None:
                            file.write(str(sas333)+ '\n')
                        else:
                            file.write(str(sas222)+ '\n')
                    try:
                        context.bot.send_message(int(partner), message)
                    except:
                        pass
    else:
        try:
            reply_markup = ReplyKeyboardMarkup([["Подобрать собеседника ❤️", "Реферальная система💲"],["👑Vip👑"], ["⚙Настойки⚙"]], resize_keyboard=True)
            context.bot.send_message(chat_id, "Привет, если хочешь пообщаться, нажми кнопку 'Подобрать собеседника ❤️'\n\nЕсли у вас возникли проблемы или другие вопросы @sov_support_bot", reply_markup=reply_markup)
        except:
            pass

def main() -> None:
    TOKEN = config.TOKEN
    
    
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(MessageHandler(Filters.video, handle_video))
    dispatcher.add_handler(MessageHandler(Filters.voice, handle_voice))
    dispatcher.add_handler(MessageHandler(Filters.sticker, handle_sticker))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.audio, handle_audio))
    dispatcher.add_handler(MessageHandler(Filters.animation, handle_animation))
    dispatcher.add_handler(MessageHandler(Filters.caption, handle_caption))
    dispatcher.add_handler(MessageHandler(Filters.contact, handle_contact))
    dispatcher.add_handler(MessageHandler(Filters.game, handle_game))
    dispatcher.add_handler(MessageHandler(Filters.location, handle_location))
    dispatcher.add_handler(MessageHandler(Filters.video_note, handle_video_note))

    dispatcher.add_handler(CallbackQueryHandler(button_click))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
