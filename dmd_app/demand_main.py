from demand_cal import demandCal
from datetime import datetime, timedelta
import os
import django


def get_times():
    """
    0時から23時までの1時間毎のデータを取得する関数
    
    """
    # 基準時間を設定
    start_time = datetime.strptime('00:00:00', '%H:%M:%S')
    # 終了時間を設定
    end_time = datetime.strptime('23:00:00', '%H:%M:%S')
    # 1時間ごとの時間を格納するリスト
    get_times = []
    # 現在の時間を基準時間に設定 ※拡張用(現状は'00:00:00')
    current_time = start_time
    # 終了時間に達するまでループ
    while current_time <= end_time:
        get_times.append(current_time.strftime('%H:%M:%S'))
        current_time += timedelta(hours=1)
    return get_times


def get_daytype():
    """
    現在の日時を基に「daytype」を作成する関数
    
    """
    # 現在の日付を取得
    now = datetime.now()
    # 曜日を取得 (0=月曜日, 1=火曜日, ..., 6=日曜日)
    weekday = now.weekday()
    # 曜日をカスタムの範囲に変換 (日曜日=1, ..., 土曜日=7)
    dayType = (weekday + 1) % 7 + 1
    return dayType


def get_forecast():
    """
    DBから気温(1h)を取得する関数
    
    """
    def get_forecast_as_list(forecasts):
        """
        DBから気温(1h)を取得するためのリストを作成する関数
        
        """
        result_list = []
        # 各レコードのフィールドの値をリストに格納
        for forecast in forecasts:
            record = {
                'index_name': forecast.index_name,
                'plot_1': forecast.plot_1,
                'plot_2': forecast.plot_2,
                'plot_3': forecast.plot_3,
                'plot_4': forecast.plot_4,
                'plot_5': forecast.plot_5,
                'plot_6': forecast.plot_6,
                'plot_7': forecast.plot_7,
                'plot_8': forecast.plot_8,
                'plot_9': forecast.plot_9,
                'plot_10': forecast.plot_10,
                'plot_11': forecast.plot_11,
                'plot_12': forecast.plot_12,
                'plot_13': forecast.plot_13,
                'plot_14': forecast.plot_14,
                'plot_15': forecast.plot_15,
                'plot_16': forecast.plot_16,
                'plot_17': forecast.plot_17,
                'plot_18': forecast.plot_18,
                'plot_19': forecast.plot_19,
                'plot_20': forecast.plot_20,
                'plot_21': forecast.plot_21,
                'plot_22': forecast.plot_22,
                'plot_23': forecast.plot_23,
                'plot_24': forecast.plot_24,
            }
            result_list.append(record)
        return result_list

    # Django設定のインポートと設定
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_app.settings')
    django.setup()
    from dmd_gui.models import WeatherData0
    fk_forecasts = WeatherData0.objects.filter(index_name='fk_temperature')
    kg_forecasts = WeatherData0.objects.filter(index_name='kg_temperature')
    km_forecasts = WeatherData0.objects.filter(index_name='km_temperature')
    # 条件に一致するすべてのレコードを取得
    fk_result_list = get_forecast_as_list(fk_forecasts)
    kg_result_list = get_forecast_as_list(kg_forecasts)
    km_result_list = get_forecast_as_list(km_forecasts)
    # 「result_list」に当日の気象情報を格納
    result_list = []
    result_list.append(fk_result_list)
    result_list.append(kg_result_list)
    result_list.append(km_result_list)
    return result_list

# 需要比率（2023年11月）政府統計より
# グループ1：福岡：37％、佐賀：8％
group1_demand_ratio = ((38 + 8) / 100)
# グループ2：鹿児島：12％、宮崎：8％
group2_demand_ratio = ((12 + 8) / 100)
# グループ3：熊本：14％、長崎：10％、大分：10％
group3_demand_ratio = ((14 + 10 + 10) / 100)

# 設定
times = get_times()
dayType = get_daytype()
all_tmp = get_forecast()
fk_fingers = 0
kg_fingers = 0
km_fingers = 0
fk_spot = 0
kg_spot = 1
km_spot = 2
fk_humidity = 0
kg_humidity = 0
km_humidity = 0
plot_demand_list = []

# メイン処理(当日の0時～23時の需要予測値を計算)
for plot in range(24):
    time = times[plot]
    # 「fk_spot=0(福岡)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
    fk_dc = demandCal(time,dayType,fk_fingers,all_tmp[0][0][f'plot_{plot + 1}'],fk_spot,fk_humidity)
    fk_demand = fk_dc.demand_select()
    fk_demand = fk_demand * group1_demand_ratio
    # 「kg_spot=1(鹿児島)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
    kg_dc = demandCal(time,dayType,kg_fingers,all_tmp[1][0][f'plot_{plot + 1}'],kg_spot,kg_humidity)
    kg_demnd = kg_dc.demand_select()
    kg_demnd = kg_demnd * group2_demand_ratio
    # 「km_spot=2(熊本)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
    km_dc = demandCal(time,dayType,km_fingers,all_tmp[2][0][f'plot_{plot + 1}'],km_spot,km_humidity)
    km_demand = km_dc.demand_select()
    km_demand = km_demand * group3_demand_ratio
    # 九州域内の需要予測値を算出し、小数点第一位に丸め、リストに格納
    plot_demand = fk_demand + kg_demnd + km_demand
    plot_demand = round(plot_demand, 1)
    plot_demand_list.append(plot_demand)
    
    # デバッグ用
    print(plot_demand)

from dmd_gui.models import DemandData0
# DBに保存
for index, value in enumerate(plot_demand_list):
    record = DemandData0.objects.get(id=index)  
    record.prediction_n = value
    record.save()