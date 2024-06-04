from pprint import pprint
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import tools

class Window(ThemedTk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.title("全臺空氣品質指標(AQI)")
        self.option_add("*Font","微軟正黑體 40")
        style = ttk.Style()
        style.configure('TFrame')
        title_Frame=ttk.Frame(self)


def main():
    '''
    try:
        all_data:dict[any] = tools.download_json()
    except Exception as error:
        print(error)
    else:        
        data:list[dict] = tools.get_data(all_data)
        pprint(data)
    '''
    window = Window(theme="black")
    window.mainloop()
    

if __name__ == '__main__':
    main()