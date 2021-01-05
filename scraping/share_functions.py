import requests
from bs4 import BeautifulSoup
import traceback
from fake_useragent import UserAgent

#ทุกๆครั้งที่มีการ Scrape ข้อมูลจากเว็บ จะต้องทำ  Random Fake User Agent ก่อน
#เพื่อไม่ให้ทางเว็บแบนการ Scraping ของเราได้
def random_fake_user_agent():
    ua = UserAgent()
    random_fake_headers = ua.random
    header = {'User-Agent': str(random_fake_headers)}
    return header

def get_source(full_url):
    headers = random_fake_user_agent()
    try:
        req = requests.get(full_url, headers=headers)
        html_source = BeautifulSoup(req.text, 'html.parser')
        print("Connection Success !")
        return html_source
    except Exception as err:
        print(err)
        print(traceback.format_exc())

def create_tuple_data(url_list, title_list, date_time_list, contents_news_list):
    each_news = []
    for i in range(len(url_list)):
        each_news.append((url_list[i], title_list[i], date_time_list[i], contents_news_list[i]))
        print(each_news[i])
    return each_news