from register import *
from database import *
import globals
from telegram import KeyboardButton,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Updater

db = Database("db-evos.db")
@check_data_decorator
def message_handler(update,context):
    user = update.message.from_user
    message = update.message.text
    db_user = db.get_user_by_chat_id(user.id)
    state = context.user_data.get("state",0)
    if state == 0:
        check(update,context)
    elif state == 1:
        if not db_user['lang_id']:
            if message == globals.BTN_LANG_UZ:
                db.update_user_data(user.id,"lang_id",1)
                check(update,context)
            elif message == globals.BTN_LANG_RU:
                db.update_user_data(user.id,"lang_id",2)
                check(update,context)
            else:
                update.message.reply_text(
                    text=globals.TEXT_LANG_WARNING
                )
        elif not db_user['first_name']:
            db.update_user_data(user.id,"first_name",message)
            check(update,context)
        elif not db_user['last_name']:
            db.update_user_data(user.id,"last_name",message)
            buttons = [
                [KeyboardButton(text=globals.BTN_SEND_CONTACT[db_user['lang_id']],request_contact=True)]
            ]
            check(update,context)
        elif not db_user['phone_number']:
            db.update_user_data(user.id,"phone_number",message)
            check(update,context)
        else:
            check(update,context)
    elif state == 2:
        if message == globals.SEND_FAYL[db_user['lang_id']]:
            user_id = update.message.from_user.id
            user = update.message.from_user
            db_user = db.get_user_by_chat_id(user.id)
            if user_id == db_user['chat_id']:
                # "file_patch" jildida eng so'nggi faylni toping
                file_dir = "file_patch"
                files = os.listdir(file_dir)
                files = [os.path.join(file_dir, file) for file in files]
                latest_file = max(files, key=os.path.getctime)

                # Update the send_file_path variable

                # To'g'ri fayl yo'lini qator sifatida taqdim eting
                send_file_path = latest_file

                # Faylni Telegram guruhiga yuborish
                group_chat_id = -1002056081927  # Replace with your actual group chat ID
                send_file_to_group(context.bot, group_chat_id, send_file_path,
                                   caption=f"Ati: {db_user['first_name']}\nFamiliyasi: {db_user['last_name']}\nTelefon nomeri: {db_user['phone_number']}")
        elif message == globals.WRITE[db_user['lang_id']]:
            update.message.reply_text(
                text=globals.LITE_WRITE[db_user['lang_id']],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            send_message = []
            user_info = f"Muraajat haqinda:\nAti: {db_user['first_name']}\nFamiliyasi: {db_user['last_name']}\nTelefon nomeri: {db_user['phone_number']}"
            send_message.append(user_info)
            send_message.append(update.message.text)
            final_message = '\n'.join(send_message)
            context.bot.send_message(chat_id=-1002056081927, text=final_message)

