#!/usr/bin/env python
import sys
from PyQt4 import QtCore, QtGui
from classes.Session import ByuSession, ByuSessionError
from ByuGradesWindow import Ui_ByuGradesWindow
from AboutWidget import Ui_AboutWidget
from classes.Semester import Semester, SemesterError
from classes.Transcript import Transcript, TranscriptError
from os.path import isfile
import os

class MyAboutWindow(QtGui.QWidget, Ui_AboutWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)

class MyByuGradesWindow(QtGui.QMainWindow):
	def __init__(self, parent=None, filename=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_ByuGradesWindow()
		self.ui.setupUi(self)
		self.about_window = None
		self.inputs_filename = "byugrades.inputs"
		self.filename = filename
		self.byu_session = None
		self.username = None
		self.password = None
		
		# Load inputs if they are saved
		if isfile(self.inputs_filename):
			self.getInputs()
			self.ui.save_checkbox.setChecked(True)
		
		# Disble the year input if necessary
		self.checkYearInput()
		
		# Slots
		QtCore.QObject.connect(self.ui.actionAbout,QtCore.SIGNAL("triggered()"), self.showAboutWidget)
		QtCore.QObject.connect(self.ui.actionSave,QtCore.SIGNAL("triggered()"), self.saveFile)
		QtCore.QObject.connect(self.ui.actionToTxt,QtCore.SIGNAL("triggered()"), self.exportFile)
		QtCore.QObject.connect(self.ui.grades_button,QtCore.SIGNAL("clicked()"), self.getGrades)
		QtCore.QObject.connect(self.ui.clear_button,QtCore.SIGNAL("clicked()"), self.clearInputs)
		QtCore.QObject.connect(self.ui.save_checkbox,QtCore.SIGNAL("clicked()"), self.saveInputs)
		QtCore.QObject.connect(self.ui.semester_input,QtCore.SIGNAL("currentIndexChanged(int)"), self.checkYearInput)
		QtCore.QObject.connect(self.ui.year_input,QtCore.SIGNAL("returnPressed(QString)"),self.ui.grades_button,QtCore.SIGNAL("clicked()"));
		QtCore.QObject.connect(self.ui.username_input,QtCore.SIGNAL("textChanged(QString)"), self.saveInputs)
		QtCore.QObject.connect(self.ui.password_input,QtCore.SIGNAL("textChanged(QString)"), self.saveInputs)
		QtCore.QObject.connect(self.ui.semester_input,QtCore.SIGNAL("currentIndexChanged(int)"), self.saveInputs)
		QtCore.QObject.connect(self.ui.year_input,QtCore.SIGNAL("textChanged(QString)"), self.saveInputs)
		
	def showAboutWidget(self):
		if self.about_window is None:
			self.about_window = MyAboutWindow(self)
		self.about_window.show()
		
	def getGrades(self):
		self.ui.classes_output.setPlainText("Collecting grades. This may take up to a few minutes...")
		app.processEvents()
	
		username = str(self.ui.username_input.text())
		password = str(self.ui.password_input.text())
		semester_name = str(self.ui.semester_input.currentText())
		year = str(self.ui.year_input.text())
		
		try:
			# Collect credentials and semester requested
			if not self.byu_session or self.username != username or self.password != password:
				self.username = username
				self.password = password
				self.byu_session = ByuSession(username, password);
			
			# Get the desired semester
			semester = self.byu_session.getTargetSemester(semester_name, year)
			
			# Set the last input accordingly
			if not semester or semester == "None":
				box_text = "There are no classes listed for " + semester_name + " " + year + "."
				self.ui.classes_output.setPlainText(box_text)
				return
			
			# Set the "GPA" field
			self.ui.gpa_output.setText(str(semester.getGPA()))
			
			# Set the Semester output
			self.ui.classes_output.setPlainText(str(semester))
			
		except ByuSessionError as e:
			self.ui.classes_output.setPlainText(e.value)
			return
		#except:
			# self.ui.classes_output.setPlainText("There was an error while retrieving your information. Please try again.")
			
	def checkYearInput(self):
		if str(self.ui.semester_input.currentText()) == "All":
			self.ui.year_input.setEnabled(False)
		else:
			self.ui.year_input.setEnabled(True)
	
	def exportFile(self):
		new_file = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File'))
		self.saveFileWithName(new_file, ".txt")
	
	def saveFile(self):
		if not self.filename:
			self.filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File'))
		self.saveFileWithName(self.filename, ".txt")
			
	def saveFileWithName(self, filename, extension):
		if not filename:
			return
		if not filename.endswith(extension):
			filename += extension
		with open(filename, 'wt') as file:
			file.write(self.ui.classes_output.toPlainText())
			file.close()
	
	def saveInputs(self):
		if self.ui.save_checkbox.isChecked():
			username = str(self.ui.username_input.text())
			password = str(self.ui.password_input.text())
			semester = str(self.ui.semester_input.currentText())
			year = str(self.ui.year_input.text())
			file_string = "username: " + username + "\n" + "password: " + password + "\n" + "semester: " + semester + "\n" + "year: " + year
			
			file = open(self.inputs_filename, 'w')
			file.write(file_string)
			file.close()
		else:
			if isfile(self.inputs_filename): 
				os.remove(self.inputs_filename)
	
	def clearInputs(self):
		self.ui.username_input.clear()
		self.ui.password_input.clear()
		self.ui.semester_input.setCurrentIndex(0)
		self.ui.year_input.clear()
		
	def getInputs(self):
		text = open(self.inputs_filename).read()
		inputs = text.split("\n");
		for line in inputs:
			if line.startswith("username: "):
				self.ui.username_input.setText(line[10:])
			if line.startswith("password: "):
				self.ui.password_input.setText(line[10:])
			if line.startswith("semester: "):
				index = self.ui.semester_input.findText(line[10:], QtCore.Qt.MatchFixedString)
				if index >= 0:
					self.ui.semester_input.setCurrentIndex(index)
				pass
			if line.startswith("year: "):
				self.ui.year_input.setText(line[6:])

class WindowContainer(object):
    def __init__(self):
        self.window_list = []
        self.add_new_window()

    def add_new_window(self):
        repo = Repository()
        ctrl = Controller(repo)
        spawn = Main(ctrl, self)
        self.window_list.append(spawn)
        spawn.show()
				
if __name__ == "__main__":
	
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	else:
		filename = None
	
	app = QtGui.QApplication(sys.argv)
	myapp = MyByuGradesWindow(None, filename)
	myapp.setFixedSize(600, 600)
	myapp.show()
	
	sys.exit(app.exec_())