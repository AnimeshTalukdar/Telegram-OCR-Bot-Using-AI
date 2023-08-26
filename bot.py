import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import google.generativeai as palm
import easyocr

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
PALM_API = os.getenv('PALM_API_KEY')
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

AUTHORIZED_USERS = [int(TELEGRAM_CHAT_ID)]

with open("authorized_users.txt", "r") as f:
    AUTHORIZED_USERS.extend([int(line.strip().split()[0]) for line in f])

palm.configure(api_key=PALM_API)
reader = easyocr.Reader(['en'])

UNAUTHORIZED_LIMIT = 5  # Number of prompts for unauthorized users
unauthorized_users_prompts = {}  # Dictionary to track unauthorized user prompts

def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# Log received and sent messages
def log_message(message, chat_id, message_type="Received"):
    with open("chat_log.txt", "a") as f:
        f.write(f"{message_type} message from {chat_id}: {message}\n")

    

async def handle_image(update: Update, context):
    chat_id = update.message.chat_id
    

    if not is_authorized(chat_id):
        if chat_id in unauthorized_users_prompts:
            if unauthorized_users_prompts[chat_id] >= UNAUTHORIZED_LIMIT:
                logger.info(f"Unauthorized user {chat_id} exceeded prompt limit")
                await update.message.reply_text("You've exceeded the prompt limit.")
                return
            else:
                unauthorized_users_prompts[chat_id] += 1
        else:
            unauthorized_users_prompts[chat_id] = 1

        logger.info(f"Handling image from unauthorized user {chat_id}")


    file = await update.message.photo[-1].get_file()
    await file.download_to_drive('download.jpg')

    text = reader.readtext('download.jpg')
    log_message(text, chat_id, message_type="Received Image")

    prompt = " ".join([i[1] for i in text])
    prompt += "try to find a question in this text blob and answer it if you feel like there is a question with 3 or 4 options try to reply with just the correct option"

    response = palm.chat(
        model="models/chat-bison-001",
        prompt=prompt,
        temperature=0.9,
    )

    for message in response.candidates:
        await update.message.reply_text(message['content'])

    log_message(response.candidates[0]['content'], chat_id, message_type="Sent")
async def handle_text(update: Update, context):
    chat_id = update.message.chat_id

    log_message(update.message.text, chat_id, message_type="Received")

    if not is_authorized(chat_id):
        logger.info(f"Unauthorized access from user {chat_id}")
        await update.message.reply_text('Not Authorized')
        return

    logger.info(f"Handling text from user {chat_id}")

    prompt = update.message.text

    response = palm.chat(
        model="models/chat-bison-001",
        prompt=prompt,
        temperature=0.9,
    )

    for message in response.candidates:
        await update.message.reply_text(message['content'])

    log_message(response.candidates[0]['content'], chat_id, message_type="Sent")

    

        
# Command handler for adding authorized users
async def add_user(update: Update, context):
    admin_chat_id = int(TELEGRAM_CHAT_ID)
    user_id_to_add = update.message.from_user.id

    if update.message.chat_id == admin_chat_id:
        if user_id_to_add not in AUTHORIZED_USERS:
            AUTHORIZED_USERS.append(user_id_to_add)
            await update.message.reply_text(f"User {user_id_to_add} has been added as an authorized user.")
        else:
            await update.message.reply_text(f"User {user_id_to_add} is already an authorized user.")
    else:
        await update.message.reply_text("Only the admin can use this command.")

# Command handler for removing authorized users
async def remove_user(update: Update, context):
    admin_chat_id = int(TELEGRAM_CHAT_ID)
    user_id_to_remove = update.message.from_user.id

    if update.message.chat_id == admin_chat_id:
        if user_id_to_remove in AUTHORIZED_USERS:
            AUTHORIZED_USERS.remove(user_id_to_remove)
            await update.message.reply_text(f"User {user_id_to_remove} has been removed as an authorized user.")
        else:
            await update.message.reply_text(f"User {user_id_to_remove} is not an authorized user.")
    else:
        await update.message.reply_text("Only the admin can use this command.")


def main():
    # Load unauthorized users' prompt count from the file
    try:
        with open("unauthorized_users.txt", "r") as f:
            for line in f:
                user_id = int(line.strip())
                unauthorized_users_prompts[user_id] = 0
    except FileNotFoundError:
        pass

    app = Application.builder().token(TELEGRAM_API_KEY).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.add_handler(CommandHandler("adduser", add_user))  # Command to add authorized user
    app.add_handler(CommandHandler("removeuser", remove_user))  # Command to remove authorized user
    app.run_polling()

if __name__ == "__main__":
    main()
