#import demand_cal as dc
import forecast_in as fi
import graph_plot as gp
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#1回目課題範囲#################################
#当日/翌日の気象情報を取得 
f_info = fi.foecast_info()

def show_selection(button_num,f_info):
    temperature_list = ['fk_temperature', 'oo_temperature', 'mz_temperature', 'kg_temperature', 'km_temperature', 'ng_temperature', 'sg_temperature']
    humidity_list = ['fk_humidity', 'oo_humidity', 'mz_humidity', 'kg_humidity', 'km_humidity', 'ng_humidity', 'sg_humidity']
    spot_list = ['福岡市', '大分市', '宮崎市', '鹿児島市', '熊本市', '長崎市', '佐賀市']
    discomfort_index_list = ['fk_discomfort_index', 'oo_discomfort_index', 'mz_discomfort_index', 'kg_discomfort_index', 'km_discomfort_index', 'ng_discomfort_index', 'sg_discomfort_index']
    #ラジオボタンの値を取得し、int型へ変換
    selected_value = radio_var.get()
    int(selected_value)
    #選択された地点のインスタンスを作成
    graph = gp.forecast_graphic(f_info, temperature_list[button_num], humidity_list[button_num], spot_list[button_num], discomfort_index_list[button_num], int(selected_value))
    graph = graph.forecast_gf()
    # Matplotlibのグラフを描画してTkinterウィンドウに埋め込む
    canvas = FigureCanvasTkAgg(graph, master = root)
    canvas.draw()
    canvas.get_tk_widget().grid(row = 9, column = 2)

# Tkinterウィンドウの作成
root = tk.Tk()
root.geometry("900x700")
root.title("気象情報")
label = tk.Label(root, text = "【当日/翌日】").grid(row = 0, column = 0)
label = tk.Label(root, text = "【地点一覧 】").grid(row = 3, column = 0)
label = tk.Label(root, text = "【不快指数(目安)】").grid(row = 0, column = 2, sticky="w")
label = tk.Label(root, text = "・  ～55：寒い　　　　　　").grid(row = 1, column = 2, sticky="w")
label = tk.Label(root, text = "・55〜60：肌寒い　　　　　").grid(row = 2, column = 2, sticky="w")
label = tk.Label(root, text = "・60〜65：何も感じない　　").grid(row = 3, column = 2, sticky="w")
label = tk.Label(root, text = "・65〜70：快い　　　　　　").grid(row = 4, column = 2, sticky="w")
label = tk.Label(root, text = "・70〜75：暑くない　　　　").grid(row = 5, column = 2, sticky="w")
label = tk.Label(root, text = "・75〜80：やや暑い　　　　").grid(row = 6, column = 2, sticky="w")
label = tk.Label(root, text = "・80〜85：暑くて汗が出る　").grid(row = 7, column = 2, sticky="w")
label = tk.Label(root, text = "・85〜  ：暑くてたまらない").grid(row = 8, column = 2, sticky="w")
# ラジオボタンの値を格納する変数
radio_var = tk.StringVar(value = 0)

# ラジオボタンの作成
radio_button1 = tk.Radiobutton(root, text = "当日", variable = radio_var, value = 0).grid(row = 1, column = 0)
radio_button2 = tk.Radiobutton(root, text = "翌日", variable = radio_var, value = 1).grid(row = 2, column = 0)

# ボタンを作成し、選択された場合にshow_selection関数を呼び出す
button1 = tk.Button(root, text = "福岡市　", command = lambda: show_selection(0, f_info)).grid(row = 4, column = 0)
button2 = tk.Button(root, text = "大分市　", command = lambda: show_selection(1, f_info)).grid(row = 5, column = 0)
button3 = tk.Button(root, text = "宮崎市　", command = lambda: show_selection(2, f_info)).grid(row = 6, column = 0)
button4 = tk.Button(root, text = "鹿児島市", command = lambda: show_selection(3, f_info)).grid(row = 7, column = 0)
button5 = tk.Button(root, text = "熊本市　", command = lambda: show_selection(4, f_info)).grid(row = 4, column = 1)
button6 = tk.Button(root, text = "長崎市　", command = lambda: show_selection(5, f_info)).grid(row = 5, column = 1)
button3 = tk.Button(root, text = "佐賀市　", command = lambda: show_selection(6, f_info)).grid(row = 6, column = 1)

#初期表示として、「福岡市（当日）」を表示
show_selection(0, f_info)

# イベントループの開始
root.mainloop()

#1回目課題範囲#################################

"""
#デバッグ用####################################
time = '9:00'
dayType = 6
fk_tmp = 8.9
fk_fingers = 9
kg_tmp = 11.5
kg_fingers=9
km_tmp = 9.6
km_fingers=9
fk_spot=0
kg_spot=1
km_spot=2
fk_humidity=0
kg_humidity=0
km_humidity=0
#デバッグ用####################################

#需要比率（2023年11月）政府統計より
#グループ1：福岡：37％、佐賀：8％
group1_demand_ratio = ((38 + 8) / 100)
#グループ2：鹿児島：12％、宮崎：8％
group2_demand_ratio = ((12 + 8) / 100)
#グループ3：熊本：14％、長崎：10％、大分：10％
group3_demand_ratio = ((14 + 10 + 10) / 100)

#対象プロットの「基準日/時間」を取得する
fk_dc=dc.demandCal(time,dayType,fk_fingers,fk_tmp,fk_spot,fk_humidity)
fk_demand = fk_dc.demand_select()
print(fk_demand)
fk_demand = fk_demand * group1_demand_ratio
print(fk_demand)

kg_dc=dc.demandCal(time,dayType,kg_fingers,kg_tmp,kg_spot,kg_humidity)
kg_demnd = kg_dc.demand_select()
print(kg_demnd)
kg_demnd = kg_demnd * group2_demand_ratio
print(kg_demnd)

km_dc=dc.demandCal(time,dayType,km_fingers,km_tmp,km_spot,km_humidity)
km_demand = km_dc.demand_select()
print(km_demand)
km_demand = km_demand * group3_demand_ratio
print(km_demand)

plot_demand = fk_demand + kg_demnd + km_demand
print(plot_demand)

"""
