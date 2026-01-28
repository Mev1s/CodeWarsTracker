import telebot

from models import Base, User, UserStats
from database import engine, SessionLocal

from parser import parse_html, stats_formating
import psycopg2


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

conn = psycopg2.connect(
    dbname="codewars_tracker",
    user="postgres",
    password="Teraser0000Pro",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

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
    stats_dict = stats_formating(stats)
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

@bot.message_handler(commands=['stats'])
def send_stats(message):
    with SessionLocal() as db:
        cursor.execute("""
                       SELECT followers, allies, leaders_board, honor_percentile, honor, rank, total_completed
                       FROM user_stats
                       WHERE user_id = (SELECT id
                                        FROM users
                                        WHERE telegram_id = %s)
                       """, (message.from_user.id,))
        user = cursor.fetchone()
        msg = (f"🙂 Followers: {user[0]}\n"
               f"😳 Allies: {user[1]}\n"
               f"📑 Leaders Board: {user[2]}\n"
               f"📃 Honor Percentile: {user[3]}\n"
               f"🪄 Rank: {user[4]}\n"
               f"📔 Total Completed: {user[5]}")
        bot.reply_to(message, msg)

@bot.message_handler(commands=['leaders'])
def send_leaders(message):
    with SessionLocal() as db:
        cursor.execute("""
                SELECT users.username_telegram, user_stats.honor FROM user_stats INNER JOIN users ON users.id = user_stats.user_id ORDER BY user_stats.honor DESC LIMIT 10
        """)
        user = cursor.fetchall()
        msg = ""
        for ind, us in enumerate(user):
            us = str(us).replace("'", '').strip('()').replace(',', ':')
            msg += f"{ind + 1}. {us} чести\n"
        bot.reply_to(message, msg)

bot.infinity_polling()