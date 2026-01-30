import telebot

from models import Base, User, UserStats
from database import engine, SessionLocal, db_add

from parser import parse_html, stats_formating
import psycopg2


Base.metadata.create_all(bind=engine)

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
        db_add(new_user)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
    bot.reply_to(message, "Привет, отправь мне никнейм своего аккауна codewars (/nick)")

@bot.message_handler(commands=['nick'])
def send_link(message):
    with SessionLocal() as db:
        cursor.execute("""
                    SELECT telegram_id FROM users WHERE telegram_id = %s
        """, (message.from_user.id,))
        user = cursor.fetchone()
        if not user:
            bot.reply_to(message, "Сначала нужно использовать /start")
            return

    username = "".join(message.text.split()[1:])

    link = f"https://www.codewars.com/users/{username}" # create link

    cursor.execute("""
                    UPDATE users SET username_codewars = %s
                    WHERE telegram_id = %s
    """, (username, message.from_user.id,))
    conn.commit()

    stats = parse_html(link) # get stats
    stats_dict = stats_formating(stats) # new format

    cursor.execute("""
            SELECT COUNT(user_id) FROM user_stats WHERE user_id = (SELECT id FROM users WHERE telegram_id = %s)
                  """, (message.from_user.id,))
    new_user = cursor.fetchone()

    if new_user[0] > 1:
        bot.reply_to(message, "Статистика уже есть, напиши /stats")
        return 100

    cursor.execute("""
                    INSERT INTO user_stats (user_id, followers, allies, leaders_board, honor_percentile, honor, rank, total_completed)
                    VALUES ((SELECT id FROM users WHERE telegram_id = %(user_id)s),
                           %(followers)s, %(allies)s, %(leaders_board)s, %(honor_percentile)s, %(honor)s, %(rank)s, %(total_completed)s)
    """, {**stats_dict, "user_id": message.from_user.id})
    try:
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

    finally:
        db.close()

    bot.reply_to(message, "Спасибо, теперь ты можешь свою статистику на сайте (/stats)")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    with SessionLocal() as db:
        cursor.execute("""
                       SELECT telegram_id
                       FROM users
                       WHERE telegram_id = %s
                       """, (message.from_user.id,))
        user = cursor.fetchone()
        if not user:
            bot.reply_to(message, "Сначала нужно использовать /start")
            return

        cursor.execute("""
                        SELECT username_codewars FROM users WHERE telegram_id = %s
        """, (message.from_user.id,)) # parse nickname_codewars from db
        username = cursor.fetchone()
        if not username:
            bot.reply_to(message, "Сначала нужно использовать /nick")
            return

        stats = parse_html(f"https://www.codewars.com/users/{username[0]}") # parse statistic for request
        stats_dict = stats_formating(stats)

        cursor.execute(""" 
                    UPDATE user_stats
                    SET followers = %(followers)s, allies = %(allies)s, rank = %(rank)s, honor = %(honor)s, 
                                    leaders_board = %(leaders_board)s, honor_percentile = %(honor_percentile)s, total_completed = %(total_completed)s
                    WHERE user_id = (SELECT id 
                                     FROM users 
                                     WHERE telegram_id = %(telegram_id)s)
        """, {**stats_dict, "telegram_id": message.from_user.id}) # update stats
        conn.commit()

        cursor.execute("""
                       SELECT followers, allies, leaders_board, honor_percentile, honor, rank, total_completed
                       FROM user_stats
                       WHERE user_id = (SELECT id
                                        FROM users
                                        WHERE telegram_id = %s)
                       """, (message.from_user.id,)) # check stats
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

bot.infinity_polling(timeout=60, long_polling_timeout=60)