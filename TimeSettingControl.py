from Ui.TimeSettingWindow import Ui_Dialog_time_setting
from PyQt5 import QtWidgets


class TimeSettingControl(QtWidgets.QDialog, Ui_Dialog_time_setting):
    def __init__(self, ch_num):
        super(TimeSettingControl, self).__init__()
        self.setupUi(self)
        self.items = [None] * 3
        self.group = []
        sensor_num = 3
        for i in range(0, ch_num):
            self.comboBox_channel.addItem("通道" + str(i + 1))
            group = QtWidgets.QGroupBox()
            spi_num = QtWidgets.QSpinBox()
            is_use = QtWidgets.QCheckBox()
            is_use.setChecked(True)
            spi_num.setMinimum(1)
            spi_num.setValue(sensor_num)
            spi_num.setMaximum(15)
            spi_num.valueChanged.connect(self.SensorChange)
            grid_layout = QtWidgets.QGridLayout()
            grid_layout.addWidget(QtWidgets.QLabel("是否启用"), 0, 0, 1, 1)
            grid_layout.addWidget(is_use, 0, 1, 1, 1)
            grid_layout.addWidget(QtWidgets.QLabel("光栅个数"), 0, 2, 1, 1)
            grid_layout.addWidget(spi_num, 0, 3, 1, 1)
            items = self.CreateItems(sensor_num, i)
            grid_layout.addWidget(self.items[i], 1, 0, 1, 4)
            grid_layout.setSpacing(0)
            group.setLayout(grid_layout)
            self.stackedWidget_Item.addWidget(group)
            group_item = [is_use, items]
            self.group.append(group_item)

    def CreateItems(self, num, index):
        widget = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout()
        items = []
        for i in range(0, num):
            group = QtWidgets.QGroupBox("光栅范围" + str(i + 1))
            grid_layout = QtWidgets.QGridLayout()
            spi_index = QtWidgets.QSpinBox()
            spi_left = QtWidgets.QSpinBox()
            spi_right = QtWidgets.QSpinBox()
            spi_index.setMaximum(2000)
            spi_index.setValue(i)
            spi_left.setMaximum(1000000000)
            spi_right.setMaximum(1000000000)
            spi_right.setValue(60000)
            grid_layout.addWidget(QtWidgets.QLabel("光栅序号"), 0, 0, 1, 1)
            grid_layout.addWidget(spi_index, 0, 1, 1, 3)
            grid_layout.addWidget(QtWidgets.QLabel("数据范围"), 1, 0, 1, 1)
            grid_layout.addWidget(spi_left, 1, 1, 1, 1)
            grid_layout.addWidget(QtWidgets.QLabel("——"), 1, 2, 1, 1)
            grid_layout.addWidget(spi_right, 1, 3, 1, 1)
            group.setLayout(grid_layout)
            v_layout.addWidget(group)
            group_item = [spi_index, spi_left, spi_right]
            items.append(group_item)
        # v_layout.setSpacing(0)
        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        v_layout.addItem(spacer)
        widget.setLayout(v_layout)
        self.items[index] = widget
        return items

    def SensorChange(self, value):
        layout = self.stackedWidget_Item.currentWidget().layout()
        index = self.stackedWidget_Item.currentIndex()
        # self.Items.hide()
        layout.removeWidget(self.items[index])
        self.group[index][1] = self.CreateItems(value, index)
        # self.Items.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        layout.addWidget(self.items[index], 1, 0, 1, 4)

