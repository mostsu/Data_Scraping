import xlsxwriter

def write_xlsx_file(scrapped, url_list, title_list, date_time_list, contents_news_list):
    workbook = xlsxwriter.Workbook("Khaosod political news.xlsx")
    excel_sheet = workbook.add_worksheet()

    #กำหนด Style ของ Column
    column_style = workbook.add_format({"bg_color": "#FBFF00", "font_size": 20})
    excel_sheet.set_column("A:A",50)
    excel_sheet.set_column("B:B",80)
    excel_sheet.set_column("C:C",30)
    excel_sheet.set_column("D:D",200)

    # กำหนด Headers แต่ละ Column
    excel_sheet.write("A1", "URL", column_style)
    excel_sheet.write("B1", "หัวข้อข่าว", column_style)
    excel_sheet.write("C1", "วันที่ / เวลา", column_style)
    excel_sheet.write("D1", "เนื้อหา", column_style)

    # excel_sheet.write(0, 0, "TEST", column_style)

    for r in range(len(scrapped)):
        excel_sheet.write(r+1, 0, url_list[r])
        excel_sheet.write(r+1, 1, title_list[r])
        excel_sheet.write(r+1, 2, date_time_list[r])
        excel_sheet.write(r+1, 3, contents_news_list[r])
    workbook.close()
    print("เขียนข้อมูลเป็นไฟล์ Excel แล้ว")
