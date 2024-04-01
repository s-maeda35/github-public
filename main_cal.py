#import demand_cal as dc
import forecast_in as fi
import graph_plot as gp

#1回目課題範囲#################################
#当日/翌日の気象情報を取得 
f_info = fi.foecast_info()

#福岡市の気象情報をグラフ表示し、tkinterに埋め込み
fk_graph = gp.forecast_graphic(f_info, 'fk_temperature', 'fk_humidity', '福岡市', 'fk_discomfort_index', 0)
fk_graph.forecast_tk()

"""
#大分市の気象情報をグラフ表示し、tkinterに埋め込み
oo_graph = gp.forecast_graphic(f_info, 'oo_temperature', 'oo_humidity', '大分市', 'oo_discomfort_index', 0)
oo_graph.forecast_tk()

#鹿児島市の気象情報をグラフ表示し、tkinterに埋め込み
kg_graph = gp.forecast_graphic(f_info, 'kg_temperature', 'kg_humidity', '鹿児島市', 'kg_discomfort_index', 0)
kg_graph.forecast_tk()

#熊本市の気象情報をグラフ表示し、tkinterに埋め込み
km_graph = gp.forecast_graphic(f_info, 'km_temperature', 'km_humidity', '熊本市', 'km_discomfort_index', 0)
km_graph.forecast_tk()

#長崎市の気象情報をグラフ表示し、tkinterに埋め込み
ng_graph = gp.forecast_graphic(f_info, 'ng_temperature', 'ng_humidity', '長崎市', 'ng_discomfort_index', 0)
ng_graph.forecast_tk()

#佐賀市の気象情報をグラフ表示し、tkinterに埋め込み
sg_graph = gp.forecast_graphic(f_info, 'sg_temperature', 'sg_humidity', '佐賀市', 'sg_discomfort_index', 0)
sg_graph.forecast_tk()
"""

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
