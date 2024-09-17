import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to get video details
def get_video_details(video_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'dump_single_json': True,
        'noplaylist': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return {
            'download_link': info['url'],
            'thumbnail': info['thumbnail'],
            'title': info.get('title')
        }

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Send me a video URL, and I'll give you the download link.")

# Define the message handler to process URLs
async def handle_message(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    
    if not video_url:
        await update.message.reply_text("Please send a valid URL.")
        return
    
    try:
        details = get_video_details(video_url)
        response_message = f"Title: {details['title']}\nDownload Link: {details['download_link']}\nThumbnail: {details['thumbnail']}"
        await update.message.reply_text(response_message)
    except Exception as e:
        await update.message.reply_text(f"Please Enter a Valid URL")

def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = Application.builder().token("Token").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
