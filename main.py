import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QComboBox, QPushButton, QVBoxLayout, QDialog
import pandas as pd

class SelectAxisDialog(QDialog):
	def __init__(self, labels):
		super().__init__()
		select_label = ["Pick column name"] + labels
		self.setWindowTitle("Select Axis")
		self.setGeometry(100, 100, 300, 150)
		layout = QVBoxLayout()

		self.combo_x = QComboBox()
		self.combo_x.addItems(select_label)
		self.combo_x.setCurrentText("Pick an Option for X Axis")
		layout.addWidget(self.combo_x)

		self.combo_y = QComboBox()
		self.combo_y.addItems(select_label)
		self.combo_y.setCurrentText("Pick an Option for Y Axis")
		layout.addWidget(self.combo_y)

		confirm_button = QPushButton("Confirm Selections")
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

	def browseFiles(self):
		# Browse file
		filename, _ = QFileDialog.getOpenFileName(self, "Select a File", "/",
												  "Excel/csv files (*.xlsx *.xls *.csv);;All Files (*)")
		if not filename:
			return

		print(filename)
		# Check file is valid
		not_file = not os.path.isfile(filename)
		self.is_xls = filename.endswith('.xls')
		self.is_xlsx = filename.endswith('.xlsx')
		self.is_csv = filename.endswith('.csv')
		bad_file_type = not (self.is_xls or self.is_xlsx or self.is_csv)
		if not_file or bad_file_type:  # Bad file
			print("Bad")
			self.lbl_loaded.setText("Bad")
			self.file_accepted = False
		else:  # Good file
			print("Good")
			self.lbl_loaded.setText("Good")
			self.file_accepted = True
			self.path = filename
			self.load_columns_names()

	def load_columns_names(self):
		# Check file is good
		if not self.file_accepted:
			return
		if self.is_xls or self.is_xlsx:
			df = pd.read_excel(self.path)
		elif self.is_csv:
			df = pd.read_csv(self.path)
		labels = list(df.columns)

		dialog = SelectAxisDialog(labels)
		if dialog.exec_():
			self.x_selection = dialog.combo_x.currentText()
			self.y_selection = dialog.combo_y.currentText()
			print(f"X Axis: {self.x_selection}")
			print(f"Y Axis: {self.y_selection}")

def window():
	app = QtWidgets.QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())

window()