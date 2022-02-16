from Ui.ExportWindow import Ui_Dialog_Export
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import numpy


class ExportControl(QtWidgets.QDialog, Ui_Dialog_Export):
    finish = pyqtSignal()

    def __init__(self):
        super(ExportControl, self).__init__()
        self.setupUi(self)
        self.items = None
        self.group = None
        data_num = 1
        for i in range(0, data_num):
            spi_num = QtWidgets.QSpinBox()
            spi_num.setMinimum(1)
            spi_num.setMaximum(100)
            spi_num.valueChanged.connect(self.DataChange)
            label = QtWidgets.QLabel("数据个数")
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            grid_layout = QtWidgets.QGridLayout()
            grid_layout.addWidget(label, 0, 0, 1, 1)
            grid_layout.addWidget(spi_num, 0, 1, 1, 1)
            items = self.CreateItems(data_num)
            grid_layout.addWidget(self.items, 1, 0, 1, 2)
            grid_layout.setSpacing(0)
            self.widget.setLayout(grid_layout)
            self.group = items

    def DataChange(self, value):
        layout = self.widget.layout()
        layout.removeWidget(self.items)
        self.group = self.CreateItems(value)
        # self.Items.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        layout.addWidget(self.items, 1, 0, 1, 2)

    def CreateItems(self, num):
        widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout()
        items = []
        for i in range(0, num):
            group = QtWidgets.QGroupBox("数据范围" + str(i + 1))
            grid_layout = QtWidgets.QGridLayout()
            spi_top = QtWidgets.QSpinBox()
            spi_bottom = QtWidgets.QSpinBox()
            spi_left = QtWidgets.QSpinBox()
            spi_right = QtWidgets.QSpinBox()
            spi_top.setMaximum(1000000000)
            spi_top.setMinimum(1)
            spi_bottom.setMaximum(1000000000)
            spi_bottom.setValue(1000)
            spi_left.setMaximum(1000000000)
            spi_left.setMinimum(1)
            spi_right.setMaximum(1000000000)
            spi_right.setValue(60000)
            grid_layout.addWidget(QtWidgets.QLabel("光栅范围"), 0, 0, 1, 1)
            grid_layout.addWidget(spi_top, 0, 1, 1, 1)
            grid_layout.addWidget(QtWidgets.QLabel("——"), 0, 2, 1, 1)
            grid_layout.addWidget(spi_bottom, 0, 3, 1, 1)
            grid_layout.addWidget(QtWidgets.QLabel("采样范围"), 1, 0, 1, 1)
            grid_layout.addWidget(spi_left, 1, 1, 1, 1)
            grid_layout.addWidget(QtWidgets.QLabel("——"), 1, 2, 1, 1)
            grid_layout.addWidget(spi_right, 1, 3, 1, 1)
            group.setLayout(grid_layout)
            v_layout.addWidget(group)
            group_item = [spi_top, spi_bottom, spi_left, spi_right]
            items.append(group_item)
        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_layout.addItem(spacer)
        widget.setLayout(v_layout)
        self.items = widget
        return items

    def SaveData(self, data, file_index):
        for i in range(0, len(file_index)):
            top = max(file_index[i][0], 1)
            bottom = min(file_index[i][1], data.shape[0])
            left = max(file_index[i][2], 1)
            right = min(file_index[i][3], data.shape[1])
            file_name = 'S' + str(top) + '-' + str(bottom) + '_' + 'T' + str(left) + '-' + str(right) + '_' + "P" \
                        + str(bottom - top + 1) + '_'
            data_s = data[top - 1:bottom, left - 1:right].T
            if data_s.dtype != numpy.dtype('float32'):
                data_s = data_s.astype('float32')
            data_s.tofile(file_name + '.bin')
        self.finish.emit()
