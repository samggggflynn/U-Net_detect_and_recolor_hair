
color = '1，2，3'
Colors = {'银色': [167, 169, 169], '皇家蓝': [225, 105, 65], '紫色': [128, 0, 128], '浅粉': [255, 182, 193], '深粉':[255, 20, 147]}
# print('qufan', Colors[color][::-1])
print(type(Colors['银色']))
# if isinstance(color, str):
#     try:
#         co = []
#         for rgb in color.split(','):
#             print("rgb", rgb)
#             if rgb.startswith('0x' or '0X'):
#                 co.append(int(rgb, 16))  # 将16进制str转为10进制int整数
#             else:
#                 co.append(int(rgb, 10))  # 将10进制str转为10进制int整数
#         color = tuple(co)
#         print(color)
#         print(type(color))
#     except:
#         for key in Colors:
#             if color == key:
#                 print( Colors[color][::-1])
#                 color = tuple(Colors[color][::-1])
#                 print(color)
#                 print(type(color))
#     else:
#         color = (1, 1, 1)
#         print(color)

co = []
if color.startswith('0x' or '0X'):
    for rgb in color.split(','):
        co.append(int(rgb, 16))  # 将16进制str转为10进制int整数
        color = tuple(co)
        print(color)
        print(type(color))
if color.startswith('0x' or '0X') :
    try:
        # co = []
        for rgb in color.split(','):
            co.append(int(rgb, 10))  # 将10进制str转为10进制int整数
            color = tuple(co)
            print(color)
            print(type(color))
    except:
        for key in Colors:
            if color == key:
                # print(Colors[color][::-1])
                color = Colors[color][::-1]
                color = tuple(color)
                print(color)
                print(type(color))
    # else:
        # color = tuple(color)
        # print(color)
        # print(type(color))