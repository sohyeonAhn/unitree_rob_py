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

        self.plot_widget_position_dot = self.findChild(pg.PlotWidget, "position_graph_1")
        self.plot_widget_position_bar = self.findChild(pg.PlotWidget, "position_graph_2")
        self.plot_widget_quaternion_dot = self.findChild(pg.PlotWidget, "quaternion_graph_dot")
        self.plot_widget_quaternion_bar = self.findChild(pg.PlotWidget, "quaternion_graph_bar")

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(200)

    def graph_PositionGraph_test(self, x_values, y_values):

        self.plot_point = self.plot_widget_position_dot.plot(x_values, y_values, pen=None, symbol='o')

        self.plot_widget_position_dot.setXRange(-5, 5)
        self.plot_widget_position_dot.setYRange(-5, 5)

    def graph_PositionValue_test(self, x_labels, y_values):
        self.plot_widget_position_bar.clear()  # Clear the plot to update it with new data
        self.plot_widget_position_bar.setLabel('left', 'Position')  # Set the Y-axis label
        self.plot_widget_position_bar.setLabel('bottom', 'Time (s)')  # Set the X-axis label
        self.plot_widget_position_bar.setXRange(0, len(x_labels) + 1)  # Set the X-axis range

        # Plot the bar graph
        bar_chart = pg.BarGraphItem(x=np.arange(len(x_labels)) + 1, height=y_values, width=0.2)
        self.plot_widget_position_bar.addItem(bar_chart)

        # Set the X-axis tick labels
        ticks = [tick + 0.5 for tick in range(1, len(x_labels) + 1)]
        self.plot_widget_position_bar.getAxis('bottom').setTicks([list(zip(ticks, x_labels))])

        # Set the Y-axis range
        max_value = max(y_values)
        self.plot_widget_position_bar.setYRange(-1, max_value + 0.5)

        # Add labels on top of the bars
        for index, value in enumerate(y_values):
            label = pg.TextItem(str(value), anchor=(0.5, 1))
            label.setPos(index + 1, value)
            self.plot_widget_position_bar.addItem(label)

    def graph_Quaternion_Graph_test(self,x_values,y_values):

        # self.plot_point_Q = self.plot_widget_position_dot.plot(x_values, y_values, pen=None, symbol='o')
        i=0
    def graph_Quaternion_Value_test(self,x_labels, y_values):

        self.plot_widget_quaternion_bar.clear()
        self.plot_widget_quaternion_bar.setLabel('left', 'Quaternion')
        self.plot_widget_quaternion_bar.setLabel('bottom', 'Time (s)')
        self.plot_widget_quaternion_bar.setXRange(0, len(x_labels) + 1)

        # Plot the bar graph
        bar_chart = pg.BarGraphItem(x=np.arange(len(x_labels)) + 1, height=y_values, width=0.2)
        self.plot_widget_quaternion_bar.addItem(bar_chart)

        # Set the X-axis tick labels
        ticks = [tick + 0.5 for tick in range(1, len(x_labels) + 1)]
        self.plot_widget_quaternion_bar.getAxis('bottom').setTicks([list(zip(ticks, x_labels))])

        # Set the Y-axis range
        max_value = max(y_values)
        self.plot_widget_quaternion_bar.setYRange(-1, max_value + 0.5)

        # Add labels on top of the bars
        for index, value in enumerate(y_values):
            label = pg.TextItem(str(value), anchor=(0.5, 1))
            label.setPos(index + 1, value)
            self.plot_widget_quaternion_bar.addItem(label)

    def update_plot(self):
        self.dialog_data_position = self.parent.plot_data_position
        self.dialog_data_quaternion = self.parent.view_data_quaternion
        if self.dialog_data_position:
            y_values = self.dialog_data_position
            x_values = range(1, len(y_values) + 1)

            y_values_2 = [self.dialog_data_position[0]]
            x_values_2 = [self.dialog_data_position[1]]

            self.graph_PositionGraph_test(x_values_2, y_values_2)
            self.graph_PositionValue_test(x_values, y_values)

        if self.dialog_data_quaternion:

            x_value_Q_dot = [self.dialog_data_quaternion[1]]
            y_value_Q_dot = [self.dialog_data_quaternion[2]]

            y_value_Q_bar = self.dialog_data_quaternion
            x_value_Q_bar = range(1, len(y_value_Q_bar) + 1)

            self.graph_Quaternion_Graph_test(x_value_Q_dot,y_value_Q_dot)
            self.graph_Quaternion_Value_test(x_value_Q_bar,y_value_Q_bar)

