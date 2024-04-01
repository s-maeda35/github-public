import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import japanize_matplotlib

class forecast_graphic:
    def __init__(self, f_info, temperature, humidity, spot, discomfort_index, daytype):
        self.f_info = f_info
        self.temperature = temperature
        self.humidity = humidity
        self.spot = spot
        self.discomfort_index = discomfort_index
        self.daytype = daytype
    
    def forecast_tk(self):
        # Matplotlibのグラフを描画する関数
        def draw_graph():
            fig = Figure(figsize = (8, 6), dpi = 150)
            ax = fig.add_subplot(111)
            ax.plot(today_info, marker = 'o', linestyle = '-')
            ax.set_title(self.spot)
            ax.set_xlabel('時間')
            ax.set_ylabel('％')
            ax.grid(True)
            ax.legend(today_info, loc = 'upper right')
            return fig
        
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

        # DataFrame内のすべての要素をfloat型に変換
        today_info = today_info.astype(float)

        # 'データ名'列をインデックスに設定し、転置する
        today_info = today_info.T

        # Tkinterウィンドウの作成
        root = tk.Tk()
        root.title("気象情報")

        # Matplotlibのグラフを描画してTkinterウィンドウに埋め込む
        fig = draw_graph()
        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # イベントループの開始
        root.mainloop()