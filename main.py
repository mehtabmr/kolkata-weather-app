#!/usr/bin/env python3
"""
Kolkata Weather Android App
Built with Kivy - Cross-platform Python framework
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
import urllib.request
import json
from datetime import datetime


class WeatherData:
    """Handle weather API calls"""
    
    def __init__(self):
        self.city = "Kolkata"
        self.lat = 22.5726
        self.lon = 88.3639
        self.data = None
        
    def fetch(self):
        """Fetch weather from Open-Meteo"""
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,pressure_msl&timezone=Asia%2FKolkata"
            
            with urllib.request.urlopen(url, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                return self.parse(data)
        except Exception as e:
            return {"error": str(e)}
    
    def parse(self, data):
        """Parse API response"""
        current = data.get("current", {})
        return {
            "city": self.city,
            "time": datetime.now().strftime("%I:%M %p"),
            "date": datetime.now().strftime("%d %b %Y"),
            "temp": round(current.get("temperature_2m", 0), 1),
            "feels_like": round(current.get("apparent_temperature", 0), 1),
            "humidity": current.get("relative_humidity_2m", 0),
            "wind": round(current.get("wind_speed_10m", 0), 1),
            "rain": current.get("precipitation", 0),
            "pressure": current.get("pressure_msl", 0),
            "condition": self.get_condition(current.get("weather_code", 0)),
            "icon": self.get_icon(current.get("weather_code", 0))
        }
    
    def get_condition(self, code):
        conditions = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Rime Fog",
            51: "Drizzle",
            53: "Moderate Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Light Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            95: "Thunderstorm",
            96: "Thunderstorm with Hail",
            99: "Heavy Thunderstorm"
        }
        return conditions.get(code, "Unknown")
    
    def get_icon(self, code):
        """Return emoji based on weather code"""
        icons = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️",
            51: "🌦️", 53: "🌧️", 55: "🌧️",
            61: "🌧️", 63: "🌧️", 65: "🌧️",
            71: "🌨️", 73: "🌨️", 75: "❄️",
            95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        return icons.get(code, "🌡️")


class WeatherCard(BoxLayout):
    """Custom card widget for weather display"""
    
    def __init__(self, title, value, icon="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        
        # Background
        with self.canvas.before:
            Color(0.15, 0.2, 0.3, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Icon
        if icon:
            self.add_widget(Label(
                text=icon,
                font_size='40sp',
                size_hint_y=0.4,
                color=(1, 1, 1, 1)
            ))
        
        # Title
        self.add_widget(Label(
            text=title,
            font_size='14sp',
            color=(0.7, 0.8, 1, 1),
            size_hint_y=0.3
        ))
        
        # Value
        self.add_widget(Label(
            text=value,
            font_size='18sp',
            color=(1, 1, 1, 1),
            bold=True,
            size_hint_y=0.3
        ))
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class KolkataWeatherAppLayout(BoxLayout):
    """Main app layout"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        
        # Set mobile-friendly background
        Window.clearcolor = (0.1, 0.15, 0.25, 1)
        
        self.weather_data = WeatherData()
        
        self.build_ui()
        
        # Auto-refresh every 10 minutes
        Clock.schedule_interval(self.refresh_weather, 600)
    
    def build_ui(self):
        """Build the UI"""
        # Title
        title_label = Label(
            text='🌤️ Kolkata Weather',
            font_size='28sp',
            bold=True,
            color=(1, 0.8, 0.3, 1),
            size_hint_y=0.1
        )
        self.add_widget(title_label)
        
        # Last updated
        self.status_label = Label(
            text='Tap Refresh to get weather',
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.05
        )
        self.add_widget(self.status_label)
        
        # Main temperature display
        self.temp_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        self.temp_icon = Label(
            text='🌡️',
            font_size='60sp',
            size_hint_x=0.4
        )
        self.temp_value = Label(
            text='--°C',
            font_size='48sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_x=0.6
        )
        self.temp_layout.add_widget(self.temp_icon)
        self.temp_layout.add_widget(self.temp_value)
        self.add_widget(self.temp_layout)
        
        # Condition
        self.condition_label = Label(
            text='Loading...',
            font_size='22sp',
            color=(0.9, 0.9, 1, 1),
            size_hint_y=0.08
        )
        self.add_widget(self.condition_label)
        
        # Weather details grid
        details_scroll = ScrollView(size_hint_y=0.35)
        self.details_grid = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint_y=None
        )
        self.details_grid.bind(minimum_height=self.details_grid.setter('height'))
        
        # Create empty cards
        self.cards = {}
        for title, icon in [
            ("Feels Like", "🤒"),
            ("Humidity", "💧"),
            ("Wind Speed", "🌬️"),
            ("Pressure", "📊"),
            ("Rain", "🌧️"),
            ("Date", "📅")
        ]:
            card = WeatherCard(title, "--", icon, size_hint_y=None, height=120)
            self.cards[title] = card
            self.details_grid.add_widget(card)
        
        details_scroll.add_widget(self.details_grid)
        self.add_widget(details_scroll)
        
        # Refresh button
        self.refresh_btn = Button(
            text='🔄 Refresh Weather',
            font_size='18sp',
            size_hint_y=0.1,
            background_color=(0.2, 0.6, 0.9, 1),
            background_normal=''
        )
        self.refresh_btn.bind(on_press=self.on_refresh)
        self.add_widget(self.refresh_btn)
        
        # Initial load
        Clock.schedule_once(lambda dt: self.refresh_weather(), 0.5)
    
    def on_refresh(self, instance):
        """Handle refresh button"""
        self.refresh_btn.text = "⏳ Loading..."
        self.refresh_btn.disabled = True
        self.refresh_weather()
    
    def refresh_weather(self, *args):
        """Fetch and display weather"""
        # Run in separate thread to avoid blocking UI
        import threading
        thread = threading.Thread(target=self._fetch_weather)
        thread.daemon = True
        thread.start()
    
    def _fetch_weather(self):
        """Fetch weather in background"""
        data = self.weather_data.fetch()
        # Update UI from main thread
        Clock.schedule_once(lambda dt: self.update_ui(data), 0)
    
    def update_ui(self, data):
        """Update UI with weather data"""
        self.refresh_btn.text = "🔄 Refresh Weather"
        self.refresh_btn.disabled = False
        
        if "error" in data:
            self.condition_label.text = f"❌ Error: {data['error']}"
            return
        
        # Update main display
        self.temp_icon.text = data['icon']
        self.temp_value.text = f"{data['temp']}°C"
        self.condition_label.text = f"{data['condition']}"
        self.status_label.text = f"Last updated: {data['time']}"
        
        # Update cards
        self.cards["Feels Like"].children[0].text = f"{data['feels_like']}°C"
        self.cards["Humidity"].children[0].text = f"{data['humidity']}%"
        self.cards["Wind Speed"].children[0].text = f"{data['wind']} km/h"
        self.cards["Pressure"].children[0].text = f"{data['pressure']} hPa"
        self.cards["Rain"].children[0].text = f"{data['rain']} mm"
        self.cards["Date"].children[0].text = data['date']


class KolkataWeatherApp(App):
    """Main App Class"""
    
    def build(self):
        self.title = 'Kolkata Weather'
        return KolkataWeatherAppLayout()


if __name__ == '__main__':
    KolkataWeatherApp().run()
