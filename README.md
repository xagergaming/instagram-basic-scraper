# Instagram Basic Scraper

This tool is a simple and powerful Instagram scraper built using Python, `telebot`, and `instaloader`. It allows users to scrape various data such as posts, bios, and hashtags from both public and private profiles through a Telegram bot interface. Users can select what they want to scrape with easy-to-use Telegram commands.

## Features

- **Scrape Public Profiles**: Scrape Instagram data from public profiles by providing the username.
- **Scrape Private Profiles**: Scrape data from private profiles (you need to be following the private account).
- **Scrape Posts**: Download all posts from an Instagram profile.
- **Scrape Hashtags**: Scrape all posts from a specific hashtag.
- **Scrape Bio**: Extract the bio information from any Instagram profile.
- **Scrape All Data**: Get all available details from a profile, including bio, follower counts, following counts, and posts.
- **Stop Scraping**: Use the `/stop` command or "Stop Scraping" button to stop scraping at any point.
- **Customizable**: Modify the code to suit your scraping needs, including adding more scraping functionalities or altering the bot’s behavior.

## Getting Started

### Requirements

1. Python 3.x
2. Telegram Bot API Token
3. Instaloader
4. Requests
5. Telebot (`pyTelegramBotAPI`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/xagergaming/instagram-basic-scraper.git
    cd instagram-basic-scraper
    ```

2. Install the required Python libraries:
    ```bash
    pip install instaloader pyTelegramBotAPI requests
    ```

3. Create a Telegram bot and obtain an API token:
   - Talk to [@BotFather](https://telegram.me/BotFather) on Telegram.
   - Follow the steps to create a bot and get the API token.

4. Replace the token in the code:
    ```python
    bot = telebot.TeleBot("YOUR_TELEGRAM_BOT_API_TOKEN")
    ```

5. Run the script:
    ```bash
    python scraper.py
    ```

6. Start chatting with your bot on Telegram and use the following commands:

### Available Commands

- **`/start`**: Starts the bot and lets you choose between scraping a public or private profile.
- **`/private`**: Prompts you to enter the Instagram username of a private profile.
- **`/public`**: Prompts you to enter the Instagram username of a public profile.
- **`/posts`**: Scrapes and downloads all posts from the selected profile.
- **`/hashtag`**: Prompts you to enter a hashtag and scrapes all posts associated with that hashtag.
- **`/bio`**: Scrapes and returns the bio of the selected profile.
- **`/all`**: Scrapes the entire profile (bio, posts, follower/following counts).
- **`/stop`**: Stops the current scraping process.

### Example Usage

1. Start the bot on Telegram with `/start`.
2. Choose whether the profile is **public** or **private**.
3. Enter the username of the profile.
4. Choose what to scrape by selecting `/posts`, `/hashtag`, `/bio`, or `/all`.
5. The scraped data (photos, videos, bio, etc.) will be sent to your Telegram chat.

## Customization

You can modify this tool to suit your needs. Here are a few common changes you might want to make:

### 1. Change the Scraping Options

You can edit the buttons or options users select after setting the profile type. Modify the code in `create_scraping_options_keyboard` to add or remove scraping options:
```python
def create_scraping_options_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('/all')
    btn2 = types.KeyboardButton('/posts')
    btn3 = types.KeyboardButton('/hashtag')
    btn4 = types.KeyboardButton('/bio')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
