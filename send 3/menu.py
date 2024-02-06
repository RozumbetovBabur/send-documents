from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime
import globals
from database import *
sent_documents = []
import os
db = Database("db-evos.db")

# Agar sizda faylni jo'natish funksiyasi mavjud deb hisoblasangiz
def send_file_to_group(bot, chat_id, file_path, caption=""):
    with open(file_path, "rb") as file:
        bot.send_document(chat_id, document=file, caption=caption)
def send_file(update,context):
    chat_id = update.message.chat_id
    file_path = "file_patch/Welcome.docx"
    context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
def send_main_menu(update, context):
    state = context.user_data.get("state", 0)
    user = update.message.from_user
    db_user = db.get_user_by_chat_id(user.id)
    if state == globals.STATES["menu"]:
        buttons = [
            [KeyboardButton(text=globals.SEND_FAYL[db_user['lang_id']]),
             KeyboardButton(text=globals.WRITE[db_user['lang_id']])]
        ]
        update.message.reply_text(
            text=globals.HOME[db_user['lang_id']],
            reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True)
        )

def receive_file(update,context):
    chat_id = update.message.chat_id
    # Qabul qilingan faylni saqlash joylashuvi
    file = context.bot.get_file(update.message.document.file_id)
    file_path = f'file_patch/{update.message.document.file_name}'
    file.download(file_path)
    update.message.reply_text(f"Fayl qabul qilindi ha'm saqlandi: {file_path}")

