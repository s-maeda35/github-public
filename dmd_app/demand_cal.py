import pandas as pd
from datetime import datetime
from workalendar.asia import Japan
# perform_in.to_csv('perform_in_aa.csv',encoding='shift_jis')

class demandCal:
    """
    各地点の需要予測値を計算するクラス
    
    """
    def __init__(self,time,day,fin,tmp,spot,hum):
        self.time = time
        self.dayType = day
        self.fingers = fin
        self.tmp = tmp
        self.spot = spot
        self.humidity = hum
        
    def dayTypeSelection1(self):
        """
        対象日が「祝日」OR「それ以外」を判定し、「祝日」OR「それ以外」のデータリストを作成。
        
        """
        # 設定情報
        perform_in = pd.read_csv('C:\\Users\\frontier-Python\\Desktop\\dmd_app\\perform_in.csv')
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
                    if self.dayType == 1 or self.dayType == 7:
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


    def dayTypeSelection2(self, perform_in):
        """
        対象日の「曜日」「時間」を基にデータリストの絞り込みを行う。さらに、対象日の「曜日」「時間」の1時間前のリストも作成する。
        
        """
        #②カラム「type」の中から指定の  曜日のレコードを抽出する。抽出したレコードだけのリストを作成する。
        
        if self.time == '00:00:00':
            if self.dayType == 0:
                perform_in = perform_in[(perform_in["type"] == self.dayType) | (perform_in["type"] == 7)]
                perform_in_now = perform_in[(perform_in["type"] == self.dayType) & (perform_in["pt_time"] == '00:00:00')]
                perform_in_past = perform_in[(perform_in["type"] == self.dayType -1) & (perform_in["pt_time"] == '23:00:00')]
            else:
                perform_in = perform_in[(perform_in["type"] == self.dayType) | (perform_in["type"] == self.dayType - 1)]
                perform_in_now = perform_in[(perform_in["type"] == self.dayType) & (perform_in["pt_time"] == '00:00:00')]
                perform_in_past = perform_in[(perform_in["type"] == self.dayType -1) & (perform_in["pt_time"] == '23:00:00')]
        else:
            perform_in = perform_in[perform_in["type"] == self.dayType]
            #③-1カラム「time」の中から指定の時間のレコードを抽出する。抽出したレコードだけのリストを作成する。
            perform_in_now = perform_in[perform_in["pt_time"] == self.time]
            #③-2カラム「time」の中から指定の時間の1時間前のレコードを抽出する。抽出したレコードだけのリストを作成する。 + ':00:00'
            time_timedelta = pd.to_timedelta(self.time)
            one_hour_delta = pd.to_timedelta('1 hour')
            one_hour_ago = time_timedelta - one_hour_delta
            one_hour_ago_formatted = one_hour_ago.components.hours.__str__().zfill(2) + ':' + one_hour_ago.components.minutes.__str__().zfill(2)+ ':' + one_hour_ago.components.seconds.__str__().zfill(2)       
            perform_in_past = perform_in[perform_in["pt_time"] == one_hour_ago_formatted]
        #「perform_in_now」は補正値の計算で使用するため代入
        
        perform_in = perform_in_now
        
        return perform_in, perform_in_now, perform_in_past
    
    def Correction_cal(self, perform_in, perform_in_now, perform_in_past):
        """
        補正計算を行う関数
        """
        in_spot_tmp = ["fk_temp","kg_temp","km_temp"]
        
        import numpy as np

        # perform_in[in_spot_tmp[self.spot]] - self.tmp の結果に NA が含まれている場合
        # values = (perform_in[in_spot_tmp[self.spot]] - self.tmp).abs().fillna(np.inf)
        # pickup_no = perform_in.index[values.argsort()][0]
        # values = (perform_in[in_spot_tmp[self.spot]] - self.tmp).abs().fillna(0)
        # pickup_no = perform_in.index[values.argsort()][0]
        
        #⑤抽出したレコードの中から気温が一番近いレコードを取得する。
        #pickup_no = perform_in.index[(perform_in[in_spot_tmp[self.spot]]-self.tmp).abs().argsort()][0]
        # print(pickup_no)
        # NA値、-inf、infを除外

        processed_values = (perform_in[in_spot_tmp[self.spot]] - self.tmp).abs()
        cleaned_values = processed_values.replace([np.inf, -np.inf], np.nan).dropna()

        # インデックス取得
        pickup_no = perform_in.index[cleaned_values.argsort()][0]
        
        
        if self.tmp >= 30.0:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] >= 30.0]
            now_index = perform_in_now.index
            # インデックスが存在するかを確認
            indices_to_check = [idx - 1 for idx in now_index if (idx - 1) in perform_in_past.index]
            perform_in_past = perform_in_past.loc[indices_to_check]
            perform_in_now_reset = perform_in_now.reset_index(drop=True)
            perform_in_past_reset = perform_in_past.reset_index(drop=True)
            ##現在プロットと同時刻の「需要」「気温」から1プロット前の「需要」「気温」で減算
            result = perform_in_now_reset[[in_spot_tmp[self.spot],'demand']] - perform_in_past_reset[[in_spot_tmp[self.spot],'demand']]
            
            # 条件を満たす行に 0 を設定し、それ以外は計算結果を設定
            result['correct'] = np.where(
                (result['demand'] == 0) | (result[in_spot_tmp[self.spot]] == 0), 
                0, 
                (result['demand'] / result[in_spot_tmp[self.spot]]) * 0.1
            )
            
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] <= 0.0]
            else:
                result = result[result['correct'] > 0.0]
        elif self.tmp >= 20.0:
            perform_in_now = perform_in_now[(perform_in_now[in_spot_tmp[self.spot]] >= 20.0) & (perform_in_now[in_spot_tmp[self.spot]] < 30.0)]
            now_index = perform_in_now.index
            
            # インデックスが存在するかを確認
            indices_to_check = [idx - 1 for idx in now_index if (idx - 1) in perform_in_past.index]
            perform_in_past = perform_in_past.loc[indices_to_check]
            perform_in_now_reset = perform_in_now.reset_index(drop=True)
            perform_in_past_reset = perform_in_past.reset_index(drop=True)  
            ##現在プロットと同時刻の「需要」「気温」から1プロット前の「需要」「気温」で減算
            result = perform_in_now_reset[[in_spot_tmp[self.spot],'demand']] - perform_in_past_reset[[in_spot_tmp[self.spot],'demand']]
            
            # 条件を満たす行に 0 を設定し、それ以外は計算結果を設定
            result['correct'] = np.where(
                (result['demand'] == 0) | (result[in_spot_tmp[self.spot]] == 0), 
                0, 
                (result['demand'] / result[in_spot_tmp[self.spot]]) * 0.1
            )
            
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] <= 0.0]
            else:
                result = result[result['correct'] > 0.0]
        elif self.tmp >= 10.0:
            perform_in_now = perform_in_now[(perform_in_now[in_spot_tmp[self.spot]] >= 10.0) & (perform_in_now[in_spot_tmp[self.spot]] < 20.0)]
            now_index = perform_in_now.index
            # インデックスが存在するかを確認
            indices_to_check = [idx - 1 for idx in now_index if (idx - 1) in perform_in_past.index]
            perform_in_past = perform_in_past.loc[indices_to_check]
            perform_in_now_reset = perform_in_now.reset_index(drop=True)
            perform_in_past_reset = perform_in_past.reset_index(drop=True)
            ##現在プロットと同時刻の「需要」「気温」から1プロット前の「需要」「気温」で減算
            result = perform_in_now_reset[[in_spot_tmp[self.spot],'demand']] - perform_in_past_reset[[in_spot_tmp[self.spot],'demand']]
            # 条件を満たす行に 0 を設定し、それ以外は計算結果を設定
            result['correct'] = np.where(
                (result['demand'] == 0) | (result[in_spot_tmp[self.spot]] == 0), 
                0, 
                (result['demand'] / result[in_spot_tmp[self.spot]]) * 0.1
            )
            ##現在の気温が基準日時の気温より低い場合は、補正値（kW）リストの中からプラスのものを抽出 
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] >= 0.0]
            else:
                result = result[result['correct'] < 0.0]           
        else:
            perform_in_now = perform_in_now[perform_in_now[in_spot_tmp[self.spot]] < 10]
            now_index = perform_in_now.index
            # インデックスが存在するかを確認
            indices_to_check = [idx - 1 for idx in now_index if (idx - 1) in perform_in_past.index]
            perform_in_past = perform_in_past.loc[indices_to_check]
            perform_in_now_reset = perform_in_now.reset_index(drop=True)
            perform_in_past_reset = perform_in_past.reset_index(drop=True)
            result = perform_in_now_reset[[in_spot_tmp[self.spot],'demand']] - perform_in_past_reset[[in_spot_tmp[self.spot],'demand']]
            # 条件を満たす行に 0 を設定し、それ以外は計算結果を設定
            result['correct'] = np.where(
                (result['demand'] == 0) | (result[in_spot_tmp[self.spot]] == 0), 
                0, 
                (result['demand'] / result[in_spot_tmp[self.spot]]) * 0.1
            )
            if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                result = result[result['correct'] >= 0.0]
            else:
                result = result[result['correct'] < 0.0]
        #需要変化量「kW」のリストの中から中央値を算出
        if result.empty:
            result = pd.DataFrame({'correct': [0.0]})   
        correct_value = result['correct'].median() 

        #⑦上記⑤で抽出した需要に補正値を考慮する。
        tmp_Differential = self.tmp - perform_in.loc[pickup_no][in_spot_tmp[self.spot]]
        plot_result = perform_in.loc[pickup_no]['demand'] + (correct_value * (tmp_Differential + 1))
        return plot_result
        
    def demand_select(self):
        """
        「dayTypeSelection1」「dayTypeSelection2」「Correction_cal」を実行する関数

        """
        perform_in_dayTypeSelection1 = self.dayTypeSelection1()
        perform_in, perform_in_now, perform_in_past = self.dayTypeSelection2(perform_in_dayTypeSelection1)
        plot_result = self.Correction_cal(perform_in, perform_in_now, perform_in_past)
        return plot_result


