import time
import requests
from requests.exceptions import ReadTimeout
import telebot
import instaloader
from telebot import types
from io import BytesIO

# Initialize Instaloader and TeleBot instances
L = instaloader.Instaloader()
bot = telebot.TeleBot("ENTER YOUR BOT'S API TOKEN")

# Global variables to store user input and scraping status
pvt_username = None
username = None
hashtag = None
stop_scraping = False

def create_stop_button():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    stop_button = types.KeyboardButton("Stop Scraping")
    keyboard.add(stop_button)
    return keyboard

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('/private')
    btn2 = types.KeyboardButton('/public')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Choose profile type:", reply_markup=markup)

# Handle private profile command
@bot.message_handler(commands=['private'])
def ask_private_username(message):
    msg = bot.reply_to(message, "Enter the private Instagram username:")
    bot.register_next_step_handler(msg, set_private_username)

def set_private_username(message):
    global pvt_username
    pvt_username = message.text
    bot.send_message(message.chat.id, """Private profile set! 
        Now choose what to scrape using
            /all        -->  Scrape whole profile
            /posts      -->  Scrape only posts of profile
            /hashtag    -->  Scrape only #tags of profile
            /bio        -->  Scrape only bio
        created & coded by ( Ahmed Bhai ) @tipsandgamer """)  
# Handle public profile command
@bot.message_handler(commands=['public'])
def ask_public_username(message):
    msg = bot.reply_to(message, "Enter the public Instagram username:")
    bot.register_next_step_handler(msg, set_public_username)

def set_public_username(message):
    global username
    username = message.text
    bot.send_message(message.chat.id, """Public profile set! 
        Now choose what to scrape using
            /all        -->  Scrape whole profile
            /posts      -->  Scrape only posts of profile
            /hashtag    -->  Scrape only #tags of profile
            /bio        -->  Scrape only bio
        created & coded by ( Ahmed Bhai ) @tipsandgamer """)

# Command to stop scraping
@bot.message_handler(commands=['stop'])
def stop_scraping_command(message):
    global stop_scraping
    stop_scraping = True
    bot.send_message(message.chat.id, "Scraping process has been stopped.", reply_markup=types.ReplyKeyboardRemove())

# Command to scrape all posts
@bot.message_handler(commands=['posts'])
def scrape_posts(message):
    if not username and not pvt_username:
        bot.send_message(message.chat.id, "Please set a username first using /private or /public.")
        return
    global stop_scraping
    stop_scraping = False  # Reset stop flag
    try:
        target_profile = username if username else pvt_username
        profile = instaloader.Profile.from_username(L.context, target_profile)
        bot.send_message(message.chat.id, f"Scraping posts from {target_profile}...")
        for post in profile.get_posts():
            if stop_scraping:
                bot.send_message(message.chat.id, "Scraping stopped.")
                return
            caption = post.caption if post.caption else ""
            if post.is_video:
                video_url = post.video_url
                response = requests.get(video_url)
                video_file = BytesIO(response.content)
                bot.send_video(message.chat.id, video_file, caption=caption)
            else:
                image_url = post.url
                response = requests.get(image_url)
                image_file = BytesIO(response.content)
                bot.send_photo(message.chat.id, image_file, caption=caption)
        bot.send_message(message.chat.id, f"Downloaded all posts from {target_profile}.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to download posts: {e}")

# Command to scrape specific hashtag
@bot.message_handler(commands=['hashtag'])
def ask_hashtag(message):
    msg = bot.reply_to(message, "Enter the hashtag to scrape:")
    bot.register_next_step_handler(msg, scrape_hashtag)

def scrape_hashtag(message):
    global hashtag
    hashtag = message.text
    global stop_scraping
    stop_scraping = False  # Reset stop flag
    try:
        bot.send_message(message.chat.id, f"Scraping posts for hashtag #{hashtag}...")
        for post in instaloader.Hashtag.from_name(L.context, hashtag).get_posts():
            if stop_scraping:
                bot.send_message(message.chat.id, "Scraping stopped.")
                return
            caption = post.caption if post.caption else ""
            if post.is_video:
                video_url = post.video_url
                response = requests.get(video_url)
                video_file = BytesIO(response.content)
                bot.send_video(message.chat.id, video_file, caption=caption)
            else:
                image_url = post.url
                response = requests.get(image_url)
                image_file = BytesIO(response.content)
                bot.send_photo(message.chat.id, image_file, caption=caption)
        bot.send_message(message.chat.id, f"Downloaded all posts for hashtag #{hashtag}.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to download posts for hashtag #{hashtag}: {e}")

# Command to scrape bio
@bot.message_handler(commands=['bio'])
def scrape_bio(message):
    if not username and not pvt_username:
        bot.send_message(message.chat.id, "Please set a username first using /private or /public.")
        return
    global stop_scraping
    stop_scraping = False  # Reset stop flag
    try:
        target_profile = username if username else pvt_username
        profile = instaloader.Profile.from_username(L.context, target_profile)
        bio = profile.biography
        bot.send_message(message.chat.id, f"Bio for {target_profile}:\n{bio}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to scrape bio: {e}")

# Command to scrape all details
@bot.message_handler(commands=['all'])
def scrape_all(message):
    if not username and not pvt_username:
        bot.send_message(message.chat.id, "Please set a username first using /private or /public.")
        return
    global stop_scraping
    stop_scraping = False  # Reset stop flag
    try:
        target_profile = username if username else pvt_username
        profile = instaloader.Profile.from_username(L.context, target_profile)
        bot.send_message(message.chat.id, f"Scraping all details from {target_profile}...")

        # Scrape and send bio
        bio = profile.biography
        bot.send_message(message.chat.id, f"""Bio: 
                         {bio}""")
        
        # Scrape and send follower/following count
        followers = profile.followers
        followees = profile.followees
        bot.send_message(message.chat.id, f"""Followers: 
                         {followers}\nFollowing: 
                         {followees}""")
        
        # Scrape and download posts
        for post in profile.get_posts():
            if stop_scraping:
                bot.send_message(message.chat.id, "Scraping stopped.")
                return
            caption = post.caption if post.caption else ""
            if post.is_video:
                video_url = post.video_url
                response = requests.get(video_url)
                video_file = BytesIO(response.content)
                bot.send_video(message.chat.id, video_file, caption=caption)
            else:
                image_url = post.url
                response = requests.get(image_url)
                image_file = BytesIO(response.content)
                bot.send_photo(message.chat.id, image_file, caption=caption)
        bot.send_message(message.chat.id, "Downloaded all posts.")

    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to download details: {e}")

# Start polling
while True:
    try:
        bot.polling(timeout=60)
    except ReadTimeout:
        print("Read timeout occurred. Retrying...")
        time.sleep(5)  # Wait before retrying
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)  # Wait before retrying
