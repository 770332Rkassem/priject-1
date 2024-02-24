import requests
from bs4 import BeautifulSoup
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (350, 600)

kv = '''
MDFloatLayout:
    md_bg_color: 1,1,1,1
    Image:
        source: "icons8-location-48.png"
        size_hint: .18, .18
        pos_hint: {"center_x": .5, "center_y": .95}
    MDLabel:
        id: location
        text: "" 
        font_name: "Poppins-SemiBold.ttf"
        font_size: "21sp"
        color: 0, 0, 0, 1  
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .876}
    Image:
        id: weather_image
        source: ""
        pos_hint: {"center_x": .5, "center_y": .77}
    MDLabel:
        id: degree
        text: ""
        markup: True
        font_name: "Poppins-SemiBold.ttf"
        font_size: "60sp"
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .62}
    MDLabel:
        id: weather 
        text: ""
        font_name: "Poppins-Regular.ttf"
        font_size: "20sp"
        halign: "center"
        pos_hint: {"center_x": .5, "center_y": .54}
    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .4}
        size_hint: .22, .1
        Image:
            source: "icons8-humidity-48.png"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: humidity
            text: ""
            font_size: "18sp"
            font_name: "Poppins-SemiBold.ttf"
            pos_hint: {"center_x": 1, "center_y": .7}
        MDLabel:
            text: "Humidity"
            font_size: "14sp"
            font_name: "Poppins-Regular.ttf"
            pos_hint: {"center_x": 1, "center_y": .3}
            
    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .4}
        size_hint: .22, .1
        Image:
            source: "icons8-wind-speed-48.png"
            pos_hint: {"center_x": .1, "center_y": .5}
        MDLabel:
            id: wind_speed
            text: ""
            font_size: "18sp"
            font_name: "Poppins-SemiBold.ttf"
            pos_hint: {"center_x": 1.1, "center_y": .7}
        MDLabel:
            text: "Wind"
            font_size: "16sp"
            font_name: "Poppins-Regular.ttf"
            pos_hint: {"center_x": 1.1, "center_y": .3}
    MDFloatLayout:
        size_hint_y : .3
        canvas:
            Color:
                rgb:rgba(148, 117, 255, 255)
            RoundedRectangle:
                size : self.size
                pos: self.pos
                radius:[10,10,0,0]
        MDFloatLayout:
            pos_hint: {"center_x": .5, "center_y": .71}
            size_hint : .9, .32
            canvas:
                Color:
                    rgb:rgba(131, 69, 255, 255)
                RoundedRectangle:
                    size : self.size
                    pos: self.pos
                    radius:[6]
            TextInput
                id: city_name
                hint_text: "Enter City Name"
                size_hint : 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                font_name: "Poppins-SemiBold.ttf"
                font_size: "20sp"
                hint_text_color: 1,1,1,1
                foreground_color: 1,1,1,1
                background_color: 1,1,1,0
                padding:15
                cursor_color: 1,1,1,1
                cursor_width: "2sp" 
                multiline: False
                
        Button:
            text:"Get Weather"
            size_hint: .9,.32
            pos_hint: {"center_x": .5, "center_y": .29}
            font_size: "20sp"
            font_name: "Poppins-SemiBold.ttf"
            background_color: 1,1,1,0
            color: rgba(148, 117, 255, 255)
            on_release: app.search_weather()
            canvas.before:
                Color:
                    rgb:1,1,1,1
                RoundedRectangle:
                    size : self.size
                    pos: self.pos
                    radius:[6]
            
            

                                
                
'''


class WeatherApp(MDApp):
    api_key = "76ad75fc386d40343bbae643d5bab601"
    def on_start(self):
        try:
            soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text, "html.parser" )
            temp = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
            location = ''.join(filter(lambda item: not item.isdigit(), temp.text)).split("،")
            self.get_weather(location[1].strip())

        except ConnectionError:
            print("No Internet Connection")

    def build(self):
        return Builder.load_string(kv)

    def get_weather(self,city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}"
            response = requests.get(url)
            x = response.json()
            if x["cod"] != '404':
                temperature = round(x["main"]["temp"] -273.15)
                humidity = x["main"]["humidity"]
                weather = x["weather"][0]["main"]
                id = str(x["weather"][0]["id"])
                wind_speed = round(x["wind"]["speed"]*18/5)
                location = x["name"] + ", " + x["sys"]["country"]
                self.root.ids.degree.text = f"[b]{temperature}[/b][sup]°[/sup]"
                self.root.ids.humidity.text = f"{humidity}%"
                self.root.ids.weather.text = str(weather)
                self.root.ids.wind_speed.text = f"{wind_speed} km/h"
                self.root.ids.location.text = location
                if id == "800":
                    self.root.ids.weather_image.source = "icons8-sun-96.png"
                elif "200" <= id <= "232":
                    self.root.ids.weather_image.source = "icons8-storm-96.png"
                elif "300" <= id <= "321" and "500" <= id <= "531":
                    self.root.ids.weather_image.source = "icons8-rain-96.png"
                elif "600" <= id <= "622":
                    self.root.ids.weather_image.source = "icons8-snow-96.png"
                elif "701" <= id <= "781":
                    self.root.ids.weather_image.source = "icons8-haze-96.png"
                elif "801" <= id <= "804":
                    self.root.ids.weather_image.source = "icons8-cloud-96.png"


            else:
                print("City Not Found")
        except requests.ConnectionError:
            print("No Internet Connection !")

    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != "":
            self.get_weather(city_name)




if __name__ == '__main__':
    WeatherApp().run()
