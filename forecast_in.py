import requests
from bs4 import BeautifulSoup
import pandas as pd

#九州における主要都市の当日と翌日の気象情報を取得する関数
def foecast_info():
    load_urls=['https://tenki.jp/forecast/9/43/8210/40130/1hour.html',\
                'https://tenki.jp/forecast/9/47/8310/44201/1hour.html',\
                'https://tenki.jp/forecast/9/48/8710/45201/1hour.html',\
                'https://tenki.jp/forecast/9/49/8810/46201/1hour.html',\
                'https://tenki.jp/forecast/9/46/8610/43100/1hour.html',\
                'https://tenki.jp/forecast/9/45/8410/42201/1hour.html',\
                'https://tenki.jp/forecast/9/44/8510/41201/1hour.html']
    load_urls_spotName=['福岡市','大分市','宮崎市','鹿児島市','熊本市','長崎市','佐賀市']
    day_type=['forecast-point-1h-today', 'forecast-point-1h-tomorrow'] 
    in_item=['temperature', 'prob-precip', 'precipitation', 'humidity', 'wind-speed']
    list_day=[]
    for spotCounter in range(len(load_urls)):  #福岡～佐賀までループ
        for i in range(len(day_type)):  #当日～翌日でループ
            html = requests.get(load_urls[spotCounter])
            soup = BeautifulSoup(html.content,'html.parser')
            dayType = soup.find(id=day_type[i])
            for j in range(len(in_item)):  #気温、降水確率、降水量、湿度、風速を取得するためのループ
                day = dayType.find(class_= in_item[j]) 
                day_result = []
                day_result.append(i)
                day_result.append(load_urls_spotName[spotCounter])
                for element in day.find_all('td'):
                    day_result.append(element.text)  
                list_day.append(day_result)
    df = pd.DataFrame(list_day,columns  #DataFrameに加工
            = ["type","spot","1時","2時","3時","4時","5時","6時","7時","8時","9時","10時","11時","12時","13時","14時","15時","16時","17時","18時","19時","20時","21時","22時","23時","24時"],\
            index = ['fk_temperature', 'fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed','fk_temperature','fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed',\
                    'oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed','oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed',\
                    'mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed','mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed',\
                    'kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed','kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed',\
                    'km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed','km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed',\
                    'ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed','ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed',\
                    'sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed','sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed'])
    return df
