from bs4 import BeautifulSoup
import requests

from models import Base, User, UserStats
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

st_accept = "text/html"
st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}


def parse_html(link):
    statistic = []
    htm = requests.get(link, headers)
    src = htm.text

    soup = BeautifulSoup(src, 'html.parser')
    stats = soup.find_all('div', class_='stat')

    for item in stats:
        statistic.append(item.get_text(strip=False))

    return statistic

def stats_formating(statistic): # переводим инф-ию в нужный формат, хз пока как реализовать
    stats = [statistic[6:13]]
    stats = stats[0]
    print(stats)