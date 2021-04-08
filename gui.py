from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QDateEdit, QTextEdit
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread,QTimer, Qt
import sys
import requests
import csv
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
from tabulate import tabulate

class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        
class Window(QDialog):
    def __init__(self):
        super().__init__()
        sys.stdout = Stream(newText=self.onUpdateText)
        
        self.initSearch()
        
        ## Widgets --------------------
        self.taskCombo = QComboBox(self)
        self.taskCombo.addItems(self.task_list)
        self.taskCombo.currentIndexChanged.connect(self.resetsearchindex)

        self.taskLabel = QLabel("Select appointment type: ")
        self.taskLabel.setBuddy(self.taskCombo)

        self.dateEdit = QDateEdit(self, calendarPopup=True)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime().addDays(30)) # default within a month
        self.dateEdit.setMinimumDateTime(QtCore.QDateTime.currentDateTime())

        self.dateLabel = QLabel("Search slots before date: ")
        self.dateLabel.setBuddy(self.dateEdit)

        self.submitBtn = QPushButton('Start search',self)
        #self.submitBtn.setToolTip('Runnnnnnnn')
        self.submitBtn.setCheckable(True)
        self.submitBtn.clicked.connect(self.TextConsl)
        
        self.autodirect = QCheckBox("Take me to the appointment page automatically (with default browser)")
        self.autodirect.setChecked(False)
        self.autodirect.toggled.connect(self.boxchecked)
        
        self.process = QTextEdit()
        self.process.moveCursor(QtGui.QTextCursor.Start)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setAlignment(Qt.AlignRight)
        
        ## layout --------------------
        topLayout = QHBoxLayout()
        topLayout.addWidget(self.taskLabel)
        topLayout.addWidget(self.taskCombo)
        topLayout.addStretch(1)

        midLayout = QHBoxLayout()
        midLayout.addWidget(self.dateLabel)
        midLayout.addWidget(self.dateEdit)
        midLayout.addStretch(1)
        
        btmLayout = QVBoxLayout()
        btmLayout.addWidget(self.submitBtn)
        btmLayout.addWidget(self.autodirect)
        btmLayout.addWidget(self.process)
        btmLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(midLayout, 1, 0, 1, 2)
        mainLayout.addLayout(btmLayout, 2, 0, 1, 2)

        self.setLayout(mainLayout)
        self.setGeometry(200,200,800,400)
        self.setWindowTitle("NJ MVC Appointment Finder")

        
        
    def onUpdateText(self, text):
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()
        
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
        
    def initSearch(self):
        self.locfile = 'locations.csv'
        self.URL_prefix = 'https://telegov.njportal.com/njmvc/AppointmentWizard'
        self.db_host = 'https://telegov.njportal.com/'
        self.non_avail_str = 'Currently, there are no appointments available at this location.'
        self.search_list = [] # hold each location for loop over
        self.search_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.web_scraper)
        self.by_task = {} # key: task, value: list of locations and url
        self.task_list = []
        self.directweb = False
        
        csvReader = csv.DictReader(open(self.locfile), delimiter=',')
        for line in csvReader:
            if line['Task'] not in self.task_list: self.task_list.append(line['Task'])
            if line['Task'] not in self.by_task: self.by_task[line['Task']] = []
            self.by_task[line['Task']].append(line)
            
    def resetsearchindex(self):
        self.search_index = 0
        
    def boxchecked(self):
        if self.autodirect.isChecked(): self.directweb = True
        else: self.directweb = False
            
    def web_scraper(self):
        seleTask = str(self.taskCombo.currentText())
        seleDate = str(self.dateEdit.date().toPyDate())
        seleloc = self.by_task[seleTask][self.search_index]
        
        page = requests.get(self.URL_prefix + '/' + seleloc['task_url'] + '/' + seleloc['url'])
        soup = BeautifulSoup(page.content, 'html.parser')
    
        if self.search_index == 0:  ## print some header
            print('{:25s} {:30s} {:15s} '.format('Location', 'Availability', 'Date'))
            print("__________________________________________________________________")
            
        if self.non_avail_str in str(soup): 
            print('{:25s} {:30s} {:15s} '.format(seleloc['Name'].strip(), 'no slots', 'na'))
        else:
            ## find available slots
            timee_list = soup.findAll('a', attrs={'class':'text-primary', 'href':True})
            timee = timee_list[0]['href'] ## get earlist time
        
            date_string = timee.split('/')[-2]
            time_string = timee.split('/')[-1]
            date_obj = datetime.strptime(date_string + ' ' + time_string, "%Y-%m-%d %H%M")
    
            if date_obj < datetime.strptime(seleDate, "%Y-%m-%d"):
                print('{:25s} {:30s} {:15s} '.format(seleloc['Name'], 'yes', str(date_obj.date())))
                if self.directweb: webbrowser.open(self.db_host + timee)
            else:
                print('{:25s} {:30s} {:15s} '.format(seleloc['Name'], 'earlist slot', str(date_obj.date())))
                
        self.search_index += 1
        if (self.search_index >= len(self.by_task[seleTask])):
            self.search_index = 0
            print('\n\nAnother round of search...\n\n')
        
    def TextConsl(self):

        if self.submitBtn.isChecked():
            self.submitBtn.setText('Stop search')
            self.submitBtn.setStyleSheet("color: magenta")
            self.timer.start(1000)  # 1s per search
            
        else:
            self.submitBtn.setText('Start search')
            self.submitBtn.setStyleSheet("")
            self.timer.stop()
        
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
