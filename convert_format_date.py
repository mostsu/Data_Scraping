from datetime import timedelta, datetime
import traceback
import database.firebase_db
from datetime import date

def convert(get_date, name_news):

    months1 = {"มกราคม": "01", "กุมภาพันธ์": "02", "มีนาคม": "03", "เมษายน": "04", "พฤษภาคม": "05", "มิถุนายน": "06",
              "กรฎาคม": "07", "สิงหาคม": "08", "กันยายน": "09", "ตุลาคม": "10", "พฤศจิกายน": "11", "ธันวาคม": "12"}

    months2 = {"มกราคม": "01", "กุมภาพันธ์": "02", "มีนาคม": "03", "เมษายน": "04", "พฤษภาคม": "05", "มิถุนายน": "06",
              "กรฎาคม": "07", "สิงหาคม": "08", "กันยายน": "09", "ตุลาคม": "10", "พฤศจิกายน": "11", "ธันวาคม": "12"}

    split_date = get_date.split()

    # year = date.today().year + 543
    # year = str(year)
    if name_news == "khaosod":
        index = 2
    elif name_news == "dailynews":
        index = 3

    day = ""
    month = ""
    year = int(split_date[index])

    for m in months.keys():
        if m in split_date:
            month = months[m]
            break

    for d in range(1, 31 + 1):
        if str(d) in split_date:
            if d < 10:
                day = "0" + str(d)
                break
            else:
                day = day + str(d)
                break

    new_format = year + "-" + month + "-" + day

    return new_format