from django.apps import AppConfig
from django.conf import settings
import os


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        if os.environ.get('RUN_MAIN'):  # 防止在开发服务器中运行两次
            from . import scrape_weather_data
            year = input("请输入要爬取的年份：")
            scrape_weather_data.scrape_weather_data(year)
