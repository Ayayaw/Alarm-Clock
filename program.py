import multiprocessing
import sys
import os
import datetime
from datetime import datetime
from time import sleep
import PyQt5
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIntValidator
from multiprocessing import *
import winsound


class App(QWidget):
    
    def __init__(self):
        super().__init__()
        print("Program running...")
        self.title = "Alarm Clock"
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.setStyleSheet(open("C:\\Users\\*****\\Desktop\\Alarm Clock\\SyNet.qss","r").read()) #Edit Here
        self.initUI()
    
    
    def initUI(self):
        self.setWindowTitle(self.title)

        #region-Labels
        ####-Hour-Minute-Second-####
        hour = QtWidgets.QLabel(self)
        hour.setText("Hour")
        hour.move(25,25)
        hour.setFont(QtGui.QFont("Times",14, QtGui.QFont.Bold))
        hour.setStyleSheet("font: 18px;color: red;") #CSS

        minutes = QtWidgets.QLabel(self)
        minutes.setText("Min")
        minutes.move(85,25)
        minutes.setFont(QtGui.QFont("Times",14, QtGui.QFont.Bold))
        minutes.setStyleSheet("font: 18px;color: red;") #CSS

        seconds = QtWidgets.QLabel(self)
        seconds.setText("Sec")
        seconds.move(145,25)
        seconds.setFont(QtGui.QFont("Times",14, QtGui.QFont.Bold))
        seconds.setStyleSheet("font: 18px;color: red;") #CSS
        ####-Hour-Minute-Second-####

        label = QtWidgets.QLabel(self)
        label.setText("When to wake you up")
        label.move(50,115)
        label.setFont(QtGui.QFont("Times",14, QtGui.QFont.Bold))
        label.setStyleSheet("font: 18px;color: red;") #CSS
        #endregion

        #region-Buttons
        ####-Buttons-####
        button = QPushButton("Set Alarm",self)
        button.setToolTip("Set Alarm")
        button.setGeometry(50,150,160,60)
        button.clicked.connect(self.settingUp)

        button3 = QPushButton("Exit", self)
        button3.setToolTip("Exit")
        button3.setGeometry(300,50,160,60)
        button3.clicked.connect(self.quit)
        button3.setAutoDefault(True)


        ####-Buttons-####
        #endregion

        #region-Inputs
        ####-Inputs-####
        validator_hour = QIntValidator(10, 25, self)
        self.hour_input = QLineEdit(self)
        self.hour_input.setValidator(validator_hour)
        self.hour_input.setGeometry(25,50,45,45)
        self.hour_input.setStyleSheet("background: rgb(255,192,203); font: 18px;")

        validator_min = QIntValidator(10, 59, self)
        self.min_input = QLineEdit(self)
        self.min_input.setValidator(validator_min)
        self.min_input.setGeometry(85,50,45,45)
        self.min_input.setStyleSheet("background: rgb(255,192,203); font: 18px;")

        self.sec_input = QLineEdit(self)
        self.sec_input.setValidator(validator_min)
        self.sec_input.setGeometry(145,50,45,45)
        self.sec_input.setStyleSheet("background: rgb(255,192,203); font: 18px;")
        ####-Inputs-####
        #endregion

        self.show()
    
    def getCurrentTime(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        return current_time

    def timer(self,alarm_time):

        QtCore.QCoreApplication.processEvents() #You should call QtCore.QCoreApplication.processEvents() within your for loop to make the Qt's event loop proceed the incoming event (from keyboard or mouse or sleep)
        
        current_time = self.getCurrentTime()

        start_date = datetime.strptime(current_time,'%H:%M:%S')
        end_date = datetime.strptime(alarm_time,'%H:%M:%S')

        date_difference = end_date - start_date
        
        alarm_time_hour = round(date_difference.seconds/3600)
        alarm_time_min = round(date_difference.seconds//60)%60
        alarm_time_sec = date_difference.seconds % 60
        
        self.hour_input.setText(str(alarm_time_hour))
        self.min_input.setText(str(alarm_time_min))
        self.sec_input.setText(str(alarm_time_sec))
        print(self.hour_input.text(),self.min_input.text(),self.sec_input.text())
        sleep(1)

    def settingUp(self):
        first_alarm_time = [int(self.hour_input.text()),int(self.min_input.text()),int(self.sec_input.text())]
        first_alarm_time = ':'.join(str(v) for v in first_alarm_time)

        try:
            if((int(self.hour_input.text()) > 24)):
                print("Enter time in 24 hour format!")
            elif(int(self.min_input.text()) > 59):
                print("Enter minute in range (00 - 59) ")
            elif(int(self.sec_input.text()) > 59):
                print("Enter second in range (00 - 59) ")

            else:
                self.hour_input.setEnabled(False)
                self.min_input.setEnabled(False)
                self.sec_input.setEnabled(False)
                 

                while True:
                    print('Alarm set',first_alarm_time)
                    proc = multiprocessing.Process(target=self.timer(first_alarm_time))
                    proc.start()
                    if((self.hour_input.text() == str(0)) and (self.min_input.text() == str(0)) and (self.sec_input.text() == str(0))):
                        break
                print('Proccess Done!')
                for i in range(5):
                    winsound.Beep(500, 700)
                self.hour_input.setEnabled(True)
                self.min_input.setEnabled(True)
                self.sec_input.setEnabled(True)
                proc.join()
                   
        except:
            #traceback.print_exc()
            print("Please enter a valid input!")
            
    def quit(self):
        os._exit(1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
