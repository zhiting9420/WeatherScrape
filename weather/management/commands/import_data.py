from django.core.management.base import BaseCommand
from django.db import transaction
from weather.models import WeatherRecord
import csv
from datetime import datetime
import os


class Command(BaseCommand):
    help = '导入所有CVS文件'

    def add_arguments(self, parser):
        parser.add_argument('csv_folder', type=str, help='CSV文件所在文件夹的路径')

    def handle(self, *args, **options):
        csv_folder = options['csv_folder']
        all_weather_data = []

        for filename in os.listdir(csv_folder):
            if filename.endswith('.csv'):
                file_path = os.path.join(csv_folder, filename)
                all_weather_data.extend(self.read_csv(file_path))

        # 按日期对数据排序
        all_weather_data.sort(key=lambda x: x['date'])

        # 导入需要排序的数据
        self.import_data(all_weather_data)

        self.stdout.write(self.style.SUCCESS('成功导入所有天气数据!'))

    def read_csv(self, file_path):
        weather_data = []
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date = datetime.strptime(row['日期'], '%Y-%m-%d').date()
                max_temp = float(row['最高气温'].rstrip('℃'))
                min_temp = float(row['最低气温'].rstrip('℃'))
                wind_level = row['级别'].rstrip('级')

                weather_data.append({
                    'date': date,
                    'day_of_week': row['星期'],
                    'max_temperature': max_temp,
                    'min_temperature': min_temp,
                    'weather': row['天气'],
                    'wind_direction': row['风向'],
                    'wind_level': wind_level
                })
        return weather_data

    def import_data(self, weather_data):
        weather_records = []
        for data in weather_data:
            weather_record = WeatherRecord(**data)
            weather_records.append(weather_record)

        with transaction.atomic():
            WeatherRecord.objects.all().delete()  # 清理已经存在的数据
            WeatherRecord.objects.bulk_create(weather_records)

        self.stdout.write(self.style.SUCCESS(f'成功导入 {len(weather_records)} '))
