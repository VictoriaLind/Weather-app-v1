import sys
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
from datetime import date, datetime
from datetime import *
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl, QPoint, Qt
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QMovie, QIcon, QPixmap
from configparser import ConfigParser
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QEvent, QTimer, QSize, QPoint, QRect, QThread, QUrl
from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QOpenGLWidget
from pytz import timezone
from timezonefinder import TimezoneFinder
import requests

url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']



class mainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('app_PyQt_v1.ui', self)

        self.setWindowTitle('Weather App')
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.mainFrm = self.mainFrame
        # Does this even do anything?↓
        #self.mainFrm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrm.setStyleSheet("background-image: url('images/testBG.png');")

        self.closeBtn = QPushButton(self)
        self.closeBtn.setIcon(QIcon('images/test-removebg.png'))
        self.closeBtn.setIconSize(QtCore.QSize(20, 20))

        self.closeBtn.setStyleSheet("background-color: transparent;")
        self.closeBtn.setGeometry(195, -5, 50, 30)
        self.closeBtn.clicked.connect(sys.exit)
        
        self.cityText = str()
        
        self.cityEntry = QLineEdit(self, text=self.cityText)
        self.cityEntry.setPlaceholderText("Enter city name")
        # self.cityEntry.setStyleSheet("background-color: rgba(255, 255, 255, 60);")
        # self.cityEntry.setStyleSheet("border-radius: 1px;")
        # self.cityEntry.setStyleSheet("padding-left: 7px;")
        # self.cityEntry.setStyleSheet("background-color: red;")
        self.cityEntry.setGeometry(10, 15, 150, 30)
        self.cityEntry.setStyleSheet("background-color: rgba(255, 255, 255, 60); border-top-left-radius: 10px; border-bottom-left-radius: 10px; padding-left: 5px; color: white; font-family: Arial; font-size: 12px;")

        self.searchBtn = QPushButton(self)
        self.searchBtn.setIcon(QIcon('images/search-white-removebg.png'))
        self.searchBtn.setIconSize(QtCore.QSize(20, 20))
        self.searchBtn.setStyleSheet("background-color: rgba(255, 255, 255, 60); border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding-right: 5px;")
        self.searchBtn.setGeometry(160, 15, 24, 30)
        self.searchBtn.clicked.connect(self.search)
        # self.searchBtn.setStyleSheet("background-color: red;")
 
    
        self.locationLbl = QLabel(self, text='')
        self.locationLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 17px;")
        self.locationLbl.setGeometry(26, 45, 200, 30)

        self.tempLbl = QLabel(self, text='')
        self.tempLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 50px;")
        self.tempLbl.setGeometry(10, 80, 200, 50)

        self.image = QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setScaledContents(True)
        self.image.setGeometry(10, 200, 50, 50)



        self.weatherLbl = QLabel(self, text='')
        self.weatherLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 17px;")
        self.weatherLbl.setGeometry(10, 340, 200, 30)

        self.feelsLikeLbl = QLabel(self, text='')
        self.feelsLikeLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 17px;")
        self.feelsLikeLbl.setGeometry(10, 370, 200, 30)

        self.windLbl = QLabel(self, text='')
        self.windLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 17px;")
        self.windLbl.setGeometry(10, 400, 200, 30)

        self.dragBarLbl = QLabel(self)
        self.dragBarLbl.setStyleSheet("background-color: transparent;")
        self.dragBarLbl.setMaximumSize(QSize(200, 15))
        self.dragBarLbl.setMinimumSize(QSize(200, 15))

        self.locationIcon = QLabel(self)

        self.drag_start_pos = None

        self.timeLbl = QLabel(self, text='')
        self.timeLbl.setStyleSheet("color: white; font-family: Yu Gothic UI Light; font-size: 17px;")
        self.timeLbl.setGeometry(10, 170, 200, 30)

        
        # self.time.strftime('%H:%M')

    def get_weather(self, city):
        result = requests.get(url.format(city, api_key))
        # print(url.format(city, api_key))
        
        if result:
            json = result.json()
            # (City, country, temp_celsius, icon, weather)
            city = json['name']
            country = json['sys']['country']
            temp_kelvin = json['main']['temp']
            temp_celsius = temp_kelvin - 273.15
            feels_like = json['main']['feels_like'] - 273.15
            wind = json['wind']['speed']
            icon = json['weather'][0]['icon']
            weather = json['weather'][0]['description']
            longitude = json['coord']['lon']
            latitude = json['coord']['lat']


            final = (city, country, temp_celsius, feels_like, wind, icon, weather, longitude, latitude)
            return final
        else:
            print("Error while getting weather data")
            return None
# TODO: ADD IF STATEMENT TO SEE IF FEELS-LIKE IS THE SAME AS TEMP, IF NOT THEN DONT SHOW?
    def search(self):
        city = self.cityEntry.text()
        weather = self.get_weather(city)
        # if weather:
        #     location = weather[0] + ', ' + weather[1]
        #     self.locationLbl.setText(location)
        #     self.tempLbl.setText(str(weather[2]) + '°C')
        #     self.weatherLbl.setText(weather[6])
        #     self.feelsLikeLbl.setText(str(weather[3]) + '°C')
        #     self.windLbl.setText(str(weather[4]) + 'km/h')
        if weather:
            
            self.locationIcon.setPixmap(QPixmap('images/location_v2_16x.png'))
            self.locationIcon.setGeometry(10, 53, 16, 16)
            self.locationIcon.setScaledContents(True)
            self.locationIcon.setAlignment(QtCore.Qt.AlignCenter)
            self.locationIcon.setStyleSheet("background-color: transparent;")

            self.locationLbl.setText('{}, {}'.format(weather[0], weather[1]))
            
            pixmap = QPixmap('images/weather_icons_orig/{}.png'.format(weather[5]))  
            self.image.setPixmap(pixmap)

            self.tempLbl.setText('{:.0f}°'.format(weather[2]))
            
            self.feelsLikeLbl.setText('{:.0f}°'.format(weather[3]))
            
            self.windLbl.setText('{:.0f}km/h'.format(weather[4]))

            self.weatherLbl.setText(weather[6])

            self.time = TimezoneFinder().timezone_at(lng=weather[7], lat=weather[8])
            self.timeLbl.setText(self.time)
            # print(self.time)
            self.timezone = timezone(self.time)
            self.time = datetime.now(self.timezone)
            self.timeLbl.setText(self.time.strftime('%H:%M'))
            # print(self.time.strftime('%H:%M'))

        else:
            QMessageBox.critical(self, 'Error', "Cannot find city {}".format(city))

    
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            try:
                # Check if the mouse press position is within the label's boundaries
                if self.dragBarLbl.geometry().contains(event.pos()):
                    self.press_pos = event.globalPos()
                    self.move_pos = QPoint(0, 0)
            except Exception as error:
                return None

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            try:
                if self.dragBarLbl.geometry().contains(event.pos()):
                    self.move_pos = event.globalPos() - self.press_pos
                    self.move(self.pos() + self.move_pos)
                    self.press_pos = event.globalPos()
            except Exception as error:
                return None

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        x = ag.width() - widget.width() - 50
        y = 2 * ag.height() - sg.height() - widget.height() + 18
        self.move(x, y)

if __name__ == "__main__":
    # Create an application object
    app = QApplication(sys.argv)

    #app.setStyle('Fusion')

    # Create the Main Window object from FormWithTable Class and show it on the screen
    appWindow = mainWindow()
    appWindow.location_on_the_screen()
    appWindow.show()  # This can also be included in the FormWithTable class
    sys.exit(app.exec_())
        