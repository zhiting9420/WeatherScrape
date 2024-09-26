import requests
from lxml import etree
import pandas as pd


def scrape_weather_data(year):
    month = str()

    for i in range(1, 13):
        if i < 10:
            month = '0' + str(i)
        else:
            month = str(i)

        url = f"https://lishi.tianqi.com/changde/{year}{month}.html"

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }

        response = requests.get(url, headers=header).text

        weather_info = {
            '日期': [],
            '星期': [],
            '最高气温': [],
            '最低气温': [],
            '天气': [],
            '风向': [],
            '级别': [],
        }

        root = etree.HTML(response)
        uls = root.xpath('//ul[@class="thrui"]')
        for ul in uls:
            lis = ul.xpath('./li')
            s = ''
            for li in lis:


                # 确保 split_text 至少有 7 个元素，不足的部分用 '' 填充
                text = li.xpath('normalize-space(string(.))')
                split_text = text.split()
                split_text.extend([''] * (7 - len(split_text)))
                weather_info['日期'].append(split_text[0])
                weather_info['星期'].append(split_text[1])
                weather_info['最高气温'].append(split_text[2])
                weather_info['最低气温'].append(split_text[3])
                weather_info['天气'].append(split_text[4])
                weather_info['风向'].append(split_text[5])
                weather_info['级别'].append(split_text[6])

            pd.DataFrame(weather_info).to_csv(f'./weather_data/weather{month}.csv', index=False)

        print(f'{month}月爬取完毕')
        month += str(1)


if __name__ == "__main__":
    year = input("请输入年份：")
    scrape_weather_data(year)
