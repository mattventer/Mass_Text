from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import massTextUtils as utils
from twilio.rest import Client
import openpyxl
import sys
import time
###############################################################################
###############################################################################
# Input from GUI
# Your Account SID from twilio.com/console
account_sid = None
# Your Auth Token from twilio.com/console
auth_token = None
# Number that the texts will be sent from
twil_num = None
msg_data = None
client = None
# Filepath to stored number list
file_path = None
wb = None
excel_sheet = None
# Holds list of numbers
contact_list = []
surpress_output = False


class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.showNumberInputs()
        self.showProgramOutput()
        self.showExcelImport()
        # Window
        self.setFixedSize(840, 540)
        self.setWindowTitle('Mass Text by Matthew Venter')
        self.setWindowIcon(QIcon('Resources/icon.png'))
        self.showMenu()
        self.show()

    def showMenu(self):
        # Actions
        self.importAct = QAction(QIcon('import_icon.png'), 'Import List', self)
        self.importAct.setShortcut('Ctrl+I')
        self.importAct.setStatusTip('Import .XLSX file')
        self.importAct.triggered.connect(self.importBtnClicked)

        self.exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(self.close)

        # Menus
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('File')
        self.fileMenu.addAction(self.importAct)
        self.fileMenu.addAction(self.exitAct)

    def showNumberInputs(self):
        # Twilio
        self.twil_num_label = QLabel('Twilio Phone Number:', self)
        self.twil_num_label.adjustSize()
        self.twil_num_label.move(20, 63)
        self.twil_num_label.setToolTip(
            "This is the Twilio registered phone number that will send the messages")

        self.twil_num_le = QLineEdit(self)
        self.twil_num_le.resize(200, 25)
        self.twil_num_le.move(185, 60)

        # Auth
        self.twil_sid_label = QLabel('Twilio SID:', self)
        self.twil_sid_label.adjustSize()
        self.twil_sid_label.move(20, 100)
        self.twil_sid_label.setToolTip(
            "Twilio Account SID.\nFound in Twilio Dashboard")

        self.twil_sid_le = QLineEdit(self)
        self.twil_sid_le.resize(200, 25)
        self.twil_sid_le.move(185, 98)

        self.twil_authid_label = QLabel('Twilio Auth ID:', self)
        self.twil_authid_label.adjustSize()
        self.twil_authid_label.move(20, 140)
        self.twil_authid_label.setToolTip(
            "Twilio Auth Token.\nFound in Twilio Dashboard")

        self.twil_authid_le = QLineEdit(self)
        self.twil_authid_le.resize(200, 25)
        self.twil_authid_le.move(185, 137)

        # Save
        self.set_btn = QPushButton('Create Client', self)
        self.set_btn.clicked.connect(self.setBtnClick)
        self.set_btn.adjustSize()
        self.set_btn.move(290, 180)
        self.set_btn.setToolTip(
            "Create Twilio Client using provided information")

    def showProgramOutput(self):
        self.output_label = QLabel('Program Output:', self)
        self.output_label.setStyleSheet("QLabel {color: Dodgerblue}")
        self.output_label.adjustSize()
        self.output_label.move(20, 210)

        self.surpress_ckbx = QCheckBox("Surpress output", self)
        self.surpress_ckbx.adjustSize()
        self.surpress_ckbx.setChecked(False)
        self.surpress_ckbx.stateChanged.connect(
            lambda: self.btnstate(self.surpress_ckbx))
        self.surpress_ckbx.move(250, 210)
        self.surpress_ckbx.setToolTip("Enable to turn-off message statuses")

        self.output_textbox = QPlainTextEdit(self)
        self.output_textbox.setReadOnly(True)
        self.output_textbox.setStyleSheet(
            "QPlainTextEdit {background-color: grey}")
        self.output_textbox.resize(370, 275)
        self.output_textbox.move(20, 235)

        self.msg_lbl = QLabel("Message:", self)
        self.msg_lbl.setStyleSheet("QLabel {color: Dodgerblue}")
        self.msg_lbl.adjustSize()
        self.msg_lbl.move(425, 325)
        self.msg_lbl.setToolTip(
            "Note: Messages over 160 characters will be\nsent in multiple texts.")
        
        self.msg_note = QLabel(
            "Note: Include 'name' within message to be\nreplaced by recipient's first name.", self)
        self.msg_note.adjustSize()
        self.msg_note.setStyleSheet("QLabel {color: lightgrey}")
        self.msg_note.move(425, 500)

        self.msg_to_send = QPlainTextEdit(self)
        self.msg_to_send.setStyleSheet(
            "QPlainTextEdit {background-color: grey}")
        self.msg_to_send.resize(395, 155)
        self.msg_to_send.move(425, 345)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(160, 515, 230, 20)
        self.progress.setMaximum(100)

        self.run_btn = QPushButton("Run", self)
        self.run_btn.clicked.connect(self.runBtnClick)
        self.run_btn.adjustSize()
        self.run_btn.move(750, 510)

        self.clear_output = QPushButton("Clear", self)
        self.clear_output.clicked.connect(self.clearOutputBox)
        self.clear_output.adjustSize()
        self.clear_output.move(19, 513)



    def showExcelImport(self):
        output_label = QLabel("Phone Number List: ", self)
        output_label.setStyleSheet("QLabel {color: Dodgerblue}")
        output_label.adjustSize()
        output_label.move(425, 30)

        file_path_label = QLabel("File Path:", self)
        file_path_label.adjustSize()
        file_path_label.move(425, 50)

        self.file_path_le = QLineEdit(self)
        self.file_path_le.resize(220, 20)
        self.file_path_le.move(495, 49)

        self.numbers_list = QPlainTextEdit(self)
        self.numbers_list.setReadOnly(True)
        self.numbers_list.setStyleSheet(
            "QPlainTextEdit {background-color: grey}")
        self.numbers_list.resize(395, 250)
        self.numbers_list.move(425, 70)

        self.import_btn = QPushButton("Import", self)
        self.import_btn.adjustSize()
        self.import_btn.clicked.connect(self.importBtnClicked)
        self.import_btn.move(740, 27)
        self.import_btn.setToolTip(
            "Select an '.XLSX' file containing phone numbers in first column")

    def importBtnClicked(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, caption='Select .XLSX file')
        self.file_path_le.setText(filename)
        self.file_path = filename
        self.wb = openpyxl.load_workbook(self.file_path)
        self.excel_sheet = self.wb.active
        self.contact_list = utils.populateNumberList(self.excel_sheet)
        count = 1
        if self.contact_list:
            for num in self.contact_list:
                self.numbers_list.appendPlainText(str(count) + ": " + num.getInfo())
                count += 1

    def btnstate(self, b):
        if b.text() == "Surpress output":
            if b.isChecked() == True:
                self.surpress_output = True
                return True
            else:
                self.surpress_output = False
                return False
                

    def clearOutputBox(self):
        self.output_textbox.clear()
        print("Clearing output...")


    def setBtnClick(self):
        self.account_sid = self.twil_sid_le.text()
        self.auth_token = self.twil_authid_le.text()
        self.twil_num = utils.formatNumber(self.twil_num_le.text())
        try:
            self.client = Client(self.account_sid, self.auth_token)
            self.output_textbox.appendPlainText("Successfully created Twilio Client\n")
        except:
            self.output_textbox.appendPlainText("Unable to initialize client with SID and Auth token...")

    def runBtnClick(self):
        msg_data = self.msg_to_send.toPlainText()
        exec_time = utils.massSendSMS(
            msg_data, self.contact_list, self.excel_sheet, self)
        self.output_textbox.appendPlainText(
            "\nExecution time: " + str(round(exec_time, 2)) + " seconds")
        self.wb.save(self.file_path)
