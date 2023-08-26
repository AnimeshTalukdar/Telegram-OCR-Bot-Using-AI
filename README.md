# Telegram Chat Bot with AI
This is a Telegram chat bot that utilizes AI models for chat interactions and image processing. The bot can handle text messages, process images, and provide responses based on AI-generated content.

## Demo
Try it out at @ocrgptbot on Telegram

## Features
Responds to text messages with AI-generated content.
Processes images and provides responses based on the content of the images.
Supports authorized users and provides administrative commands.
Logs all received and sent messages to a chat log file.
## Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.6 or higher
Telegram Bot API token
OpenAI GPT API key
EasyOCR and Google Generative AI libraries
## Installation
Follow these steps to install and set up the project:

Clone the repository:


```bash
git clone https://github.com/AnimeshTalukdar/telegram-chat-bot.git
cd telegram-chat-bot
```
Install the required packages:


```bash
pip install -r requirements.txt
```
Set up your environment variables by renaming .env.example to .env and filling in your API keys.

## .env Template
Create a file named .env in the root directory of your project and fill it with the required API keys and variables:


```
# Telegram Bot API key
TELEGRAM_API_KEY=your_telegram_api_key_here

# OpenAI GPT API key
PALM_API_KEY=your_openai_gpt_api_key_here

# Your Telegram Chat ID (for admin purposes)
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```
Replace your_telegram_api_key_here, your_openai_gpt_api_key_here, and
your_telegram_chat_id_here with your actual API keys and chat ID.

## Usage
To run the project, follow these steps:

Run the bot:

``` bash
python bot.py
```
Interact with the bot through Telegram.

## Authorized Users
The bot can be configured to allow authorized users to interact with it.
The admin can add or remove authorized users using commands.
## Chat Log
All received and sent messages are logged to the chat_log.txt file.
The chat log includes timestamps, message types, user IDs, and message content.
## Commands
/adduser - Add an authorized user (admin only)
/removeuser - Remove an authorized user (admin only)
Contributing
Contributions are welcome! To contribute:

## Fork the repository
Create a new branch: git checkout -b feature/your-feature
Make your changes and commit them: git commit -m 'Add some feature'
Push to the branch: git push origin feature/your-feature
Create a pull request

