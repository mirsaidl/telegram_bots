import requests
import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Initialize your bot with the Telegram API token
bot = telebot.TeleBot("Telegram API")

# Function to fetch yesterday's and today's matches
def get_matches(date):
    url = f'https://api.football-data.org/v4/matches?date={date}'
    headers = {'X-Auth-Token': "API"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Function to format a single match
def format_match(match):
    home_team_name = match["homeTeam"]["name"]
    away_team_name = match["awayTeam"]["name"]
    home_score = match["score"]["fullTime"]["home"]
    away_score = match["score"]["fullTime"]["away"]
    winner = "Draw" if home_score == away_score else (home_team_name if home_score > away_score else away_team_name)
    match_info = f"{home_team_name} {home_score} - {away_score} {away_team_name}\nWinner: {winner}"
    return match_info


# Function to format all matches
def format_matches(matches):
    formatted_matches = []
    for match in matches:
        formatted_match = format_match(match)
        formatted_matches.append(formatted_match)
    return "\n\n".join(formatted_matches)

# Function to handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Yesterday's Matches", callback_data='yesterday'),
                 InlineKeyboardButton("Today's Matches", callback_data='today'))
    bot.send_message(message.chat.id, "Please choose:", reply_markup=keyboard)

# Function to handle button clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'yesterday':
        yesterday_matches = get_matches("YESTERDAY")["matches"]
        formatted_matches = format_matches(yesterday_matches)
        bot.send_message(call.message.chat.id, formatted_matches)
    elif call.data == 'today':
        today_matches = get_matches("TODAY")["matches"]
        formatted_matches = format_matches(today_matches)
        bot.send_message(call.message.chat.id, formatted_matches)

# Start the bot
bot.polling()


