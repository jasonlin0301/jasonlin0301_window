import pandas as pd

# 讀取CSV文件
file_path = 'weather_data.csv'  # 確保這個文件在你的工作目錄中
weather_data = pd.read_csv(file_path)

# 提取唯一的站名
unique_stations = weather_data['站名'].drop_duplicates()

# 印出唯一的站名
print("所有唯一的站名:")
for station in unique_stations:
    print(station)
