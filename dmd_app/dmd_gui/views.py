from django.shortcuts import render
from data_input import foecast_info_update1, foecast_info_update2, foecast_info_update3, demand_info_update1
from .models import DemandData0
from django.utils import timezone
from django.views.decorators.cache import never_cache

@never_cache #HTTP応答のキャッシュを無効

def index(request):
    return render(request, 'dmd_gui/index.html')

def forecast_all(request):
    if request.method == 'POST':
        foecast_info_update1()
        foecast_info_update2()
        foecast_info_update3()
        demand_info_update1()
    # タイムスタンプを生成
    timestamp = timezone.now().timestamp()
    # テンプレートにデータを渡してレンダリング
    response = render(request, 'dmd_gui/forecast_all.html', {'timestamp': timestamp})
    return response

def forecast_details(request):
    if request.method == 'POST':
        foecast_info_update1()
        foecast_info_update2()
        foecast_info_update3()
        demand_info_update1()
    # タイムスタンプを生成
    timestamp = timezone.now().timestamp()
    # テンプレートにデータを渡してレンダリング
    response = render(request, 'dmd_gui/forecast_details.html', {'timestamp': timestamp})
    return response

def demand_info(request):
    if request.method == 'POST':
        foecast_info_update1()
        foecast_info_update2()
        foecast_info_update3()
        demand_info_update1()
    # 更新後のデータを取得
    data_list = DemandData0.objects.all()
    for data in data_list:
        data.formatted_date = data.date.strftime('%Y-%m-%d')
        data.formatted_time = data.time.strftime('%H:%M')
        # 予測値の差を計算
        diff_q = abs(data.ploperformancet - data.prediction_q)
        diff_n = abs(data.ploperformancet - data.prediction_n)
        # 背景色のクラスを設定
        data.prediction_q_class = 'highlight' if diff_q < diff_n else ''
        data.prediction_n_class = 'highlight' if diff_n < diff_q else ''
    # タイムスタンプを生成
    timestamp = timezone.now().timestamp()
    # テンプレートにデータを渡してレンダリング
    response = render(request, 'dmd_gui/demand_info.html', {'data_list': data_list, 'timestamp': timestamp})
    return response

def setup(request):
    return render(request, 'dmd_gui/setup.html')


