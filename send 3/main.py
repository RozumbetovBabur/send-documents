from telegram.ext import Updater,MessageHandler,CommandHandler,CallbackQueryHandler,Filters
from database import *
import globals
db = Database("db-evos.db")
from register import *
from messages import *

token = XXXXXXXXXXXXXX

def start_handler(update,context):
    check(update,context)


def inline_handler(update,context):
    pass
def contact_handler(update,context):
    message = update.message.contact.phone_number
    user = update.message.from_user
    db.update_user_data(user.id,"phone_number",message)
    check(update,context)

def main():
    update = Updater(token=token)
    dispatcher = update.dispatcher

    dispatcher.add_handler(CommandHandler("start",start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text,message_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))
    receive_file_handler = MessageHandler(Filters.document, receive_file)
    dispatcher.add_handler(receive_file_handler)

    update.start_polling()
    update.idle()

if __name__ == "__main__":
    main()