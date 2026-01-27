import telebot

from models import Base, User, UserStats
from database import engine, SessionLocal

from parser import parse_html, stats_formating


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bot = telebot.TeleBot("8121349204:AAGq1oY3grcGVT1cik3gHNGqkRm1Qttu9Ho", parse_mode=None) # init token

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        db = SessionLocal()
        new_user = User(username_telegram=message.from_user.username, telegram_id=message.from_user.id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
    bot.reply_to(message, "Привет, отправь мне никнейм своего аккауна codewars (/nick)")

@bot.message_handler(commands=['nick'])
def send_link(message):
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        if not user:
            bot.reply_to(message, "Сначала нужно использовать /start")
            return

    username = message.text.split()[1:]

    link = f"https://www.codewars.com/users/{''.join(username)}" # create link
    stats = parse_html(link) # get stats
    stats_dict = stats_formating(stats, message)
    user_stats = UserStats(
        user_id=user.id
        , **stats_dict
    )
    try:
        db = SessionLocal()
        db.add(user_stats)
        db.commit()
        db.refresh(user_stats)
    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()

    bot.reply_to(message, "Спасибо, теперь ты можешь свою статистику на сайте (/stats)")

bot.infinity_polling()