import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np

class myDialog(QDialog):
    def __init__(self,parent):
        super().__init__()
        # super().__init__(parent) # parent 입력하면 modal

        uic.loadUi(r'./graph_gui.ui', self)

        self.parent = parent # 상위 윈도우의 데이터를 접근
        # print(self.parent.test)
        self.dialog_data_footforce = self.parent.plot_data_footforce

        self.plot_widget = self.findChild(pg.PlotWidget, "footforce_graph")

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(200)


    def graph_footforce(self):
        if self.dialog_data_footforce:
            x_labels = ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            y_values = self.dialog_data_footforce

            self.plot_widget.clear()  # Clear the plot to update it with new data
            self.plot_widget.setLabel('left', 'Footforce')  # Set the Y-axis label
            self.plot_widget.setLabel('bottom', 'Time (s)')  # Set the X-axis label
            self.plot_widget.setXRange(0, len(x_labels) + 1)  # Set the X-axis range

            # Plot the bar graph
            bar_chart = pg.BarGraphItem(x=np.arange(len(x_labels)) + 1, height=y_values, width=0.6)
            self.plot_widget.addItem(bar_chart)

            # Set the X-axis tick labels
            ticks = [tick + 0.5 for tick in range(1, len(x_labels) + 1)]
            self.plot_widget.getAxis('bottom').setTicks([list(zip(ticks, x_labels))])

            # Set the Y-axis range
            max_value = max(y_values)
            self.plot_widget.setYRange(0, max_value + 5)

            # Add labels on top of the bars
            for index, value in enumerate(y_values):
                label = pg.TextItem(str(value), anchor=(0.5, 1))
                label.setPos(index + 1, value)
                self.plot_widget.addItem(label)

    def update_plot(self):
        # self.graph_bodyHeight()
        self.graph_footforce()