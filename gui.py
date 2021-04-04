from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QHBoxLayout, QGridLayout, QDialog

import sys
 
class Window(QDialog):
    def __init__(self):
        super().__init__()
 
        tmplist = ['a', 'b', 'c', 'd']
        taskCombo = QComboBox(self)
        taskCombo.addItem("Apple")
        taskCombo.addItem("Pear")
        taskCombo.addItem("Lemon")
        taskCombo.addItems(tmplist)

        taskLabel = QLabel("Select appointment type: ")
        taskLabel.setBuddy(taskCombo)

        dateCombo = QComboBox(self)
        dateCombo.addItems(tmplist)
        dateLabel = QLabel("Search slots before date: ")
        dateLabel.setBuddy(dateCombo)

        #button=QPushButton('Click me',self)
        #button.setToolTip('Thank you for thinking about me')
        #button.move(100,100)

        topLayout = QHBoxLayout()
        topLayout.addWidget(taskLabel)
        topLayout.addWidget(taskCombo)
        topLayout.addStretch(1)


        midLayout = QHBoxLayout()
        midLayout.addWidget(dateLabel)
        midLayout.addWidget(dateCombo)
        midLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addLayout(midLayout, 1, 0, 1, 2)
        #mainLayout.addWidget(aa, 1, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setGeometry(200,200,320,200)
        self.setWindowTitle("NJ MVC Appointment Finder")


    def visitWeb(self):
        print(str(self.ui.taskCombo.currentText()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
