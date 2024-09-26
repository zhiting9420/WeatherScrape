from django.db import models


class WeatherRecord(models.Model):
    date = models.DateField(verbose_name="日期")
    day_of_week = models.CharField(max_length=10, verbose_name="星期")
    max_temperature = models.FloatField(verbose_name="最高气温")
    min_temperature = models.FloatField(verbose_name="最低气温")
    weather = models.CharField(max_length=50, verbose_name="天气")
    wind_direction = models.CharField(max_length=50, verbose_name="风向")
    wind_level = models.CharField(max_length=20, verbose_name="级别")

    def __str__(self):
        return f"{self.date} - {self.weather}"

    class Meta:
        verbose_name = "天气记录"
        verbose_name_plural = "天气记录"
        ordering = ['date']
