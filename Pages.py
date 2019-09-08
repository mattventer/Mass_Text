from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainScreen(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)
        self.showNumberInputs()
        self.showProgramOutput()
        self.showExcelImport()
        # Window
        self.resize(840, 540)
        self.setWindowTitle('Mass Text by Matthew Venter')
        self.setWindowIcon(QIcon('icon.png'))
        self.showMenu()
        self.show()
        
    def showMenu(self):
        # Actions
        importAct = QAction(QIcon('import_icon.png'), 'Import List', self)        
        importAct.setShortcut('Ctrl+I')
        importAct.setStatusTip('Import .XLSX file')
        #importAct.triggered.connect(qApp.quit)

        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        # Menus
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(importAct)
        fileMenu.addAction(exitAct)
    
    def showNumberInputs(self):
        # User
        user_num = QLabel('User Phone Number:', self)
        user_num.setStyleSheet("QLabel {color: blue;}")
        user_num.adjustSize()
        user_num.move(20, 55)
        
        user_num_le = QLineEdit(self)
        user_num_le.resize(190, 28)
        user_num_le.move(190, 50)
        

        # Twilio
        twil_num = QLabel('Twilio Phone Number:', self)
        twil_num.setStyleSheet("QLabel {color: blue;}")
        twil_num.adjustSize()
        twil_num.move(20, 105)
        
        twil_num_le = QLineEdit(self)
        twil_num_le.resize(190, 28)
        twil_num_le.move(190, 100)
    
    def showProgramOutput(self):
        output_label = QLabel('Program Output:', self)
        output_label.setStyleSheet("QLabel {color: orange;}")
        output_label.adjustSize()
        output_label.move(20, 200)

        output_textbox = QPlainTextEdit(self)
        output_textbox.resize(375, 290)
        output_textbox.move(20, 225)
        # TODO use setPlainText(), insertPlainText(), and appendPlainText() 
        # TODO to grab from massText
    
    def showExcelImport(self):
        output_label = QLabel('Phone Numbers:', self)
        output_label.setStyleSheet("QLabel {color: darkblue;}")
        output_label.adjustSize()
        output_label.move(450, 30)

        import_button = QPushButton('Import list', self)
        import_button.adjustSize()
        import_button.move(575, 27)
        # TODO import file and pass to program