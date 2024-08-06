from matplotlib.figure import Figure
import japanize_matplotlib

class forecast_graphic:
    # コンストラクタの定義
    def __init__(self, f_info, temperature, humidity, spot, discomfort_index, daytype):
        self.f_info = f_info
        self.temperature = temperature
        self.humidity = humidity
        self.spot = spot
        self.discomfort_index = discomfort_index
        self.daytype = daytype
        
    # Matplotlibのグラフを描画する関数
    def draw_graph(self,today_info):
        fig = Figure(figsize = (8, 6), dpi = 80)
        ax = fig.add_subplot(111)
        ax.plot(today_info, marker = 'o', linestyle = '-')
        ax.set_title(self.spot)
        ax.set_xlabel('時刻')
        ax.set_ylabel('℃(％)', rotation = 90)
        ax.grid(True)
        ax.legend(['気温(℃)', '湿度(％)', '不快指数'], loc='upper right')
        ax.set_xticks(today_info.index)
        ax.set_xticklabels(today_info.index, rotation = 90)
        return fig    
    
    #取得した気象情報を抽出し、グラフに加工するメソッド
    def forecast_gf(self):
        #当日/翌日の気象情報を取得 
        today_info = self.f_info.loc[[self.temperature, self.humidity]]
        today_info = today_info[today_info['type'] == self.daytype]
        tfr = []
        #使用しない列を削除
        today_info = today_info.drop('type', axis = 1)
        today_info = today_info.drop('spot', axis = 1)
        #気温と湿度を抽出して不快指数を計算
        for i in today_info.columns:
            tmp = float(today_info.loc[self.temperature, i])
            humidity = float(today_info.loc[self.humidity, i])
            discomfort_index = 0.81 * tmp + 0.01 * humidity * (0.99 * tmp - 14.3) + 46.3
            tfr.append(round(discomfort_index))
        # 新しい行を追加
        today_info.loc[self.discomfort_index] = [tfr[0], tfr[1], tfr[2], tfr[3], tfr[4],tfr[5], tfr[6],\
                                                tfr[7], tfr[8], tfr[9], tfr[10], tfr[11],tfr[12], tfr[13],\
                                                tfr[14], tfr[15], tfr[16], tfr[17], tfr[18],tfr[19], tfr[20],\
                                                tfr[21], tfr[22], tfr[23]]
        today_info = today_info.astype(float)  # DataFrame内のすべての要素をfloat型に変換
        today_info = today_info.T  # データ名列をインデックスに設定し、転置する
        #説明用##########################
        print(today_info)
        print(type(today_info))
        #説明用##########################
        fig = self.draw_graph(today_info)  #関数の呼び出し
        return fig