from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import requests
import datetime

API_KEY =

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Forecast")
    
        vertical = QVBoxLayout()
        horizontal = QHBoxLayout()
        horizontal1 = QHBoxLayout()
        horizontal2 = QHBoxLayout()
        horizontal3 = QHBoxLayout()
        
        toolbar = QToolBar("Menu")
        self.addToolBar(toolbar)
        manual_button = QAction("Manual", self)
        manual_button.triggered.connect(self.clicked_manual)
        toolbar.addAction(manual_button)
        
        self.city = QLabel()
        self.city.setText("City :")
        self.city_name = QLineEdit()
        
        #Create Pushbutton instance for Enter button
        self.enter_button = QPushButton("Enter")
        self.enter_button.clicked.connect(self.set_info)
        
        #Create QLabel instance for each elements 
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter)
        self.temperature = QLabel()
        self.temperature.setAlignment(Qt.AlignCenter)
        self.feel_like = QLabel()
        self.min_temp = QLabel()
        self.max_temp = QLabel()
        self.description = QLabel()
        self.sunrise = QLabel()
        self.sunset = QLabel()
        
        #add Widget to layout
        horizontal.addWidget(self.city)
        horizontal.addWidget(self.city_name)
        horizontal.addWidget(self.enter_button)
        horizontal1.addWidget(self.feel_like)
        horizontal1.addWidget(self.description)
        horizontal2.addWidget(self.min_temp)
        horizontal2.addWidget(self.max_temp)
        horizontal3.addWidget(self.sunrise)
        horizontal3.addWidget(self.sunset)
        
        #Add horizontal to vertical layout
        vertical.addLayout(horizontal)
        vertical.addWidget(self.icon)
        vertical.addWidget(self.temperature)
        vertical.addLayout(horizontal1) 
        vertical.addLayout(horizontal2)
        vertical.addLayout(horizontal3)
        
        #Set layout in QWidget
        layout = QWidget()
        layout.setLayout(vertical)
        self.setCentralWidget(layout)

        
    def get_city(self):
        """
            for get_city
            
            :param self: Description
            :raise  ValueError : if no city_name or city name not match with data
            :return : A String of city_name
            :rtype : Str
        """

        try:
            city_name = self.city_name.text()
        except ValueError:
            sys.exit("Invalid City Name")
        return city_name
    
    def call_geo(self, city):
        """
            Docstring for call_info
            
            :param city: City Name
            :raise: ValueError :Not found city match data
            :return: Json data lat and lon
        """
        
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={API_KEY}"
        try: 
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200 :
                data = response.json()
                lat = data[0]['lat']
                lon = data[0]['lon']
        except requests.exceptions.ConnectionError :
            print(f"Can't retrieved weather data")
        return lat, lon
        
        
    def call_info(self, lat, lon):
        """
        Docstring for call_info
        
            :param self: Description
            :param lat: latitude of city return from call_geo
            :param lon: longitude of city return from call_geo
            :return : json dataset of weather forecast
            :raise HTTPError: if return not code 200
        """
        
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
        try :
            response = requests.get(url)
            response.raise_for_status 
            if response.status_code == 200 :
                data = response.json()
        except requests.exceptions.ConnectionError :
            print(f"Can't retrieved weather data")
            
        return data
    
    def clicked_manual(self):
        text = """
            Weather Forecast Application
            - Go to www.openweather.com 
            - Register account 
            - Get API_KEY 
            - Set API_KEY AT the top of file:"App.py"
            - Enter City Name to text field
            - Clicked Enter Button
            - Program will requests data from API (openweather api) and show data in Mainwindow of application
            
        """
        QMessageBox.warning(self, "Manual(How to Use)", text)
    
    def set_info(self):
        """
            Docstring for set_info

            :param : No param
            :return : No return type
            :description: Modify instance QLabel of each elements with .setText and for icon using 
                          QPixmap by using data from return of self.call_info and extract info from json data
        """
        city = self.get_city().title().strip()
        lat, lon = self.call_geo(city)
        info = self.call_info(lat, lon)
        image = requests.get(f"https://openweathermap.org/img/wn/{info['current']['weather'][0]['icon']}@2x.png")
        image_byte = QByteArray(image.content)
        pixmap = QPixmap()
        pixmap.loadFromData(image_byte)
        self.icon.setPixmap(pixmap)
        self.temperature.setText(f"Temperature: {info['current']['temp']} °C")
        self.feel_like.setText(f"Feellike : {info['current']['feels_like']} °C")
        self.description.setText(f"Description: {info['current']['weather'][0]['description']}")
        self.min_temp.setText(f"Lowest Temperature : {info['daily'][0]['temp']['min']} °C")
        self.max_temp.setText(f"Highest Temperature : {info['daily'][0]['temp']['max']} °C")
         # Change time unix to time
        sunrise_time = datetime.datetime.fromtimestamp(info['current']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(info['current']['sunset'])
        self.sunrise.setText(f"Sunrise Time : {sunrise_time}")
        self.sunset.setText(f"Sunset TIme : {sunset_time}")
        # If have special condition or weather condition alerts will show as pop-up 
        if info.get('alert'):
            alert = info['alerts'][0]
            QMessageBox.warning(
                self,
                "Special Condition Alert",
                (f"Event : {alert['event'].title()}\n"
                f"Sender : {alert['sender_name']}\n"
                f"Detail : {alert['description']}")
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
