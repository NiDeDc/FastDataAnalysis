import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# 递归获取.csv文件存入到list1
import os


# 将所有文件的路径放入到listcsv列表中
def list_dir(file_dir):
    # list_csv = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        # 判断是文件夹还是文件
        if os.path.isfile(path):
            # print("{0} : is file!".format(cur_file))
            dir_files = os.path.join(file_dir, cur_file)
        # 判断是否存在.csv文件，如果存在则获取路径信息写入到list_csv列表中
        if os.path.splitext(path)[1] == '.csv':
            csv_file = os.path.join(file_dir, cur_file)
            # print(os.path.join(file_dir, cur_file))
            # print(csv_file)
            list_csv.append(csv_file)
        if os.path.isdir(path):
            # print("{0} : is dir".format(cur_file))
            # print(os.path.join(file_dir, cur_file))
            list_dir(path)
    return list_csv


if __name__ == '__main__':
    paths = r'E:\2022-06-03-17_07'
    list_csv = []
    list_dir(file_dir=paths)
    print(list_csv)

    # path = r'E:\HE\2022-06-01\2022-06-01-13_55'#文件夹路径
    # files = os.listdir(path)
    timeIndex = -1
    channelData = [[] for i in range(4)]
    cTongDao = 0
    cPotition = 1
    colorArray = ['black', 'red', 'green', 'blue']
    for file in list_csv:
        data = pd.read_csv(file)
        data = np.array(data)
        for j in data:
            j[3] = j[3][1:-1]
            j[3] = j[3].split(',', -1)
            for index in range(len(j[3])):
                j[3][index] = float(j[3][index])
        for d in data:
            channelData[d[cTongDao]].append(d)

    for channelNo in range(len(channelData)):
        miles = []
        times = []
        index = []
        count = 0
        for record in channelData[channelNo]:
            miles.append(record[cPotition])
            times.append(record[timeIndex])
            index.append(count)
            count += 1
        plt.scatter(miles, times, color=colorArray[channelNo],
                    label='channel' + str(channelNo + 1),
                    s=2)
        plt.legend()

    plt.show()
