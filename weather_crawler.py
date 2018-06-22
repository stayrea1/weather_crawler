# -*- coding: utf-8 -*-
# @Time    : 18/6/22 下午1:01
# @Author  : SunXie
# @Email   : turbob00st.sr@gmail.com
# @Software: PyCharm Community Edition

from bs4 import BeautifulSoup

import requests


class Weather_crawler:
    ##存储城市的url信息
    city_url = []
    ##存储城市及其历史的月份
    month_info = []
    ##存储历史天气
    history_weather = []

    ## 获取同地级市的所有城市信息
    def get_city_list(self,city_index_page):
        web_data = requests.get(city_index_page)
        soup = BeautifulSoup(web_data.text,'lxml')

        city = soup.select('div.racitybox')[0].select('ul.raweather760 a')

        for index in city:
            if index.select('h5') != []:
                city_info = {

                    'city': index.select('h5')[0].text,
                    'city_suf':index.get('href')
                }

                self.city_url.append(city_info)



    ## 获取历史数据的链接
    def get_history_pages(self):
        for i in self.city_url:
            page = 'http://lishi.tianqi.com{}index.html'.format(i.get('city_suf'))
            city = i.get('city')
            web_data = requests.get(page)
            soup = BeautifulSoup(web_data.text,'lxml')
            history_month = soup.select('div.tqtongji1 a')
            for i in history_month:
                month_info = {
                    'city' : city,
                    'month' : i.text,
                    'page' : i.get('href')
                }

                self.month_info.append(month_info)

    
    # 获取天气
    def get_weather(self):
        for i in self.month_info:
            web_data = requests.get(i.get('page'))
            city = i.get('city')
            print(city)
            soup = BeautifulSoup(web_data.text,'lxml')
            weather = soup.select('div.tqtongji2 li')
            for i in range(6,len(weather)-6,6):
                weather_info = {
                    'city': city,#城市
                    'date': weather[i].text,#日期
                    'max_temp':weather[i+1].text,#最高温
                    'min_temp': weather[i+2].text,#最低温
                    'weather': weather[i+3].text,#天气情况
                    'wind_direction':weather[i+4].text.strip('级'),#风向
                    'wind_intensity':weather[i+5].text #风力
                }

                self.history_weather.append(weather_info)





if __name__ == '__main__':


    url = 'http://wwww.tianqi.com/hangzhou' ##要爬取的县市url
    weather = Weather_crawler()
    weather.get_city_list(url)
    weather.get_history_pages()
    weather.get_weather()


