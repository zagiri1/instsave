import os
import json
import re
import time
import requests
import random
import tiktok_module
from requests import *
from datetime import datetime
from config import *

api = f"https://api.telegram.org/bot{token_bot}/"
update_id = 0
last_use = 1

def SendVideo(userid,msgid):
	res = post(f"{api}sendvideo",
    data={"chat_id":userid,
      "caption":"<b>✅ А вот и ваше видео!</b>\n\n<i>Если видео не работает, то пришлите ссылку заново</i>\n\n🔥 Видео скачано с помощью бота: @tikgobot",
      "parse_mode":"html",
      "reply_to_message_id":msgid,
      "reply_markup":json.dumps(
        {"inline_keyboard":[
          [
            {"text":"✉️ Связь с админом бота",
            "url":"https://t.me/qws1z"
            }
          ]
          ]
        }
      )},
    files={"video":open("video.mp4","rb")})

def SendMsg(userid,text,msgid):
	post(f"{api}sendmessage",
    json={
      "chat_id":userid,
      "text":text,
      "parse_mode":"html",
      "reply_to_message_id":msgid
    }
  )

def get_time(tt):
	ttime = datetime.fromtimestamp(tt)
	return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"

def Bot(update):
  try:
    global last_use
    userid = update['message']['chat']['id']
    pesan = update['message']['text']
    msgid = update['message']['message_id']
    timee = update['message']['date']
    if update['message']['chat']['type'] != "private":
      SendMsg(userid,"Bot only work in private chat !",msgid)
      return
    first_name = update['message']['chat']['first_name']
    print(f"{get_time(timee)}-> {userid} - {first_name} -> {pesan}")
    if pesan.startswith('/start'):
      SendMsg(userid,"<b>📥 Загрузчик видео с TikTok!</b>\n\nБот умеет скачивать видосики без логотипа «TikTok» и ссылки на автора видео\n\n<b>Как пользоваться?</b>\n1️⃣ Скопируйте ссылку на видео из TikTok\n<i>Не знаете как получить ссылку на видео? То жму сюда</i> \n\n2️⃣ Вставьте ссылку сюда в чат\n\n3️⃣ Немножко подождите и бот пришлёт вам видео, которое вы можете сохранить себе в память телефона",msgid)
    elif "tiktok.com" in pesan and "https://" in pesan :
      getvid = tiktok_module.Tiktok().musicallydown(url=pesan)
      if getvid == False:
        SendMsg(userid,"<i>Ошибка загрузки видео</i>\n\n<i>Попробуйте попозже</i>",msgid)
        return
      elif getvid == "private/removed":
        SendMsg(userid,"<i>Ошибка загрузки видео</i>\n\n<i>Видео приватное или удалено</i>",msgid)
      elif getvid == "file size is to large":
        SendMsg(userid,"<i>Ошибка загрузки видео</i>\n\n<i>Видео имеет большой размер</i>",msgid)
      else:
        SendVideo(userid,msgid)
    elif "/help" in pesan:
      SendMsg(userid,"<b>📥 Загрузчик видео с TikTok!</b>\n\nБот умеет скачивать видосики без логотипа «TikTok» и ссылки на автора видео\n\n<b>Как пользоваться?</b>\n1️⃣ Скопируйте ссылку на видео из TikTok\n<i>Не знаете как получить ссылку на видео? То жму сюда</i> \n\n2️⃣ Вставьте ссылку сюда в чат\n\n3️⃣ Немножко подождите и бот пришлёт вам видео, которое вы можете сохранить себе в память телефона",msgid)
    elif pesan.startswith("/admin"):
      SendMsg(userid,"Связь с админом бота: https://t.me/qws1z",msgid)
  except KeyError:
    return
