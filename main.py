import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QComboBox, QPushButton, QVBoxLayout, QDialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns

class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def ScatterPlot(self, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        sns.scatterplot(x=x, y=y, ax=ax)
        ax.set_xlabel(x.name)
        ax.set_ylabel(y.name)
        self.canvas.draw()

class SelectAxisDialog(QDialog):
	def __init__(self, labels):
		super().__init__()
		# General
		select_label = ["Pick column name"] + labels
		self.setWindowTitle("Select Axis")
		self.setGeometry(100, 100, 300, 150)
		layout = QVBoxLayout()
		# X Axis
		self.combo_x = QComboBox()
		self.combo_x.addItems(select_label)
		self.combo_x.setCurrentText("Pick an Option for X Axis")
		layout.addWidget(self.combo_x)
		# Y Axis
		self.combo_y = QComboBox()
		self.combo_y.addItems(select_label)
		self.combo_y.setCurrentText("Pick an Option for Y Axis")
		layout.addWidget(self.combo_y)
		# Confirm Btn
		confirm_button = QPushButton("Select")
		confirm_button.clicked.connect(self.accept)
		layout.addWidget(confirm_button)

		self.setLayout(layout)

class MyWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(500, 100, 1200, 800)
		self.setWindowTitle("Pro Visualize")
		self.initUI()

	def initUI(self):
		# Load test
		self.lbl_text = QtWidgets.QLabel(self)
		self.lbl_text.setText("Load File: ")
		self.lbl_text.move(50, 50)
		# Btn load
		self.btn_load = QtWidgets.QPushButton(self)
		self.btn_load.setText("Load")
		self.btn_load.clicked.connect(self.browseFiles)
		self.btn_load.move(50, 90)
		# After loaded text
		self.lbl_loaded = QtWidgets.QLabel(self)
		self.lbl_loaded.setText("")
		self.lbl_loaded.move(170, 90)
		# Plot
		self.plot_widget = PlotWidget(self)
		self.plot_widget.setGeometry(50, 150, 1100, 600)

	def browseFiles(self):
		# Browse file
		filename, _ = QFileDialog.getOpenFileName(self, "Select a File", "/",
												  "Excel/csv files (*.xlsx *.xls *.csv);;All Files (*)")
		# Check that we got filename
		if not filename:
			return
		print(filename)
		# Check file is valid
		not_file = not os.path.isfile(filename)
		if not_file:
			self.lbl_loaded.setText("Invalid File")
			return
		# Check file Type
		self.is_xls = filename.endswith('.xls')
		self.is_xlsx = filename.endswith('.xlsx')
		self.is_csv = filename.endswith('.csv')
		bad_file_type = not (self.is_xls or self.is_xlsx or self.is_csv)
		if bad_file_type:  # Bad file
			print("Bad")
			self.lbl_loaded.setText("Invalid File")
			self.file_accepted = False
			return
		else:  # Good file
			print("Good")
			self.lbl_loaded.setText("File Loaded")
			self.file_accepted = True
			self.path = filename
			self.load_columns_names()

	def load_columns_names(self):
		# Check file is good
		if not self.file_accepted:
			return
		if self.is_xls or self.is_xlsx:
			self.df = pd.read_excel(self.path)
		elif self.is_csv:
			self.df = pd.read_csv(self.path)
		labels = list(self.df.columns)
		# Open dialog to choose columns
		dialog = SelectAxisDialog(labels)
		if dialog.exec_():
			self.x_selection = dialog.combo_x.currentText()
			self.y_selection = dialog.combo_y.currentText()
			print(f"X Axis: {self.x_selection}")
			print(f"Y Axis: {self.y_selection}")
			self.plot_data()

	def plot_data(self):
		if self.x_selection in self.df.columns and self.y_selection in self.df.columns:
			x = self.df[self.x_selection]
			y = self.df[self.y_selection]
			self.plot_widget.ScatterPlot(x, y)
		else:
			if self.x_selection in self.df.columns:
				x = self.df[self.x_selection]
				self.plot_widget
				# Histsogram
				pass
			elif self.y_selection in self.df.columns:
				# Histogram
				pass
			else:
				print("Invalid column selection")

def window():
	app = QtWidgets.QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())

window()