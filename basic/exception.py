# -*-coding:utf-8-*-

# try:
#     a = 1/0
# except Exception as e:
#     print(e)

for a in range(1,3):
    try:
        b = a/0
    except Exception as e:
        print(e)

print('done')
