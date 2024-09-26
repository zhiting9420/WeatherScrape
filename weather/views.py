from django.shortcuts import render, HttpResponse
from .scrape_weather_data import scrape_weather_data
from weather.models import WeatherRecord
from django.db.models import Avg, Max, Min
from collections import Counter
from datetime import datetime
from django.http import JsonResponse
import pandas as pd
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings


def index(request):
    return HttpResponse("请到/dashboard查看面板")


def update(request):
    return render(request, '../templates/update_form.html')


def weather_dashboard(request):
    # 从GET请求参数中获取month值，如果没有提供，则默认使用当前月份。
    selected_month = int(request.GET.get('month', datetime.now().month))

    # 从数据库中筛选出选定月份的天气数据
    weather_data = WeatherRecord.objects.filter(date__month=selected_month)

    # 计算统计数据
    stats = weather_data.aggregate(
        avg_max_temp=Avg('max_temperature'),
        avg_min_temp=Avg('min_temperature'),
        max_temperature=Max('max_temperature'),
        min_temperature=Min('min_temperature')
    )

    # 准备气温走势图数据
    dates = [data.date.strftime('%Y-%m-%d') for data in weather_data]
    max_temperatures = [data.max_temperature for data in weather_data]
    min_temperatures = [data.min_temperature for data in weather_data]

    # 准备天气统计数据
    weather_types = list(weather_data.values_list('weather', flat=True))
    weather_counter = Counter(weather_types)
    weather_types = list(weather_counter.keys())
    weather_counts = list(weather_counter.values())

    context = {
        'weather_data': weather_data,
        'avg_max_temp': stats['avg_max_temp'],
        'avg_min_temp': stats['avg_min_temp'],
        'max_temperature': stats['max_temperature'],
        'min_temperature': stats['min_temperature'],
        'dates': dates,
        'max_temperatures': max_temperatures,
        'min_temperatures': min_temperatures,
        'weather_types': weather_types,
        'weather_counts': weather_counts,
        'selected_month': selected_month,
    }

    return render(request, '../templates/dashboard.html', context)


@csrf_exempt
def update_weather_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            year = data.get('year')

            if not year:
                return JsonResponse({'status': 'error', 'message': '未提供年份'})

            # 调用爬虫函数获取最新数据
            scrape_weather_data(str(year))

            # 遍历所有生成的 CSV 文件并更新数据库
            # data_dir = '../weather_data'
            data_dir = settings.WEATHER_DATA_DIR

            for filename in os.listdir(data_dir):
                if filename.endswith('.csv'):
                    file_path = os.path.join(data_dir, filename)
                    df = pd.read_csv(file_path)

                    for _, row in df.iterrows():
                        date = datetime.strptime(row['日期'], '%Y-%m-%d').date()
                        WeatherRecord.objects.update_or_create(
                            date=date,
                            defaults={
                                'max_temperature': float(row['最高气温'].rstrip('℃')),
                                'min_temperature': float(row['最低气温'].rstrip('℃')),
                                'weather': row['天气'],
                                'wind_direction': row['风向'],
                                'wind_level': row['级别']
                            }
                        )

            return JsonResponse({'status': 'success', 'message': f'{year}年天气数据更新成功!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'更新数据时出错: {str(e)}'})
    return JsonResponse({'status': 'error', 'message': '无效的请求方法'})
