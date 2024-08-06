import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

def foecast_info_update1():
    """
    foecast_info_htmlの「九州の天気」の内容を更新する関数
    
    """
    load_url_9 = 'https://tenki.jp/forecast/9/'
    line_number = 20
    all_filename = 'C:\\xampp\\htdocs\\last_product_20240622\\all_realtime.html'
    
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
    
#雨雲レーダーを取得
def foecast_info_update2():
    load_url_radar = 'https://tenki.jp/radar/9/'
    radar_html = requests.get(load_url_radar)
    soup = BeautifulSoup(radar_html.content,'html.parser')
    radar = soup.find(class_='radar-top-tab-img-box')
    radar_filename = 'radar_realtime'
    with open(f'C:\\xampp\\htdocs\\last_product_20240622\\{radar_filename}.html', 'w', encoding='utf-8') as file:
        radar_text = radar.prettify() 
        file.write(radar_text)

def foecast_info_update3():
    # MariaDBの接続情報
    db_user = 'root'
    db_password = ''
    db_host = 'localhost' 
    db_name = 'dcs'

    # SQLAlchemyエンジンの作成
    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    #データ取得元の情報
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
            #######################################################
            #画面で使用するHTMLファイルの作成
            filename = 'spot' + str(spotCounter) + 'day' + str(i)
            with open(f'C:\\xampp\\htdocs\\last_product_20240622\\{filename}.html', 'w', encoding='utf-8') as file:
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
    df = pd.DataFrame(list_day,columns  #DataFrameに加工
            = ["type","spot","plot_1","plot_2","plot_3","plot_4","plot_5","plot_6","plot_7","plot_8","plot_9","plot_10","plot_11","plot_12","plot_13","plot_14","plot_15","plot_16","plot_17","plot_18","plot_19","plot_20","plot_21","plot_22","plot_23","plot_24"],\
            index = ['fk_temperature', 'fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed','fk_temperature','fk_prob-precip', 'fk_precipitation', 'fk_humidity', 'fk_wind-speed',\
                    'oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed','oo_temperature','oo_prob-precip', 'oo_precipitation', 'oo_humidity', 'oo_wind-speed',\
                    'mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed','mz_temperature','mz_prob-precip', 'mz_precipitation', 'mz_humidity', 'mz_wind-speed',\
                    'kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed','kg_temperature','kg_prob-precip', 'kg_precipitation', 'kg_humidity', 'kg_wind-speed',\
                    'km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed','km_temperature','km_prob-precip', 'km_precipitation', 'km_humidity', 'km_wind-speed',\
                    'ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed','ng_temperature','ng_prob-precip', 'ng_precipitation', 'ng_humidity', 'ng_wind-speed',\
                    'sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed','sg_temperature','sg_prob-precip', 'sg_precipitation', 'sg_humidity', 'sg_wind-speed'])

    # MariaDBにデータを保存
    df.to_sql('forecast9', engine, if_exists='replace')

# コマンドライン引数から引数を受け取る
# arg_from_php = sys.argv[1]
arg_from_php = '1'

# 引数に応じた処理
if arg_from_php == '1':
    foecast_info_update1()
elif arg_from_php == 2:
    foecast_info_update2()
elif arg_from_php == 3:
    foecast_info_update3()
else:
    print("不明な引数です")

