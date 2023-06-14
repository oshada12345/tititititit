import os
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import tiktok_downloader

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define a global variable to store user information
user_info = {}

# Command handler for /start
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to TikTok Download Bot!")

# Command handler for /download
def download(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    chat_id = update.effective_chat.id
    
    # Get the TikTok video URL from the message
    video_url = message.split(' ')[1]
    
    # Download the TikTok video
    video_path, audio_path = tiktok_downloader.download(video_url)
    
    # Send the downloaded video and audio as files
    context.bot.send_video(chat_id=chat_id, video=open(video_path, 'rb'))
    context.bot.send_audio(chat_id=chat_id, audio=open(audio_path, 'rb'))

# Command handler for /broadcast
def broadcast(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    
    # Check if the user is authorized to use the /broadcast command
    user_id = update.effective_user.id
    if user_id not in user_info['admins']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")
        return
    
    # Get the message to broadcast
    broadcast_message = message.split(' ', 1)[1]
    
    # Send the broadcast message to all users
    for user_id in user_info['users']:
        context.bot.send_message(chat_id=user_id, text=broadcast_message)

# Command handler for /view_broadcast
def view_broadcast(update: Update, context: CallbackContext) -> None:
    # Check if the user is authorized to view the broadcast messages
    user_id = update.effective_user.id
    if user_id not in user_info['users']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")
        return
    
    # Get the broadcast messages
    broadcast_messages = user_info['broadcast_messages']
    
    # Send the broadcast messages as a single string
    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(broadcast_messages))

# Message handler for regular messages
def handle_message(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command. Please use /start, /download, /broadcast, or /view_broadcast.")

def main() -> None:
    # Load user information from a file or a database
    # Here, we initialize it with dummy values for demonstration purposes
    user_info['admins'] = [5310455183]  # List of admin user IDs
    user_info['users'] = set()         # Set of user IDs
    user_info['broadcast_messages'] = []  # List to store broadcast messages
    
    # Set up the Telegram bot
    token = '6043054287:AAGwCMEOTcY0d7N-s8JtnQ9HUFYOQG-pWzQ'
    bot = telegram.Bot(token=token)
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    download_handler = CommandHandler('download', download)
    dispatcher.add_handler(download_handler)
    
    broadcast_handler = CommandHandler('broadcast', broadcast)
    dispatcher.add_handler(broadcast_handler)
    
    view_broadcast_handler = CommandHandler('view_broadcast', view_broadcast)
    dispatcher.add_handler(view_broadcast_handler)
    
    # Add message handler for regular messages
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
