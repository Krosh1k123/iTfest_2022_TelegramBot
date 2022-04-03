from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import requests
import sqlite3 as sq
import os

token_bot = "5096580905:AAFSccbzJmY49vOTxzdPBusRzDAxmUzXJhg"
token_vk = "12c1364a9d426d4c3a654bd1d279e4953df572a80f4b9aed00b4e3c9f2cd8de242dd3c3630368e0d0546c"
bot = Bot(token_bot)
db = Dispatcher(bot)
#Кнопки на клавиатуре
# b1 = KeyboardButton("fitnessed")
# b2 = KeyboardButton("azbukaxaypa")
#
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_client.insert(b1).insert(b2)


# Парсер вк, выход url на img
# Передаем название группы vk.com/fitnessed = fitnessed
def get_wall_posts():
    group_name = "azbukaxaypa"
    posts_urls = []
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token_vk}&v=5.81"
    req = requests.get(url)
    src = req.json()
    # собираем ID новых постов в список
    fresh_posts_id = []
    posts_ids=[]
    posts = src["response"]["items"]
    if os.path.exists("Memes"):
        print("Указанный файл существует")
    else:
        os.mkdir("Memes")

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

        # извлекаем данные из постов
    i = 0
    for post in posts:
        #Сохраняем фотки
        def download_img(url, post_id, group_name):
            res = requests.get(url)

            # создаем папку group_name/files
            if not os.path.exists(f"Memes/files"):
                os.mkdir(f"Memes/files")

            with open(f"Memes/files/{post_id}.jpg", "wb") as img_file:
                img_file.write(res.content)

        # пробуем извелкать ссылку с фото
        try:
            post_id = post["id"]
            if "attachments" in post:
                post = post["attachments"]

                photo_quality = dict(m=0, o=1, p=2, q=3, r=4, s=5, w=6, x=7, y=8, z=9)
                if len(post) == 1:
                    # забираем фото
                    if post[0]["type"] == "photo":
                        for pq in photo_quality:
                            if pq in post[0]["photo"]["sizes"][i]["type"]:
                                post_photo = post[0]["photo"]["sizes"][photo_quality[pq]]["url"]
                                download_img(post_photo, post_id, group_name)
                                posts_urls.append(post_photo)
                                posts_ids.append(post_id)
                                break
        except Exception:
            pass
    clear_urls = [[0] * 2 for i in range(len(posts_urls))]
    for i in range(len(posts_urls)):
        clear_urls[i][0] = posts_ids[i]
        clear_urls[i][1] = posts_urls[i]
    print(clear_urls)
    return clear_urls



# База данных
# def sql_start():
#     global base, cur
#     base = sq.connect('Vk_bt.db')  # Подключаемся к БД
#     cur = base.cursor()  # Создаем курсор
#     if base:
#         print("Data base connected Ok!")
#     base.execute("CREATE TABLE IF NOT EXISTS posts(url TEXT)")
#     base.commit()
#     cur.execute("INSERT INTO posts VALUES (?, ?)", (get_wall_posts()))
#     base.commit()



# async def sql_add_command(state):
#     async with state.proxy() as data:
#         cur.execute("INSERT INTO posts VALUES (?)", (get_wall_posts("azbukaxapa")))


# -------------------------теория-------------------------
# ====Методы====
# await message.answer(message.text) пишет сообещение
# await message.reply(message.text) отвечает на сообщение
# await bot.send_message(message.from_user.id, message.text) # отправляет сообщение в лс
# ==============
# ==Декораторы==
# @db.message_handler() Декоратор который улачливает все сообщения, которые дошли до него (Неважно лс это или группа)
# @db.message_handler(commands=['start','help']) Реагирует на команды start help (пример сообщения: /start)
# ==============
# ==Клавиатура и Кнопки==

# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) kb_client.insert(b1).insert(b2) await
# bot.send_message(message.from_user.id, "Привет! Я твой личный бот, выбери темы которые ты  любишь!",
# reply_markup=kb_client

# BD


# =======================
# --------------------------------------------------------ъ
# Нужно для вывода текста в консоль и подключения БД
async def on_startup(_):
    get_wall_posts()
    print("Бот в онлайн")


@db.message_handler(commands=['start', 'help'])
async def comands_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет! Я твой личный бот, выбери темы которые ты  любишь!")\

@db.message_handler(commands=['Memes'])
async def comands_start(message: types.Message):
    posts_wall = get_wall_posts()
    for n in range(len(posts_wall)):
        print(posts_wall[n][0])
        photo = open(f"Memes/files/{posts_wall[n][0]}.jpg", "rb")  # rb - чтение байтов, wb - запись байтов.
        await bot.send_photo(message.from_user.id, photo)



executor.start_polling(db, skip_updates=True, on_startup=on_startup)
