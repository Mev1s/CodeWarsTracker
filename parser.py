import telebot
from bs4 import BeautifulSoup
import requests

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bot = telebot.TeleBot("8121349204:AAGq1oY3grcGVT1cik3gHNGqkRm1Qttu9Ho", parse_mode=None) # init token

statistic = []

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, отправь мне никнейм своего аккауна codewars (/nick)")

@bot.message_handler(commands=['nick'])
def send_link(message):
    global link, username
    username = message.text.split()[1:]
    link = f"https://www.codewars.com/users/{''.join(username)}" # create link
    bot.reply_to(message, "Спасибо, теперь ты можешь свою статистику на сайте (/stats)")

def parse_html(link):
    htm = requests.get(link, headers)
    src = htm.text
    soup = BeautifulSoup(src, 'html.parser')
    stats = soup.find_all('div', class_='stat')
    for item in stats:
        statistic.append(item.get_text(strip=False))
    return statistic

print(parse_html("https://www.codewars.com/users/Mev1s"))

bot.infinity_polling()