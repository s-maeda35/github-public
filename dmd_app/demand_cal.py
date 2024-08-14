import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class demandCal:
    """
    需要予測値を計算するクラス
    
    """
    def __init__(self, time, day, tmp, spot, perform_in):
        """
        コンストラクタ
    
        """
        self.time = time
        self.dayType = day
        self.tmp = tmp
        self.spot = spot
        self.perform_in = perform_in
        
    def dayTypeSelection2(self):
        """
        対象日の「曜日」「時間」を基にデータリストの絞り込みを行い、対象日の「曜日」「時間」の1時間前のリストを作成する関数
        
        """
        # 「type」の中から指定の  曜日のレコードを抽出する。抽出したレコードだけのリストを作成する。
        # 「time」が0時の場合や「type」が0の場合は特別処理を行う。
        perform_in = self.perform_in
        if self.time == '00:00:00': 
            if self.dayType == 0: 
                perform_in = perform_in[(perform_in["type"] == self.dayType) | (perform_in["type"] == 6)]
            else:
                perform_in = perform_in[(perform_in["type"] == self.dayType) | (perform_in["type"] == self.dayType - 1)]
            perform_in_now = perform_in[(perform_in["type"] == self.dayType) & (perform_in["pt_time"] == '00:00:00')]
            perform_in_past = perform_in[(perform_in["type"] == self.dayType -1) & (perform_in["pt_time"] == '23:00:00')]
        else:
            perform_in = perform_in[perform_in["type"] == self.dayType]
            #③-1カラム「time」の中から指定の時間のレコードを抽出する。抽出したレコードだけのリストを作成する。
            perform_in_now = perform_in[perform_in["pt_time"] == self.time]
            #③-2カラム「time」の中から指定の時間の1時間前のレコードを抽出する。抽出したレコードだけのリストを作成する。 
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
        def temperature_sensitivity(cal_spot, temp_start, temp_end, perform_in):
            """
            回帰モデル係数を使用して、気温感応度を算出する関数
            
            """
            # データの準備（仮想データ）
            perform_in_ts = perform_in
            # 説明変数と目的変数の設定
            X = perform_in_ts[[cal_spot]]
            y = perform_in_ts['demand']
            # 欠損値を削除
            valid_indices = X.notna().all(axis=1) & y.notna()
            X = X[valid_indices]
            y = y[valid_indices]
            # 線形回帰モデルの構築
            model = LinearRegression()
            model.fit(X, y)
            # 回帰モデルの係数（気温感応度）
            temperature_sensitivity = model.coef_[0]
            temp_change = temp_end - temp_start
            correct_value_Differential = temperature_sensitivity * temp_change
            return correct_value_Differential
        
        in_spot_tmp = ["fk_temp","kg_temp","km_temp"]
        # 補正値のリストを作成する。絶対値に変換
        processed_values = (perform_in[in_spot_tmp[self.spot]] - self.tmp).abs()
        cleaned_values = processed_values.replace([np.inf, -np.inf], np.nan).dropna()
        # 一番気温差が少ないインデックス(0に近いインデックス)を取得(基準日時の選定)
        pickup_no = perform_in.index[cleaned_values.argsort()][0]
        try:
            # 抽出した需要に気温差を考慮して補正値を算出
            temp_end = perform_in.loc[pickup_no][in_spot_tmp[self.spot]]
            correct_value_Differential = temperature_sensitivity(in_spot_tmp[self.spot], self.tmp, temp_end, perform_in)
        except Exception:
            # 機械学習を使用した補正値の作成に失敗した場合は、別の手法で補正値を作成
            try:
                # ±3度の範囲でフィルタリング
                lower_bound = self.tmp - 3.0
                upper_bound = self.tmp + 3.0
                perform_in_now = perform_in_now[(perform_in_now[in_spot_tmp[self.spot]] >= lower_bound) & (perform_in_now[in_spot_tmp[self.spot]] <= upper_bound)]
                now_index = perform_in_now.index
                # インデックスが存在するかを確認
                indices_to_check = [idx - 1 for idx in now_index if (idx - 1) in perform_in_past.index]
                perform_in_past = perform_in_past.loc[indices_to_check]
                perform_in_now_reset = perform_in_now.reset_index(drop=True)
                perform_in_past_reset = perform_in_past.reset_index(drop=True)
                # 現在プロットと同時刻の「需要」「気温」から1プロット前の「需要」「気温」で減算
                result = perform_in_now_reset[[in_spot_tmp[self.spot],'demand']] - perform_in_past_reset[[in_spot_tmp[self.spot],'demand']]
                # 条件を満たす行に 0 を設定し、それ以外は計算結果を設定
                result['correct'] = np.where(
                    (result['demand'] == 0) | (result[in_spot_tmp[self.spot]] == 0), 
                    0, 
                    (result['demand'] / result[in_spot_tmp[self.spot]]) * 0.1
                )
                if self.tmp >= 15.0:
                    if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                        result = result[result['correct'] >= 0.0]
                    else:
                        result = result[result['correct'] < 0.0]
                else:
                    if self.tmp <= perform_in.loc[pickup_no][in_spot_tmp[self.spot]]: 
                        result = result[result['correct'] <= 0.0]
                    else:
                        result = result[result['correct'] > 0.0]            
                if result.empty:
                    result = pd.DataFrame({'correct': [0.0]})
                # 需要変化量「kW」のリストの中から中央値を算出
                correct_value = result['correct'].median()
                tmp_Differential = self.tmp - perform_in.loc[pickup_no][in_spot_tmp[self.spot]]
                correct_value_Differential = correct_value * (tmp_Differential)
                # 抽出した需要に補正値を加算
                plot_result = perform_in.loc[pickup_no]['demand'] + correct_value_Differential
                return plot_result
            except:
                correct_value_Differential = 0.0
        finally:
            # 抽出した需要に補正値を加算
            plot_result = perform_in.loc[pickup_no]['demand'] + correct_value_Differential
            return plot_result


    def demand_select(self):
        """
        「dayTypeSelection1」「dayTypeSelection2」「Correction_cal」を実行する関数

        """
        perform_in, perform_in_now, perform_in_past = self.dayTypeSelection2()
        plot_result = self.Correction_cal(perform_in, perform_in_now, perform_in_past)
        return plot_result


