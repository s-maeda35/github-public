import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import django
from dmd_gui.models import WeatherData0
from dmd_gui.models import WeatherData1
from dmd_gui.models import DemandData0
from datetime import datetime
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib
matplotlib.use('Agg') # Matplotlibのインタラクティブなバックエンドを無効にする

# メモ
#python manage.py makemigrations dmd_gui
#python manage.py migrate
    
def foecast_info_update1():
    """
    「forecast_all.html」の「九州の天気」の内容を更新する関数
    
    """
    # 設定情報
    load_url_9 = 'https://tenki.jp/forecast/9/'
    line_number = 20
    all_filename = 'C:\\Users\\frontier-Python\\Desktop\\dmd_app\\dmd_gui\\static\\dmd_gui\\html\\all_realtime.html'
    # 最新の天気予報情報を取得
    all9_html = requests.get(load_url_9)
    soup = BeautifulSoup(all9_html.content,'html.parser')
    all_forecast = soup.find(id='forecast-map-wrap').prettify()
    # HTMLファイルを読み込み、指定行に新しい内容を挿入
    with open(all_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 20行目以降を最新の天気予報情報で置き換える
    lines[line_number:] = [all_forecast + '\n']
    # 更新した内容でファイルを上書き保存
    with open(all_filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def foecast_info_update2():
    """
    「forecast_all.html」の「雨雲レーダー」の内容を更新する関数
    
    """
    # 設定情報
    load_url_radar = 'https://tenki.jp/radar/9/'
    radar_filename = 'C:\\Users\\frontier-Python\\Desktop\\dmd_app\\dmd_gui\\static\\dmd_gui\\html\\radar_realtime.html'
    # 最新の天気予報情報を取得
    radar_html = requests.get(load_url_radar)
    soup = BeautifulSoup(radar_html.content,'html.parser')
    radar = soup.find(class_='radar-top-tab-img-box')
    # 更新した内容でファイルを上書き保存
    with open(radar_filename, 'w', encoding='utf-8') as file:
        radar_text = radar.prettify() 
        file.write(radar_text)


def foecast_info_update3():
    """
    「forecast_details.html」の「1時間天気」の内容を更新する関数
    
    """
    # 設定情報
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
    # 最新の天気予報情報を取得
    for spotCounter in range(len(load_urls)):  #福岡～佐賀までループ
        for i in range(len(day_type)):  #当日～翌日でループ
            html = requests.get(load_urls[spotCounter])
            soup = BeautifulSoup(html.content,'html.parser')
            dayType = soup.find(id=day_type[i])
            #######################################################
            #画面で使用するHTMLファイルの作成
            filename = 'spot' + str(spotCounter) + 'day' + str(i)
            with open(f'C:\\Users\\frontier-Python\\Desktop\\dmd_app\\dmd_gui\\static\\dmd_gui\\html\\{filename}.html', 'w', encoding='utf-8') as file:
                dayType_text = dayType.prettify() 
                file.write(dayType_text)
            #######################################################
            for j in range(len(in_item)):  #気温、降水確率、降水量、湿度、風速を取得するためのループ
                day = dayType.find(class_= in_item[j]) 
                day_result = []
                day_result.append(i)
                day_result.append(load_urls_spotName[spotCounter])
                for element in day.find_all('td'):
                    day_result.append(element.text)  
                list_day.append(day_result)
    # DataFrameに加工
    df = pd.DataFrame(list_day,columns  
            = ["type","spot","plot_1","plot_2","plot_3","plot_4","plot_5","plot_6","plot_7","plot_8","plot_9","plot_10","plot_11","plot_12","plot_13","plot_14","plot_15","plot_16","plot_17","plot_18","plot_19","plot_20","plot_21","plot_22","plot_23","plot_24"],\
            index = ['fk_temperature', 'fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed','fk_temperature','fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed',\
                    'oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed','oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed',\
                    'mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed','mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed',\
                    'kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed','kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed',\
                    'km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed','km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed',\
                    'ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed','ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed',\
                    'sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed','sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed'])
    # Djangoの環境を設定
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_app.settings')
    django.setup()
    # DataFrameの各行をDjangoモデルのインスタンスに変換して保存
    df.replace('---', 99, inplace=True)
    for index, row in df.iterrows():
        if row['type'] == 0:
            data_instance0 = WeatherData0(
                index_name=index,
                type=row['type'],
                spot=row['spot'],
                plot_1=row['plot_1'],
                plot_2=row['plot_2'],
                plot_3=row['plot_3'],
                plot_4=row['plot_4'],
                plot_5=row['plot_5'],
                plot_6=row['plot_6'],
                plot_7=row['plot_7'],
                plot_8=row['plot_8'],
                plot_9=row['plot_9'],
                plot_10=row['plot_10'],
                plot_11=row['plot_11'],
                plot_12=row['plot_12'],
                plot_13=row['plot_13'],
                plot_14=row['plot_14'],
                plot_15=row['plot_15'],
                plot_16=row['plot_16'],
                plot_17=row['plot_17'],
                plot_18=row['plot_18'],
                plot_19=row['plot_19'],
                plot_20=row['plot_20'],
                plot_21=row['plot_21'],
                plot_22=row['plot_22'],
                plot_23=row['plot_23'],
                plot_24=row['plot_24']
            )
            data_instance0.save()
        else:
            data_instance1 = WeatherData1(
                index_name=index,
                type=row['type'],
                spot=row['spot'],
                plot_1=row['plot_1'],
                plot_2=row['plot_2'],
                plot_3=row['plot_3'],
                plot_4=row['plot_4'],
                plot_5=row['plot_5'],
                plot_6=row['plot_6'],
                plot_7=row['plot_7'],
                plot_8=row['plot_8'],
                plot_9=row['plot_9'],
                plot_10=row['plot_10'],
                plot_11=row['plot_11'],
                plot_12=row['plot_12'],
                plot_13=row['plot_13'],
                plot_14=row['plot_14'],
                plot_15=row['plot_15'],
                plot_16=row['plot_16'],
                plot_17=row['plot_17'],
                plot_18=row['plot_18'],
                plot_19=row['plot_19'],
                plot_20=row['plot_20'],
                plot_21=row['plot_21'],
                plot_22=row['plot_22'],
                plot_23=row['plot_23'],
                plot_24=row['plot_24']
            )
            data_instance1.save()


def demand_info_update1():    
    """
    「demand_info.html」の「現在需要/九電計画」の内容を更新する関数
    
    """
    # 設定情報
    today = datetime.now().strftime('%Y%m%d')  
    url = f'https://www.kyuden.co.jp//td_power_usages//csv//juyo-hourly-{today}.csv'
    filename = f'C:\\Users\\frontier-Python\\Desktop\\dmd_app\\98_new_demand_data\\juyo-hourly-{today}.csv'
    image_path = 'C:\\Users\\frontier-Python\\Desktop\\dmd_app\\dmd_gui\\static\\dmd_gui\\capture\\graph.png'
    # HTTP GETリクエストを送信してファイルを取得
    response = requests.get(url)
    # レスポンスが成功した場合
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        # CSVファイルの読み込み
        demand0_df = pd.read_csv(filename, encoding='shift_jis', skiprows=13, nrows=24)
        # カラム名を変更する辞書を定義
        new_column_names = {
        'DATE': 'date',
        'TIME': 'time',
        '当日実績(万kW)': 'ploperformancet',
        '予測値(万kW)': 'prediction',
        '使用率(%)': 'used',
        '予備率(%)': 'supply',
        '供給力想定値(万kW)': 'supply_prediction'
        }
        demand0_df = demand0_df.rename(columns=new_column_names)
        # DBへ保存
        for index, row in demand0_df.iterrows():
            data_instance2 = DemandData0(
                id=index,
                date=datetime.strptime(row['date'], "%Y/%m/%d").date(),
                time=row['time'],
                ploperformancet=row['ploperformancet'],
                prediction_q=row['prediction'],
                used=row['used'],
                supply=row['supply'],
                supply_prediction=row['supply_prediction']
                )
            data_instance2.save()
        data = DemandData0.objects.all()
        # 「需要実績」「Q_需要予測」「N_需要予測」の折れ線グラフを作成
        x_values = [row.id for row in data]
        ploperformancet_values = [row.ploperformancet for row in data]
        prediction_q_values = [row.prediction_q for row in data]
        prediction_n_values = [row.prediction_n for row in data]
        plt.figure(figsize=(15, 2.5))
        plt.plot(x_values, ploperformancet_values, marker='o', label='需要実績')
        plt.plot(x_values, prediction_q_values, marker='o', label='Q_需要予測')
        plt.plot(x_values, prediction_n_values, marker='o', label='N_需要予測')
        plt.xlabel('時')
        plt.ylabel('(MW)')
        plt.title('総需要')
        plt.grid(True)
        plt.legend()
        plt.savefig(image_path)
        plt.close()
    else:
        print("ファイルのダウンロードに失敗しました。ステータスコード:", response.status_code)