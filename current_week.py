#Получить текущую неделю
import requests
from bs4 import BeautifulSoup
def get_current_week():
    page = requests.get("https://www.mirea.ru/")
    soup = BeautifulSoup(page.text, "html.parser")
    weeks = soup.find("div", {"class": "bonus_cart-title"})
    week = weeks.get_text()
    week = week.split(',')
    week = week[1]
    weekNow = ""
    for i in range(len(week)):
        if week[i].isdigit():
            weekNow += week[i]
    weekNow = int(weekNow)
    return weekNow