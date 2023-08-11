import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np

class PositionDialog(QDialog):
    def __init__(self,parent):
        super().__init__()
        # super().__init__(parent) # parent 입력하면 modal
        uic.loadUi(r'./position_dialog_gui.ui', self)
        self.parent = parent # 상위 윈도우의 데이터를 접근
        # print(self.parent.test)

        self.time_data = []
        self.y_data =[]
        self.x_data = []

        self.plot_widget_1 = self.findChild(pg.PlotWidget, "position_graph_1")

        self.plot_widget = self.findChild(pg.PlotWidget, "position_graph_2")

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(200)

    def graph_PositionGraph_test(self, x_values, y_values):

        self.plot_point = self.plot_widget_1.plot(x_values, y_values, pen=None, symbol='o')

        # # Add X-axis tick marks and labels
        # x_axis = pg.AxisItem(orientation='bottom')
        # x_axis.setTicks([list(zip(x_values, [str(value) for value in x_values]))])
        # self.plot_widget_1.addItem(x_axis, 'bottom')
        #
        # # Add Y-axis tick marks and labels
        # max_value = max(y_values)
        # y_ticks = [(tick, str(tick)) for tick in np.arange(0, max_value + 1, 1)]
        # y_axis = pg.AxisItem(orientation='left')
        # y_axis.setTicks([y_ticks])
        # self.plot_widget_1.addItem(y_axis, 'left')
        #
        # # Plot the scatter plot
        # self.plot_point = self.plot_widget_1.plot(x_values, y_values, pen=None, symbol='o')
        #
        # # Set the Y-axis range
        # self.plot_widget_1.setYRange(-1, max_value + 0.5)

    def graph_PositionValue_test(self, x_labels, y_values):
        self.plot_widget.clear()  # Clear the plot to update it with new data
        self.plot_widget.setLabel('left', 'Position')  # Set the Y-axis label
        self.plot_widget.setLabel('bottom', 'Time (s)')  # Set the X-axis label
        self.plot_widget.setXRange(0, len(x_labels) + 1)  # Set the X-axis range

        # Plot the bar graph
        bar_chart = pg.BarGraphItem(x=np.arange(len(x_labels)) + 1, height=y_values, width=0.2)
        self.plot_widget.addItem(bar_chart)

        # Set the X-axis tick labels
        ticks = [tick + 0.5 for tick in range(1, len(x_labels) + 1)]
        self.plot_widget.getAxis('bottom').setTicks([list(zip(ticks, x_labels))])

        # Set the Y-axis range
        max_value = max(y_values)
        self.plot_widget.setYRange(-1, max_value + 0.5)

        # Add labels on top of the bars
        for index, value in enumerate(y_values):
            label = pg.TextItem(str(value), anchor=(0.5, 1))
            label.setPos(index + 1, value)
            self.plot_widget.addItem(label)

    def update_plot(self):
        self.dialog_data_position = self.parent.plot_data_position
        if self.dialog_data_position:
            y_values = self.dialog_data_position
            x_values = range(1, len(y_values) + 1)

            y_values_2 = [self.dialog_data_position[0]]
            x_values_2 = [self.dialog_data_position[1]]

            self.graph_PositionGraph_test(y_values_2, x_values_2)
            self.graph_PositionValue_test(x_values, y_values)
