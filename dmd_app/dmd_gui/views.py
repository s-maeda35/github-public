from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from data_input import foecast_info_update1, foecast_info_update2, foecast_info_update3, demand_info_update1, demand_graph
from demand_main import d_main
from .models import DemandData0
from django.utils import timezone
from django.views.decorators.cache import never_cache

@never_cache # HTTP応答のキャッシュを無効
def login_view(request):
    """
    「ログイン」画面を処理する関数
    
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'dmd_gui/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'dmd_gui/login.html')

@never_cache # HTTP応答のキャッシュを無効
@login_required #ログイン時以外はアクセス不可
def index(request):
    """
    「ホーム」画面を処理する関数
    
    """
    return render(request, 'dmd_gui/index.html')

@never_cache
@login_required
def logout_view(request):
    """
    ログアウトに関する処理を実行する関数
    
    """
    logout(request)
    return redirect('login')

@never_cache
@login_required 
def forecast_all(request):
    """
    「気象情報(概要)」画面を処理する関数
    
    """
    if request.method == 'POST':
        try:
            foecast_info_update1()
            foecast_info_update2()
        except Exception as e:
            return render(request, 'dmd_gui/index.html', {'error_message': str(e)})
    # タイムスタンプを生成
    timestamp = timezone.now().timestamp()
    # テンプレートにデータを渡してレンダリング
    response = render(request, 'dmd_gui/forecast_all.html', {'timestamp': timestamp})
    return response

@never_cache
@login_required
def forecast_details(request):
    """
    「気象情報(詳細)」画面を処理する関数
    
    """
    if request.method == 'POST':
        try:
            foecast_info_update3()
        except Exception as e:
            return render(request, 'dmd_gui/index.html', {'error_message': str(e)})
    # タイムスタンプを生成
    timestamp = timezone.now().timestamp()
    # テンプレートにデータを渡してレンダリング
    response = render(request, 'dmd_gui/forecast_details.html', {'timestamp': timestamp})
    return response

@never_cache
@login_required
def demand_info(request):
    """
    「需要予測情報」画面を処理する関数
    
    """
    if request.method == 'POST':
        try:
            demand_info_update1()
            d_main()
            demand_graph()
        except Exception as e:
            return render(request, 'dmd_gui/demand_info.html', {'error_message': str(e)})
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
    response = render(request, 'dmd_gui/demand_info.html', {
        'data_list': data_list, 
        'timestamp': timestamp,
        })
    return response





