import json
import requests
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Dict, Any
from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox

def download_json():
    url = "https://raw.githubusercontent.com/LanvisWei/MLproject_Solar_Irradiance/main/weather_data.json"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"連線失敗: {e}")
    else:
        all_data = res.json()
        return all_data

class WeatherInfo(BaseModel):
    站名: str
    平均氣溫: str
    絕對最高氣溫: str
    絕對最高氣溫日期: str
    絕對最低氣溫: float
    絕對最低氣溫日期: str
    平均相對濕度: str
    總降雨量: str
    平均風速: str
    最多風向: str
    總日照時數: str
    總日射量: str
    平均地溫_0cm: str
    平均地溫_5cm: str
    平均地溫_10cm: str
    平均地溫_20cm: str
    平均地溫_50cm: str
    平均地溫_100cm: str
    Year: int
    Month: int

    @field_validator('平均氣溫', '絕對最高氣溫', '平均相對濕度', '總降雨量', '平均風速', '總日照時數', '總日射量',
                     '平均地溫_0cm', '平均地溫_5cm', '平均地溫_10cm', '平均地溫_20cm', '平均地溫_50cm', '平均地溫_100cm',
                     mode='before')
    def parse_float(cls, value):
        try:
            return float(value)
        except ValueError:
            return value

class WeatherData(BaseModel):
    data: List[WeatherInfo]

class FilterData:
    @staticmethod
    def get_selected_info(station_name: str, data: List[Dict[str, Any]]) -> WeatherInfo:
        filtered_data = list(filter(lambda item: item['站名'] == station_name, data))
        if not filtered_data:
            raise ValueError(f"站名為 '{station_name}' 的數據不存在")
        return WeatherInfo(**filtered_data[0])

class Window(ThemedTk):
    def __init__(self, theme: str = 'arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title('台北市YouBike2.0及時資料')
        try:
            self.__data = download_json()
        except Exception as e:
            messagebox.showwarning(title='警告', message=str(e))
            self.__data = []

        self._display_interface()

    @property
    def data(self) -> list[dict]:
        return self.__data

    def _display_interface(self):
        mainFrame = ttk.Frame(borderwidth=1, relief='groove')
        ttk.Label(mainFrame, text="台北市YouBike2.0及時資料", font=('arial', 25)).pack(pady=(20, 10))
        # =================================
        tableFrame = ttk.Frame(mainFrame)
        columns = ('站名', '平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總降雨量', '平均風速', '總日照時數')
        tree = ttk.Treeview(tableFrame, columns=columns, show='headings', selectmode='browse')
        # define headings
        tree.heading('站名', text='站名')
        tree.heading('平均氣溫', text='平均氣溫')
        tree.heading('絕對最高氣溫', text='絕對最高氣溫')
        tree.heading('絕對最低氣溫', text='絕對最低氣溫')
        tree.heading('總降雨量', text='總降雨量')
        tree.heading('平均風速', text='平均風速')
        tree.heading('總日照時數', text='總日照時數')

        # 定義欄位寬度
        tree.column('站名', width=100, anchor=tk.CENTER)
        tree.column('平均氣溫', width=100, anchor=tk.CENTER)
        tree.column('絕對最高氣溫', width=100, anchor=tk.CENTER)
        tree.column('絕對最低氣溫', width=100, anchor=tk.CENTER)
        tree.column('總降雨量', width=100, anchor=tk.CENTER)
        tree.column('平均風速', width=100, anchor=tk.CENTER)
        tree.column('總日照時數', width=100, anchor=tk.CENTER)

        # bind使用者的事件
        tree.bind('<<TreeviewSelect>>', self.item_selected)

        # add data to the treeview
        for site in self.data:
            tree.insert('', tk.END,
                        values=(site['站名'], site['平均氣溫'], site['絕對最高氣溫'], site['絕對最低氣溫'], site['總降雨量'], site['平均風速'], site['總日照時數']))

        tree.grid(row=0, column=0, sticky='nsew')

        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tableFrame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        # ======================================
        mainFrame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def item_selected(self, event):
        tree = event.widget
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record: list = item['values']
            station_name = record[0]
            try:
                site_data = FilterData.get_selected_info(station_name, self.data)
                messagebox.showinfo(title=site_data.站名, message=str(site_data))
            except ValueError as e:
                messagebox.showerror(title='錯誤', message=str(e))

def main():
    window = Window(theme='breeze')
    window.mainloop()

if __name__ == '__main__':
    main()
