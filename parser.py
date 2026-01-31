from bs4 import BeautifulSoup
import requests

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
    stats = statistic[6:13]
    complited_stats = []
    for item in stats:
        object_item = item.split(':')[-1]
        if object_item.isdigit():
            complited_stats.append(int(object_item))
        else:
            complited_stats.append(object_item)
    formatted = {
        "followers": int(complited_stats[0]),
        "allies": int(complited_stats[1]),
        "rank": complited_stats[2],
        "honor": int(complited_stats[3].replace(",", "")),  # '1,433' -> 1433
        "leaders_board": complited_stats[4],
        "honor_percentile": complited_stats[5],
        "total_completed": int(complited_stats[6])
    }
    return formatted