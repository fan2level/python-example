import xlrd
from pprint import pprint

i = './mp.xls'
i = 'MP 대표 수익률 비교공시_20210705.xls'
i = 'MP 현황 및 수수료 비교공시_20210705.xls'

wb = xlrd.open_workbook(i)
ws = wb.sheet_by_index(0)

rows = ws.nrows
cols = ws.ncols

row = 0
data = dict()
for row in range(rows):
    data[row] = dict()
    for col in range(cols):
        data[row][col] = str(ws.cell_value(row, col)).replace('\n','')

for row in data:
    for col in data[row]:
        print(data[row][col], end=',')
    print()
