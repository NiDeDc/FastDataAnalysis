from math import ceil
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QCursor
import PlotControl as Plc


class DynamicTableWidget(QTableWidget):
    def __init__(self, _id):
        super(DynamicTableWidget, self).__init__()
        self.id = _id
        self.data = None
        self.per_row = 0
        self.per_col = 0
        self.verticalScrollBar().installEventFilter(self)
        self.horizontalScrollBar().installEventFilter(self)
        self.menu = QMenu(self)
        self.action = QAction(self)
        self.action.setText("时域图")
        self.menu.addAction(self.action)
        self.action.triggered.connect(self.DrawSingleChannelDomain)

    def CalculatePerNum(self):  # 计算每页显示数量
        desk_widget = QApplication.desktop()
        row_height = self.rowHeight(0)
        col_width = self.columnWidth(0)
        desk_height = desk_widget.availableGeometry().height()
        desk_width = desk_widget.availableGeometry().width()
        self.per_row = ceil(desk_height / row_height)
        self.per_col = ceil(desk_width / col_width)

    def LoadData(self, data):
        self.data = data
        s = self.data.shape
        self.setRowCount(s[0])
        self.setColumnCount(s[1])
        self.CalculatePerNum()
        self.UpdateData()

    def UpdateData(self):
        if self.data is None:
            return
        row = self.data.shape[0]
        col = self.data.shape[1]
        pos_y = self.verticalScrollBar().value()
        pos_x = self.horizontalScrollBar().value()
        for i in range(pos_y, min(pos_y + self.per_row, row)):
            for j in range(pos_x, min(pos_x + self.per_col, col)):
                if self.item(i, j) is None:
                    self.setItem(i, j, QTableWidgetItem(str(self.data[i, j])))

    def DrawSingleChannelDomain(self):
        sensor = []
        data = []
        ranges = self.selectedRanges()
        ch_sensor = []
        for i in ranges:
            t_row = i.topRow()
            b_row = i.bottomRow()
            l_col = i.leftColumn()
            r_col = i.rightColumn()
            for j in range(t_row, b_row + 1):
                ch_sensor.append([j, l_col, r_col])
        all_sensor = [self.id, ch_sensor]
        sensor.append(all_sensor)
        data.append(self.data)
        Plc.DrawTimeDomains(data, sensor)

    def contextMenuEvent(self, event):  # 右键默认槽
        self.menu.exec(QCursor.pos())
        event.accept()

    def eventFilter(self, obj, event):
        if obj == self.verticalScrollBar() or obj == self.horizontalScrollBar():
            self.UpdateData()
        return QTableWidget.eventFilter(self, obj, event)
