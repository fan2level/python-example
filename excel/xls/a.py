import xlrd

i = './mp.xls'

wb = xlrd.open_workbook(i)
ws = wb.sheet_by_index(0)

rows = ws.nrows
cols = ws.ncols

row = 0
data = dict()
for row in range(rows):
    data[row] = dict()
    for col in range(cols):
        data[row][col] = ws.cell_value(row, col)

for row in data:
    for col in data[row]:
        print(data[row][col])
