from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import timedelta, datetime
import database.firebase_db
# ----------------------------
from scraping import share_functions
from scraping.share_functions import *

url_list = []
title_list = []
date_time_list = []
contents_news_list = []
scrapped = []
url_link = 'https://www.khaosod.co.th/'
topics_list = ['politics', 'economics', 'sports', 'entertainment']
postfix_url = "/page/"
topic = topics_list[1]
full_url = url_link + topic
full_format_date = ""
months = {"01": "ม.ค.", "02": "ก.พ.", "03": "มี.ค.", "04": "เม.ย.", "05": "พ.ค.", "06": "มิ.ย.",
          "07": "ก.ค.", "08": "ส.ค.", "09": "ก.ย.", "10": "ต.ค.", "11": "พ.ย.", "12": "ธ.ค."}

# ----------------------------
def find_flashback_date(previous_to_date):
    global full_format_date

    flashback = timedelta(days=previous_to_date)
    current_date = datetime.now()
    date_flashback = current_date - flashback
    date_flashback_news = date_flashback.strftime("%d-%m-%Y")
    date_flashback_news = date_flashback_news.split("-")

    if date_flashback_news[0][0] == '0':
        date_flashback_news[0] = date_flashback_news[0][1]

    for m in months.keys():  # ตัวเลขให้เป็นเดือน
        if m == date_flashback_news[1]:
            month_as_text = months[m]
            break

    buddhist_year = (int(date_flashback_news[2]) + 543)
    full_format_date = date_flashback_news[0] + " " + month_as_text + " " + str(buddhist_year)
    print(full_format_date)

# ----------------------------

def compare_flashbackdate():
    global full_format_date, full_url
    # เว็บ khaosod ต้องทำการเปิดลิ้งค์เข้าไปหน้าข่าวก่อน แล้วค่อยดึงวันที่มา เพราะถ้าดึงวันที่จากหน้าหมวดหมู่เลย มันบอกเป็นชั่วโมง ไม่ได้บอกเป็นวัน
    i = 0
    check_date = ""
    while check_date != full_format_date:
        url_with_page = full_url + postfix_url + str(i)
        print("FULL URL = ", url_with_page)
        html_source = get_source(url_with_page)
        defind_scope = html_source.find_all('div', {'class': 'udblock__textwrap udblock__textwrap--transparent'})

        for dc in defind_scope:
            # เช็ควันที่ของข่าว
            temp_date = dc.find('span', {'class': 'udblock__updated_at'})
            date_text = temp_date.text
            # print("date_text", date_text)
            if date_text == full_format_date:
                check_date = date_text
                break
            else:
                get_urls(dc)
        i = i + 1
    print("จำนวนข่าวทั้งหมด = ", len(url_list))

def get_urls(dc):
    url_list.append(dc.find('a')['href'])

# ----------------------------

def scrape_details():
    dont_need_sentence = 'กดติดตามไลน์ ข่าวสด official account ได้ที่นี่'
    dict_words = OrderedDict([("\u200b", ""), ("\xa0", ""), ("\n", ""), ("\t", "")])

    def replace_multiple_word(pure_text, dict_words):
        for i, j in dict_words.items():
            pure_text = pure_text.replace(i, j)
        return pure_text

    for url in url_list:
        temp_content = ""
        get_html_source = get_source(url)

        # ----------Get Title-------
        get_title = get_html_source.find('h1', {'class': 'udsg__main-title'})

        try:
            temp_title = get_title.text
        except Exception as err:
            print(err)
            print(traceback.format_exc())
            print(url)
        cleaned_title = replace_multiple_word(temp_title, dict_words)
        cleaned_title = cleaned_title.strip()
        title_list.append(cleaned_title)

        # ----------Get Date and Time-------
        get_datetime = get_html_source.find_all('span', {'class': 'udsg__meta'})

        try:
            # date_time_list.append(get_datetime[0].text + " - " + get_datetime[2].text)
            full_date_time = get_datetime[0].text + " - " + get_datetime[2].text
            date_time_list.append(convert_date_format(full_date_time))
        except Exception as err:
            print(err)
            print(traceback.format_exc())
            print(url)

        # ----------Get Content---------
        defind_scope = get_html_source.find('div', {'class': 'udsg__content'})
        p_tags = defind_scope.find_all('p')
        for c in p_tags:
            pure_text = c.text
            cleaned_content = replace_multiple_word(pure_text, dict_words)
            if cleaned_content.strip() == dont_need_sentence:
                print("ตัดข้อความ--", dont_need_sentence, "-- ทิ้ง")
            else:
                temp_content = temp_content + cleaned_content
        temp_content = temp_content.strip()
        contents_news_list.append(temp_content)


# ----------------------------

def convert_date_format(get_date):
    split_date = get_date.split()

    day = ""
    month = ""
    year = split_date[2]

    for key, value in months.items():
        if value in split_date:
            month = key
            break

    for d in range(1, 31 + 1):
        if str(d) in split_date:
            if d < 10:
                day = "0" + str(d)
                break
            else:
                day = day + str(d)
                break

    new_format = day + "-" + month + "-" + year

    return new_format

# ---------------------------------------

def create_tuple_data():
    each_news = []
    for i in range(len(url_list)):
        each_news.append((url_list[i], title_list[i], date_time_list[i], contents_news_list[i]))
        print(each_news[i])
    return each_news

# ----------------------------

if __name__ == '__main__':
    previous_to_date = 2  # ต้องการ Scrape ข้อมูลย้อนหลังกี่วัน ?
    find_flashback_date(previous_to_date)
    compare_flashbackdate()
    scrape_details()
    scrapped = share_functions.create_tuple_data(url_list, title_list, date_time_list, contents_news_list)

    # ------------------ส่วน Database----------------------

    # name_news = "khaosod"
    # database.firebase_db.create_data(scrapped, name_news, topic)
    # database.firebase_db.read_data(name_news, topic)
    # database.firebase_db.detele_data(name_news, topic)