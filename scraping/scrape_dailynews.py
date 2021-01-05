from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import timedelta, datetime
import database.firebase_db
from datetime import date
import export_xlsx_file
from scraping import share_functions
from scraping.share_functions import *

check_first = True
url_list = []
url_link = 'https://www.dailynews.co.th'
topics_list = ['politics', 'economic', 'sports', 'entertainment']
topic = topics_list[1]
full_url = url_link + "/" + topic
postfix_url = "/" + "?page="

title_list = []
date_time_list = []
contents_news_list = []
scrapped = []

full_format_date = ""

flashback = ""

months = {"01": "มกราคม", "02": "กุมภาพันธ์", "03": "มีนาคม", "04": "เมษายน", "05": "พฤษภาคม", "06": "มิถุนายน",
          "07": "กรกฎาคม", "08": "สิงหาคม", "09": "กันยายน", "10": "ตุลาคม", "11": "พฤศจิกายน", "12": "ธันวาคม"}
#-----------------------------------------------

def find_flashback_date(previous_to_date):
    global full_format_date

    flashback = timedelta(days=previous_to_date)
    current_date = datetime.now()
    # print("Current date  = ", current_date)
    # print("Type = ", type(current_date))
    date_flashback = current_date - flashback
    # print("date_flashback date  = ", date_flashback)
    # print("Type = ", type(date_flashback))
    date_flashback_news = date_flashback.strftime("%d-%m-%Y")
    date_flashback_news = date_flashback_news.split("-")

    if date_flashback_news[0][0] == '0':
        date_flashback_news[0] = date_flashback_news[0][1]

    for m in months.keys():  # ตัวเลขให้เป็นเดือน
        if m == date_flashback_news[1]:
            month_as_text = months[m]
            break

    buddhist_year = (int(date_flashback_news[2]) + 543)
    full_format_date = date_flashback_news[0] + month_as_text + str(buddhist_year)
    print("Full format date = ", full_format_date)

def compare_flashbackdate():
    global full_format_date, full_url

    i = 1
    check_date = ""
    while check_date != full_format_date:
        url_with_page = full_url + postfix_url + str(i)
        print("อยู่หน้าที่" , i)
        get_html_source = get_source(url_with_page)
        section_tag = get_html_source.find('section', {'id': 'top-section'})
        div_tag = section_tag.find('div', {'class': 'content-wrapper'})
        article_tags = div_tag.find_all('article', {'class': 'content'})

        for at in article_tags:
            # เช็ควันที่ของข่าว
            temp_date = at.find('span', {'class': 'media-date'})
            temp_date = temp_date.text
            temp_date = temp_date.split()
            date_text = temp_date[1] + temp_date[2] + temp_date[3]

            if date_text == full_format_date:
                check_date = date_text
                break
            else:
                get_urls(at)
        i = i + 1
    print("จำนวนข่าวทั้งหมด = ", len(url_list))

def get_urls(at):
        url_list.append(url_link + at.find('a')['href'])

def scrape_details():
    temp_list = []
    dict_words = OrderedDict([("googletag.cmd.push(function() { googletag.display('div-gpt-ad-8668011-5'); });", ""),
                              ("\xa0", ""), ("\u200b", ""), ("\r", ""), ("\t", ""), ("\n", ""), ("   ", ""), ("  ", "")])
    def replace_multiple_word(pure_text, dict_words):
        for i, j in dict_words.items():
            pure_text = pure_text.replace(i, j)
        return pure_text

    for url in url_list:
        get_html_source = get_source(url)

        # ตัด Tag <script> และ <style> ออก
        # for script in get_html_source(["script", "style"]):
        #     script.decompose()

        # ----------Get Title-------
        try:
            get_title = get_html_source.find('h1', {'class': 'title'}).text
        except Exception as err:
            print(err)
            print(traceback.format_exc())
            print(url)

        cleaned_title = replace_multiple_word(get_title, dict_words)
        title_list.append(cleaned_title)

        # ----------Get Date and Time-------
        try:
            temp_date = get_html_source.find('span', {'class': 'date'}).text
            date_time_list.append(convert_date_format(temp_date))
        except Exception as err:
            print(err)
            print(traceback.format_exc())
            print(url)

        # ----------Get Content---------
        try:
            defind_scope = get_html_source.find('div', class_='entry textbox content-all')
            span_tags = defind_scope.find('span').text
            temp_list.append(span_tags)
        except AttributeError:
            temp_content = get_html_source.find('div', class_='entry textbox content-all').text
            temp_list.append(temp_content)

    for e in temp_list:
        new_content = replace_multiple_word(e, dict_words)
        contents_news_list.append(new_content)

def convert_date_format(get_date):
    split_date = get_date.split()

    day = ""
    month = ""
    year = split_date[3]

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

def create_tuple_data():
    each_news = []
    for i in range(len(url_list)):
        each_news.append((url_list[i], title_list[i], date_time_list[i], contents_news_list[i]))
        print(each_news[i])
    return each_news

if __name__ == '__main__':

    previous_to_date = 1 # ต้องการ Scrape ข้อมูลย้อนหลังกี่วัน ?
    find_flashback_date(previous_to_date)
    compare_flashbackdate()
    scrape_details()
    scrapped = share_functions.create_tuple_data(url_list, title_list, date_time_list, contents_news_list)

  #------------------------ส่วนของ Database---------------------

    name_news = "dailynews"
    # database.firebase_db.create_data(scrapped, name_news, topic)
    # database.firebase_db.read_data(name_news, topic)
    # database.firebase_db.detele_data(name_news, topic)