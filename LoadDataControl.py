from PyQt5 import QtWidgets
from Ui.DataLoadWindow import Ui_Dialog_Dataload
import numpy as np
import os
from PyQt5.QtCore import pyqtSignal


def LoadSingleFile(path):
    try:
        col = int(os.path.split(path)[1].split('_')[2][1:])
        bin_file = np.fromfile(path, dtype=np.float32)
        size = len(bin_file)
        row = int(size / col)
        data_array = bin_file.reshape((row, col))
        data_array_t = data_array.T
        return data_array_t
    except:
        return None


class LoadDataControl(QtWidgets.QDialog, Ui_Dialog_Dataload):
    finish = pyqtSignal()

    def __init__(self):
        super(LoadDataControl, self).__init__()
        self.setupUi(self)
        self.threads = []  # 加载数据线程,每通道一个线程
        self.joint_data = []  # 将所有bin文件拼接后的矩阵数据
        self.is_run = []

    def LoadData(self, path, index):
        size = len(path)
        joint_data = None
        if size > 0:
            for i in range(size):
                single_data = LoadSingleFile(path[i])
                if single_data is not None:
                    if joint_data is not None:
                        joint_data = np.hstack((joint_data, single_data))
                    else:
                        joint_data = single_data
                else:
                    joint_data = None
                    break
            self.joint_data[index] = joint_data
        self.is_run[index] = False
        self.finish.emit()

    # def WaitForLoad(self):
    #     for t in self.threads:
    #         t.join()
