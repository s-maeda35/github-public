from demand_cal import demandCal
from datetime import datetime, timedelta
import os
import django
from workalendar.asia import Japan
import pandas as pd


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
    dayType = now.weekday()
    return dayType


def get_forecast():
    """
    DBから気温(1h)を取得する関数
    
    """
    def get_forecast_as_list(forecasts):
        """
        DBから気温(1h)を取得するための取得リストを作成する関数
        
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


def dayTypeSelection1(dayType):
    """
    対象日が「祝日」OR「それ以外」を判定し、「祝日」OR「それ以外」のデータリストを作成する関数
    
    """
    # 設定情報
    perform_in = pd.read_csv('perform_in.csv')
    year_list = [2020,2021,2022,2023,2024]
    cal = Japan()
    check_flag = False
    # 現在の日付を取得。"YYYY-MM-DD" 形式でフォーマット
    current_date = datetime.now()
    check_date_str = current_date.strftime("%Y-%m-%d")
    check_date = datetime.strptime(check_date_str, "%Y-%m-%d").date()
    # CSVファイルから読み込んだデータを加工
    perform_in_holiday_list = perform_in.drop(perform_in.index, axis=0)
    perform_in['date'] = pd.to_datetime(perform_in['date']).dt.date
    # 対象データリストの作成
    for year in year_list:
        holidays_tuple = cal.holidays(year)
        for holiday in holidays_tuple:
            holiday_list = list(holiday)
            if check_date == holiday_list[0]:
                if dayType == 5 or dayType == 6:
                    continue
                else:
                    perform_in = perform_in[perform_in["date"] == holiday_list[0]] 
                    check_flag = True
                    break
            perform_in_holiday = perform_in[perform_in["date"] == holiday_list[0]]
            perform_in_holiday_list = pd.concat([perform_in_holiday_list, perform_in_holiday], ignore_index=True)
    else:
        # 対象日が祝日の場合には、祝日のデータを抽出する。対象日が祝日でない場合には、祝日以外のデータを抽出する。
        if check_flag:
            perform_in = perform_in_holiday_list
        else:
            perform_in = pd.merge(perform_in, perform_in_holiday_list, indicator=True, how='outer').query('_merge == "left_only"').drop(columns=['_merge'])
    return perform_in


def get_demand():
    """
    DBから0時時点の需要実績を取得する関数
    """
    # Django設定のインポートと設定
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmd_app.settings')
    django.setup()
    from dmd_gui.models import DemandData0

    # idが0のレコードを取得
    try:
        demand = DemandData0.objects.get(id=0)  # idが0のレコードを取得
        ploperformancet_data = demand.ploperformancet   # 正しいフィールド名に変更
        return ploperformancet_data
    except DemandData0.DoesNotExist:
        return None  # レコードが存在しない場合はNoneを返す


def d_main():
    # 設定情報
    group1_demand_ratio = ((38 + 8) / 100)  # グループ1：福岡：37％、佐賀：8％(需要比率（2023年11月）政府統計より)
    group2_demand_ratio = ((12 + 8) / 100)  # グループ2：鹿児島：12％、宮崎：8％(需要比率（2023年11月）政府統計より)
    group3_demand_ratio = ((14 + 10 + 10) / 100)  # グループ3：熊本：14％、長崎：10％、大分：10％(需要比率（2023年11月）政府統計より)
    times = get_times()
    dayType = get_daytype()
    all_tmp = get_forecast()
    plot_demand_list = []
    perform_in = dayTypeSelection1(dayType)
    ploperformancet_data = get_demand()
    time_Correction = 0
    
    # メイン処理(当日の0時～23時の需要予測値を計算)
    for plot in range(24):
        time = times[plot]
        # 「fk_spot=0(福岡)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
        fk_dc = demandCal(time, dayType, all_tmp[0][0][f'plot_{plot + 1}'], 0, perform_in)
        fk_demand = fk_dc.demand_select()
        fk_demand = fk_demand * group1_demand_ratio
        # 「kg_spot=1(鹿児島)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
        kg_dc = demandCal(time, dayType, all_tmp[1][0][f'plot_{plot + 1}'], 1, perform_in)
        kg_demnd = kg_dc.demand_select()
        kg_demnd = kg_demnd * group2_demand_ratio
        # 「km_spot=2(熊本)」のインスタンスを作成し、需要比率を加味して需要予測値を算出
        km_dc = demandCal(time, dayType, all_tmp[2][0][f'plot_{plot + 1}'], 2, perform_in)
        km_demand = km_dc.demand_select()
        km_demand = km_demand * group3_demand_ratio
        # spot1~3を合計
        plot_demand = fk_demand + kg_demnd + km_demand
        # 0時時点の需要の差分を基に補正比率を算出
        if time == '00:00:00':
            time_Correction = ploperformancet_data / plot_demand
        plot_demand = plot_demand * time_Correction
        # 九州域内の需要予測値を算出し、小数点第一位に丸め、リストに格納
        plot_demand = round(plot_demand, 1)
        plot_demand_list.append(plot_demand)

    # DBに保存
    from dmd_gui.models import DemandData0
    for index, value in enumerate(plot_demand_list):
        record = DemandData0.objects.get(id=index)  
        record.prediction_n = value
        record.save()