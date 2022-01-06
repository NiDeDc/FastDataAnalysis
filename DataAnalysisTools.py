from PyQt5 import QtWidgets
from Ui.MainWindow import Ui_MainWindow
import sys
from LoadDataControl import LoadDataControl
import PlotControl as Plc
import threading
from DynamicTableWidget import DynamicTableWidget as dtw
from FilterControl import FilterControl
from TimeSettingControl import TimeSettingControl as tsc
from WaitingControl import WaitingControl
from ExportControl import ExportControl
import ExportControl as Epc


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.ldc = LoadDataControl()  # 加载数据窗口
        self.ldc.finish.connect(self.LoadFinish)
        self.ftc = FilterControl()  # 滤波窗口
        self.ftc.finish.connect(self.FilterFinish)
        self.table = []  # 表格数组
        self.wait = WaitingControl()
        self.is_load = False

    def HandlerLoad(self):
        if self.ldc.exec() == 1:
            for i in range(0, len(self.table)):
                self.tabWidget_tab.removeTab(0)  # 每次remove后剩下的index提前
            self.table.clear()
            self.ldc.joint_data.clear()
            self.ldc.is_run.clear()
            file_names = []
            for i in range(0, self.ldc.spinBox.value()):
                filename = QtWidgets.QFileDialog.getOpenFileNames(self, '通道' + str(i + 1), '', 'FLData(*.bin)')[0]
                if len(filename) == 0:
                    break
                file_names.append([i, filename])
            for i in file_names:
                t = threading.Thread(target=self.ldc.LoadData, args=(i[1], i[0]))
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
                    table_w = dtw(i)
                    table_w.menu.addAction(self.action_stft)
                    self.table.append(table_w)
                    self.tabWidget_tab.addTab(table_w, '通道' + str(i + 1))
                    if all_data[i] is not None:
                        table_w.LoadData(all_data[i])
                    else:
                        QtWidgets.QMessageBox.critical(self, "错误", '通道' + str(i + 1) + "解析错误，请检查文件名和光栅序号是否一致")

    def HandlerFilter(self):
        index = self.tabWidget_tab.currentIndex()
        if self.ftc.exec() == 1 and len(self.table) > 0:
            data = self.table[index].data
            if data is not None:
                self.wait.show()
                t = threading.Thread(target=self.ftc.ExecuteFiltering, args=([data]))
                t.setDaemon(True)
                t.start()

    def FilterFinish(self):
        index = self.tabWidget_tab.currentIndex()
        self.table[index].clear()
        self.table[index].data = self.ftc.out_data
        self.table[index].UpdateData()
        self.wait.close()

    def HandlerDrawTime(self):
        c_num = len(self.table)
        if c_num > 0:
            sensor = []
            data = []
            t = tsc(c_num)
            if t.exec() == 1:
                group = t.group
                for i in range(0, len(group)):
                    if group[i][0].isChecked() and self.table[i].data is not None:
                        sensor_c = []
                        for j in group[i][1]:
                            sensor_s = [j[0].value(), j[1].value(), j[2].value()]
                            sensor_c.append(sensor_s)
                        sensor.append([self.table[i].id, sensor_c])
                        data.append(self.table[i].data)
                Plc.DrawTimeDomains(data, sensor)

    def HandlerWaterFall(self):
        index = self.tabWidget_tab.currentIndex()
        if index != -1:
            data = self.table[index].data
            if data is not None:
                Plc.DrawWaterFall(data)

    def HandlerSTFT(self):
        index = self.tabWidget_tab.currentIndex()
        if index != -1:
            data = self.table[index].data
            if data is not None:
                ranges = self.table[index].selectedRanges()
                sensor = 0
                for i in ranges:
                    sensor = i.topRow()
                    break
                Plc.DrawSTFT(data, 1000, sensor)

    def HandlerExport(self):
        c_num = len(self.table)
        index = self.tabWidget_tab.currentIndex()
        if c_num > 0:
            epc = ExportControl()
            epc.finish.connect(self.ExportFinish)
            if epc.exec() == 1 and self.table[index].data is not None:
                group = epc.group
                file_index = []
                for i in group:
                    file_index_s = [i[0].value(), i[1].value(), i[2].value(), i[3].value()]
                    file_index.append(file_index_s)
                t = threading.Thread(target=epc.SaveData, args=(self.table[index].data, file_index))
                t.setDaemon(True)
                t.start()
                self.wait.show()

    def ExportFinish(self):
        self.wait.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    StartPage = MainWindow()
    StartPage.show()  # 显示
    sys.exit(app.exec_())
