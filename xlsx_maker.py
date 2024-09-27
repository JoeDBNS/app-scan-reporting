import os
from openpyxl import Workbook
from openpyxl.worksheet.filters import (
    FilterColumn,
    CustomFilter,
    CustomFilters,
    DateGroupItem,
    Filters,
)


wb = Workbook()
ws = wb.active


# data = [
#     ["Fruit", "Quantity"],
#     ["Kiwi", 3],
#     ["Grape", 15],
#     ["Apple", 3],
#     ["Peach", 3],
#     ["Pomegranate", 3],
#     ["Pear", 3],
#     ["Tangerine", 3],
#     ["Blueberry", 3],
#     ["Mango", 3],
#     ["Watermelon", 3],
#     ["Blackberry", 3],
#     ["Orange", 3],
#     ["Raspberry", 3],
#     ["Banana", 3]
# ]

# for r in data:
#     ws.append(r)





# Data can be assigned directly to cells
ws['A1'] = 42

# Rows can also be appended
ws.append([1, 2, 3])

# Python types will automatically be converted
import datetime
ws['A2'] = datetime.datetime.now()






# YYYYMMDD
timestamp_today = str(datetime.date.today()).replace('-', '')

reports_path = './_reports/' + timestamp_today

if not os.path.exists(reports_path):
    os.makedirs(reports_path)

wb.save(reports_path + '/test.xlsx')





# Column filters
# https://openpyxl.readthedocs.io/en/stable/filters.html#using-filters-and-sorts

# Cell colors
# https://openpyxl.readthedocs.io/en/stable/styles.html