import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
from workalendar.asia import Japan
from datetime import date


class demandCal:
    def __init__(self,time,day,fin,tmp,spot,hum):
        self.time = time
        self.dayType = day
        self.fingers = fin
        self.tmp = tmp
        self.spot = spot
        self.humidity = hum
        
    def demand_select(self):
        in_spot_fingers = ["fk_fingers","kg_fingers","km_fingers"]
        in_spot_tmp = ["fk_temp","kg_temp","km_temp"]
        perform_in = pd.read_csv('C:\\Users\\misao\\OneDrive\\Desktop\\PY\\source\\perform_in.csv')
        #①カラム「date」の中から対象日が「祝日」の場合には「祝日」を抽出する。対象日が祝日でない場合には、リストから「祝日」を除外する。
        perform_in_holiday_list = perform_in
        perform_in_holiday_list = perform_in_holiday_list.drop(perform_in_holiday_list.index, axis=0)
        year_list = [2020,2021,2022,2023,2024]
        cal = Japan()
        check_date_str = "2023-01-20"
        check_date = datetime.strptime(check_date_str, "%Y-%m-%d").date()
        perform_in['date'] = pd.to_datetime(perform_in['date']).dt.date
        for i in year_list:
            holidays_tuple = cal.holidays(i)
            for holiday in holidays_tuple:
                holiday_list = list(holiday)
                if check_date == holiday_list[0]:
                    #リストの中から祝日のみのリストを抽出する。ただし、祝日が土曜日または日曜日の場合にはifブロックを抜ける。if self.type == 1 or self.time == 7: pass else:　　　　　　
                    perform_in = perform_in[perform_in["date"] == holiday_list[0]] 
                    print(perform_in)
                    break
                perform_in_holiday = perform_in[perform_in["date"] == holiday_list[0]]
                perform_in_holiday_list = pd.concat([perform_in_holiday_list, perform_in_holiday], ignore_index=True)
        else:
            #リストの中から祝日以外のリストを抽出する
            perform_in = pd.merge(perform_in, perform_in_holiday_list, indicator=True, how='outer').query('_merge == "left_only"').drop(columns=['_merge'])
        
        
        #②カラム「type」の中から指定の  曜日のレコードを抽出する。抽出したレコードだけのリストを作成する。
        perform_in=perform_in[perform_in["type"] == self.dayType]
        #③-1カラム「time」の中から指定の時間のレコードを抽出する。抽出したレコードだけのリストを作成する。
        perform_in_now=perform_in[perform_in["pt_time"] == self.time]

        #③-2カラム「time」の中から指定の時間の1時間前のレコードを抽出する。抽出したレコードだけのリストを作成する。 + ':00:00'
        time_timedelta = pd.to_timedelta(self.time)
        one_hour_delta = pd.to_timedelta('1 hour')
        one_hour_ago = time_timedelta - one_hour_delta
        one_hour_ago_formatted = one_hour_ago.components.hours.__str__().zfill(2) + ':' + one_hour_ago.components.minutes.__str__().zfill(2)+ ':' + one_hour_ago.components.seconds.__str__().zfill(2)       
        perform_in_past = perform_in[perform_in["pt_time"] == one_hour_ago_formatted]
        
        #④カラム「fingers」の中から指定の時間のレコードを抽出する。抽出したレコードだけのリストを作成する。
        #「perform_in_now」は補正値の計算で使用するため代入
        perform_in = perform_in_now 
        #perform_in = perform_in[perform_in[in_spot_fingers[self.spot]] == self.fingers]
        #⑤抽出したレコードの中から気温が一番近いレコードを取得する。
        pickup_no = perform_in.index[(perform_in[in_spot_tmp[self.spot]]-self.tmp).abs().argsort()][0]
        
        """ perform_in.to_csv('ffffffff.csv')
        #⑥抽出したレコードの中から気温(0.1度)あたりの補正値を計算する。
        perform_in_now.reset_index(drop=True, inplace=True)
        perform_in_past.reset_index(drop=True, inplace=True)
        perform_in.to_csv('gggggggg.csv') """
        
        #線形回帰モデルを使用して対象プロットの「気温感応度」を分析する。
        #その後、対象プロットの気温感応度を基に「基準日/時間」の需要を補正する。
        ##前プロットの気温　-　対象プロットの気温　＝　X（気温変化量）
        ##0.1度あたりの需要増減　*　X（気温変化量）　＝補正値
        ##対象プロットの需要　+　補正値　＝　対象プロットの需要（補正後）　
        ##計算対象プロットの気温により、補正に使用するデータを絞り込む
        if self.tmp >= 30.0:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] >= 30.0]
            now_index = perform_in_now.index
            perform_in_past =  perform_in_past.loc[now_index]
            ##現在プロットと同時刻の「需要」「気温」から1プロット前の「需要」「気温」で減算
            result = perform_in_now[[in_spot_tmp[self.spot],'demand']] - perform_in_past[[in_spot_tmp[self.spot],'demand']]
            ##気温の変化0.1度あたりの需要変化量「kW」を算出
            result['correct'] = (result['demand'] / result[in_spot_tmp[self.spot]]) *0.1
            ##現在の気温が基準日時の気温より低い場合は、補正値（kW）リストの中からマイナスのものを抽出 
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] <= 0.0]
            else:
                result = result[result['correct'] > 0.0]
        elif self.tmp >= 20.0:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] >= 20.0]
            now_index = perform_in_now.index
            perform_in_past =  perform_in_past.loc[now_index]
            result = perform_in_now[[in_spot_tmp[self.spot],'demand']] - perform_in_past[[in_spot_tmp[self.spot],'demand']]
            result['correct'] = (result['demand'] / result[in_spot_tmp[self.spot]]) *0.1 
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] <= 0.0]
            else:
                result = result[result['correct'] > 0.0]            
        elif self.tmp >= 10.0:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] >= 10.0]
            now_index = perform_in_now.index
            perform_in_past =  perform_in_past.loc[now_index]
            result = perform_in_now[[in_spot_tmp[self.spot],'demand']] - perform_in_past[[in_spot_tmp[self.spot],'demand']]
            result['correct'] = (result['demand'] / result[in_spot_tmp[self.spot]]) *0.1
            ##現在の気温が基準日時の気温より低い場合は、補正値（kW）リストの中からプラスのものを抽出 
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] >= 0.0]
            else:
                result = result[result['correct'] < 0.0]           
        else:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] < 10]
            now_index = perform_in_now.index
            perform_in_past =  perform_in_past.loc[now_index]
            result = perform_in_now[[in_spot_tmp[self.spot],'demand']] - perform_in_past[[in_spot_tmp[self.spot],'demand']]
            result['correct'] = (result['demand'] / result[in_spot_tmp[self.spot]]) *0.1 
            print(perform_in.loc[36729])
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] >= 0.0]
            else:
                result = result[result['correct'] < 0.0]
                
        ##需要変化量「kW」のリストの中から中央値を算出
        correct_value = result['correct'].median() 

        #⑦上記⑤で抽出した需要に補正値を考慮する。
        tmp_Differential = self.tmp - perform_in.loc[pickup_no][in_spot_tmp[self.spot]]
        plot_result = perform_in.loc[pickup_no]['demand'] + (correct_value * (tmp_Differential + 1))
        return plot_result

        
        ##デバッグ用############################################################
        #print(perform_in_now[['fk_temp','demand']])
        #print(perform_in_past[['fk_temp','demand']])
        #print(result)
        #print(correct_value)
        if self.spot==0:
            perform_in.loc[pickup_no].to_csv('fk.csv',encoding='shift_jis')
            #perform_in_now.to_csv('fk_perform_in_now.csv',encoding='shift_jis')
            #perform_in_past.to_csv('fk_perform_in_past.csv',encoding='shift_jis')
            #result.to_csv('fk_result.csv',encoding='shift_jis')
        elif self.spot==1:
            perform_in.loc[pickup_no].to_csv('kg.csv',encoding='shift_jis')
            #perform_in_now.to_csv('fk_perform_in_now.csv',encoding='shift_jis')
            #perform_in_past.to_csv('fk_perform_in_past.csv',encoding='shift_jis')
            #result.to_csv('fk_result.csv',encoding='shift_jis')
        else:
            perform_in.loc[pickup_no].to_csv('km.csv',encoding='shift_jis')
            #perform_in_now.to_csv('fk_perform_in_now.csv',encoding='shift_jis')
            #perform_in_past.to_csv('fk_perform_in_past.csv',encoding='shift_jis')
            #result.to_csv('fk_result.csv',encoding='shift_jis')
        ########################################################################


        
#デバッグ用####################################
time = '09:00:00'
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





