from PyQt5 import QtWidgets
from Ui.MainWindow import Ui_MainWindow
import sys
from LoadDataControl import LoadDataControl
import PlotControl as Plc
import threading
import csv
import numpy as np
from DynamicTableWidget import DynamicTableWidget as dtw
# from FilterControl import FilterControl
# from TimeSettingControl import TimeSettingControl as tsc
from WaitingControl import WaitingControl
# from ExportControl import ExportControl


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ldc = LoadDataControl()  # 加载数据窗口
        self.ldc.finish.connect(self.LoadFinish)
        # self.ftc = FilterControl()  # 滤波窗口
        # self.ftc.finish.connect(self.FilterFinish)
        self.table = []  # 表格数组
        self.wait = WaitingControl()
        self.is_load = False
        self.code_data = [None, None, None, None, None, None, None, None]
        self.dev = 1
        self.ch = 1

    def HandlerLoad(self):
        if self.ldc.exec() == 1:
            for i in range(0, len(self.table)):
                self.tabWidget_tab.removeTab(0)  # 每次remove后剩下的index提前
            self.table.clear()
            self.ldc.joint_data.clear()
            self.code_data = [None, None, None, None, None, None, None, None]
            self.ldc.is_run.clear()
            self.dev = self.ldc.spinBox_2.value()
            self.ch = self.ldc.spinBox.value()
            file_names = []
            for i in range(0, self.dev):
                for j in range(0, self.ch):
                    filename = QtWidgets.QFileDialog.getOpenFileNames(self, '设备' + str(i + 1) + '通道' + str(j + 1), ''
                                                                      , 'FLData(*.bin)')[0]
                    if len(filename) == 0:
                        self.ldc.is_run.append(False)
                        break
                    file_names.append(filename)
                    t = threading.Thread(target=self.ldc.LoadData, args=(filename, i * self.ch + j))
                    self.ldc.is_run.append(True)
                    self.ldc.joint_data.append(None)
                    self.ldc.threads.append(t)
                    t.setDaemon(True)
                    t.start()
            if len(file_names) > 0:
                self.is_load = False
                self.wait.show()

    def LoadFinish(self):
        for i in self.ldc.is_run:
            if i:
                return
        if self.is_load is not True:
            self.is_load = True
            self.wait.close()
            all_data = self.ldc.joint_data
            num = len(all_data)
            if num > 0:
                for i in range(0, num):
                    # table_w = dtw(i)
                    # table_w.menu.addAction(self.action_stft)
                    # self.table.append(table_w)
                    # self.tabWidget_tab.addTab(table_w, '通道' + str(i + 1))
                    if all_data[i] is None:
                        reu = divmod(i, self.ch)
                        QtWidgets.QMessageBox.critical(self, "错误", '仪表' + str(reu[0] + 1) + '通道' + str(reu[1] + 1)
                                                       + "解析错误，请检查文件名和光栅序号是否一致")
                # QtWidgets.QMessageBox.information(self, "提示", '加载成功')

    def HandlerFilter(self):
        pass
        # if self.ftc.exec() == 1:
        #     all_data = self.ldc.joint_data
        #     for i in range(len(all_data)):
        #         data = all_data[i]
        #         if data is not None:
        #             # self.wait.show()
        #             t = threading.Thread(target=self.ftc.ExecuteFiltering, args=([data]))
        #             t.setDaemon(True)
        #             t.start()

    def HandlerCoding(self):
        filename = QtWidgets.QFileDialog.getOpenFileNames(self, '编码文档', '', 'Code(*.csv)')[0]
        csv_file = open(filename[0], "r")
        reader = csv.reader(csv_file)
        all_data = self.ldc.joint_data
        for item in reader:
            dev = int(item[2]) - 1
            ch = int(item[3]) - 1
            sensor = int(item[4])
            index = dev * self.ch + ch
            if item[0] == 'Y1':
                if self.code_data[0] is None:
                    self.code_data[0] = all_data[index][sensor]
                else:
                    self.code_data[0] = np.vstack((self.code_data[0], all_data[index][sensor]))
            elif item[0] == 'Y2':
                if self.code_data[1] is None:
                    self.code_data[1] = all_data[index][sensor]
                else:
                    self.code_data[1] = np.vstack((self.code_data[1], all_data[index][sensor]))
            elif item[0] == 'Y3':
                if self.code_data[2] is None:
                    self.code_data[2] = all_data[index][sensor]
                else:
                    self.code_data[2] = np.vstack((self.code_data[2], all_data[index][sensor]))
            elif item[0] == 'Y4':
                if self.code_data[3] is None:
                    self.code_data[3] = all_data[index][sensor]
                else:
                    self.code_data[3] = np.vstack((self.code_data[3], all_data[index][sensor]))
            elif item[0] == 'Z1':
                if self.code_data[4] is None:
                    self.code_data[4] = all_data[index][sensor]
                else:
                    self.code_data[4] = np.vstack((self.code_data[4], all_data[index][sensor]))
            elif item[0] == 'Z2':
                if self.code_data[5] is None:
                    self.code_data[5] = all_data[index][sensor]
                else:
                    self.code_data[5] = np.vstack((self.code_data[5], all_data[index][sensor]))
            elif item[0] == 'Z3':
                if self.code_data[6] is None:
                    self.code_data[6] = all_data[index][sensor]
                else:
                    self.code_data[6] = np.vstack((self.code_data[6], all_data[index][sensor]))
            elif item[0] == 'Z4':
                if self.code_data[7] is None:
                    self.code_data[7] = all_data[index][sensor]
                else:
                    self.code_data[7] = np.vstack((self.code_data[7], all_data[index][sensor]))
            else:
                pass
        table_1 = dtw(0)
        self.tabWidget_tab.addTab(table_1, 'Y1')
        table_2 = dtw(1)
        self.tabWidget_tab.addTab(table_2, 'Y2')
        table_3 = dtw(2)
        self.tabWidget_tab.addTab(table_3, 'Y3')
        table_4 = dtw(3)
        self.tabWidget_tab.addTab(table_4, 'Y4')
        table_5 = dtw(4)
        self.tabWidget_tab.addTab(table_5, 'Z1')
        table_6 = dtw(5)
        self.tabWidget_tab.addTab(table_6, 'Z2')
        table_7 = dtw(6)
        self.tabWidget_tab.addTab(table_7, 'Z3')
        table_8 = dtw(7)
        self.tabWidget_tab.addTab(table_8, 'Z4')

    def FilterFinish(self):
        pass
        # index = self.tabWidget_tab.currentIndex()
        # self.table[index].clear()
        # self.table[index].data = self.ftc.out_data
        # self.table[index].UpdateData()
        # self.wait.close()

    # def HandlerDrawTime(self):
    #     c_num = len(self.table)
    #     if c_num > 0:
    #         sensor = []
    #         data = []
    #         t = tsc(c_num)
    #         if t.exec() == 1:
    #             group = t.group
    #             for i in range(0, len(group)):
    #                 if group[i][0].isChecked() and self.table[i].data is not None:
    #                     sensor_c = []
    #                     for j in group[i][1]:
    #                         sensor_s = [j[0].value(), j[1].value(), j[2].value()]
    #                         sensor_c.append(sensor_s)
    #                     sensor.append([self.table[i].id, sensor_c])
    #                     data.append(self.table[i].data)
    #             Plc.DrawTimeDomains(data, sensor)

    def HandlerWaterFall(self):
        index = self.tabWidget_tab.currentIndex()
        if index != -1:
            data = self.code_data[index]
            if data is not None:
                Plc.DrawWaterFall(data)

    # def HandlerSTFT(self):
    #     index = self.tabWidget_tab.currentIndex()
    #     if index != -1:
    #         data = self.table[index].data
    #         if data is not None:
    #             ranges = self.table[index].selectedRanges()
    #             sensor = 0
    #             for i in ranges:
    #                 sensor = i.topRow()
    #                 break
    #             Plc.DrawSTFT(data, 1000, sensor)

    # def HandlerExport(self):
    #     c_num = len(self.table)
    #     index = self.tabWidget_tab.currentIndex()
    #     if c_num > 0:
    #         epc = ExportControl()
    #         epc.finish.connect(self.ExportFinish)
    #         if epc.exec() == 1 and self.table[index].data is not None:
    #             group = epc.group
    #             file_index = []
    #             for i in group:
    #                 file_index_s = [i[0].value(), i[1].value(), i[2].value(), i[3].value()]
    #                 file_index.append(file_index_s)
    #             t = threading.Thread(target=epc.SaveData, args=(self.table[index].data, file_index))
    #             t.setDaemon(True)
    #             t.start()
    #             self.wait.show()

    # def ExportFinish(self):
    #     self.wait.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    StartPage = MainWindow()
    StartPage.show()  # 显示
    sys.exit(app.exec_())
