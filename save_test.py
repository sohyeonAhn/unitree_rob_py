import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np
from myunitree_value_test import myunitree
from myDialog import myDialog

class Tread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            while True:
                time.sleep(0.2)
                self.parent.sendCmd()
        except Exception as e:
            print("Tread1에서 예외 발생:")
            traceback.print_exc()

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'./control_gui.ui', self)

        self.isungb1 = myunitree()

        # Create the QAction for opening the graph_gui.ui
        self.actionGraph = QAction("Open Graph", self)
        self.actionGraph.triggered.connect(self.open_graph_window)

        # Add the QAction to the File menu
        self.fileMenu = self.menuBar().addMenu("Graph")
        self.fileMenu.addAction(self.actionGraph)

        self.connect_btn.clicked.connect(self.udp_connect)

        self.N_btn.pressed.connect(self.click_N)
        self.S_btn.pressed.connect(self.click_S)
        self.W_btn.pressed.connect(self.click_W)
        self.E_btn.pressed.connect(self.click_E)
        self.Stop_btn.clicked.connect(self.click_Stop)
        self.L_btn.pressed.connect(self.click_L)
        self.R_btn.pressed.connect(self.click_R)

        self.input_vel_0.valueChanged.connect(self.vel_0_value_changed)
        self.input_vel_1.valueChanged.connect(self.vel_1_value_changed)
        self.input_yawspeed.valueChanged.connect(self.yawspeed_value_changed)

        self.SOC_label = self.findChild(QLabel, "SOC_label")

        self.time_data = []
        self.body_height_data = []
        self.footforce_data = []

        self.plot_widget = self.findChild(pg.PlotWidget, "graph_chart")
        self.plot_curve = self.plot_widget.plot(pen="b")


        self.plot_widget = self.findChild(pg.PlotWidget, "footforce_graph")

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(200)


    def open_graph_window(self):
        self.graph_window = myDialog(self)

        self.graph_window.show()

    def sendCmd(self):
        self.isungb1.sendCmd()

        self.highstate_textBrowser.append(self.isungb1.highstate_info)

        self.data_SOC = self.isungb1.hstate_bms_SOC
        self.update_SOC_label()

        self.plot_data_bodyHeight = self.isungb1.hstate_bodyHeight
        self.plot_data_footforce = self.isungb1.hstate_footforce


    def vel_0_value_changed(self, value):
        self.vel_0_N = value
        self.vel_0_S = -value
    def vel_1_value_changed(self, value):
        self.vel_1_W = value
        self.vel_1_E = -value
    def yawspeed_value_changed(self, value):
        self.yawspeed_value_L = value
        self.yawspeed_value_R = -value

    def click_N(self):
        self.isungb1.click_N(self.vel_0_N)
    def click_S(self):
        self.isungb1.click_S(self.vel_0_S)
    def click_W(self):
        self.isungb1.click_W(self.vel_1_W)
    def click_E(self):
        self.isungb1.click_E(self.vel_1_E)
    def click_Stop(self):
        self.isungb1.click_Stop()
    def click_L(self):
        self.isungb1.click_L(self.yawspeed_value_L)
    def click_R(self):
        self.isungb1.click_R(self.yawspeed_value_R)

    def udp_connect(self):
        try:
            self.isungb1.connect()
            h1 = Tread1(self)
            h1.start()
        except Exception as e:
            print("udp_connect에서 예외 발생:")
            traceback.print_exc()

    def update_SOC_label(self):

        self.SOC_label.setText("{:.1f}%".format(self.data_SOC))  # The {:.1f} format specifies one decimal place

    def graph_bodyHeight(self):
        # Add new data to the plot
        if self.plot_data_bodyHeight:
            current_time = time.time()
            self.time_data.append(current_time)
            self.body_height_data.append(self.plot_data_bodyHeight)
            # Remove old data to keep the plot window fixed (adjust the range as needed)
        max_time_window = 10  # Display the last 10 seconds of data
        while self.time_data[-1] - self.time_data[0] > max_time_window:
            self.time_data.pop(0)
            self.body_height_data.pop(0)

        # Update the plot
        self.plot_curve.setData(x=np.array(self.time_data) - self.time_data[0], y=self.body_height_data)

    def graph_footforce(self):
        if self.plot_data_footforce:
            x_labels = ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            y_values = self.plot_data_footforce

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
        self.graph_bodyHeight()
        self.graph_footforce()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()