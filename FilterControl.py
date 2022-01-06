from Ui.FilterWindow import Ui_Dialog_filter
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from scipy import signal as sig


class FilterControl(QtWidgets.QDialog, Ui_Dialog_filter):
    finish = pyqtSignal()

    def __init__(self):
        super(FilterControl, self).__init__()
        self.setupUi(self)
        self.out_data = None

    def ExecuteFiltering(self, data):
        if self.comboBox_filter.currentIndex() == 0:
            self.ButterworthHighpass(data, self.spinBox_freq.value())
        self.finish.emit()

    # def ButterworthHighpass(self, data, freq):
    #     # 滤波因子
    #     c = np.arctan(3.14 * freq / 1000)
    #     a1 = 1 / (1 + c + c * c)
    #     a2 = -2 * a1
    #     a3 = a1
    #     b1 = 2 * (c * c - 1) * a1
    #     b2 = (1 - c + c * c) * a1
    #     self.out_data = np.zeros(data.shape)
    #     for i in range(3, data.shape[1]):
    #         self.out_data[:, i] = a1 * data[:, i] + a2 * data[:, i - 1] + a3 * data[:, i - 2] - b1 * \
    #                               self.out_data[:, i - 1] - b2 * self.out_data[:, i - 2]

    def ButterworthHighpass(self, data, freq):
        wn = 2 * freq / 1000
        b, a = sig.butter(3, wn, 'highpass')  # 配置滤波器 3 表示滤波器的阶数
        self.out_data = sig.filtfilt(b, a, data)
