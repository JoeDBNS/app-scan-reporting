# Column filters
# https://openpyxl.readthedocs.io/en/stable/filters.html#using-filters-and-sorts



import os, datetime as dt
from openpyxl import Workbook
from openpyxl.worksheet.filters import (
    FilterColumn,
    CustomFilter,
    CustomFilters,
    DateGroupItem,
    Filters,
)
from openpyxl.styles import PatternFill



def Setup():
    wb = Workbook()
    ws = wb.active
    return wb, ws


def SaveFile(wb, name):
    # YYYYMMDD
    timestamp_today = str(dt.date.today()).replace('-', '')

    reports_path = './_reports/' + timestamp_today

    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    wb.save(reports_path + '/' + name + '.xlsx')


def SetColumnColors(ws, column_colors):
    for idx, row in enumerate(ws.rows):
        for col in row:
            ws[col.coordinate].fill = PatternFill(start_color=column_colors[idx], end_color=column_colors[idx], fill_type='solid')


def SetColumnSize(ws):
    for col in ws.columns:
        max_length = 6
        column_letter = col[0].column_letter

        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass

        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width


def SetHyperlinks(ws):
    for col in ws.columns:
        column_letter = col[0].column_letter

        # hard coding column with hyperlinks
        if(column_letter == 'A'):
            for cell in col[1:]:
                cell.hyperlink = cell.value
                cell.style = "Hyperlink"


def BuildXlsxFile(name, data, column_colors):
    wb, ws = Setup()

    for row in data:
        ws.append(row)

    SetHyperlinks(ws)

    SetColumnColors(ws, column_colors)
    SetColumnSize(ws)

    SaveFile(wb, name)