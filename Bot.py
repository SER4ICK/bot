import logging
import shelve
import requests
from collections import defaultdict
from config import BOT_KEY
from api import gpt, image
from enum import Enum
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class ModelEnum(Enum):
    gpt_text = 1
    gpt_image = 2


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    user_name = user.full_name
    pandora = shelve.open("pandora")
    if str(user_id) not in pandora.keys():
        user_data = {
            "user_name": user_name,
            "subs": "Free",
            "tokens": 0,
            "model": ModelEnum.gpt_text.value
        }
        pandora[str(user_id)] = user_data
    await update.message.reply_html (rf"Ку {pandora[str(user_id)]["user_name"]}")
    pandora.close()

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_id =str(user.id)
        pandora = shelve.open("pandora")
        subscription_type = pandora[str(user_id)]["subs"]
        tokens = pandora[str(user_id)]['tokens']
        name = pandora[str(user_id)]['user_name']
        profile_text = (
            f"Это ваш профиль. \n"
            f"Имя: {name}.\n"
            f"ID {user_id}\n"
            f"Подписка {subscription_type}\n\n"
        )
        await update.message.reply_text(profile_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Чтобы начать, пиши /start \n"
        "За помощью пиши /help \n"
    )
    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_text)

async def store (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добро пожаловать в магазин, сколько токенов хочешь купить?")



async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    pandora = shelve.open("pandora")
    tokens = pandora[user_id]["tokens"]
    gpt_model = pandora[user_id]["model"]
    if tokens > 0:
        if gpt_model == ModelEnum.gpt_text.value:
         message = update.message.text
         answer = gpt(message)
         await update.message.reply_text(answer)
    if gpt_model == ModelEnum.gpt_image.value:
        message = update.message.text
        answer = image(message)
        await update.message.reply_photo(
            photo=answer[0],
            caption=answer[1]
        )

    else:
     mess = "пополните баланс токенов в /store"
     await update.message.reply_text(mess)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("8042103513:AAEloBMj2VaUhYcFQApDKrNkHIZy61xf5m4").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("store", store))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()