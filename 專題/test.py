import pandas as pd

# 使用原始字符串以避免路径问题
file_path = r'C:\Users\user\Documents\GitHub\jasonlin0301_window\專題\weather_data.csv'

# 讀取 CSV 文件
weather_data = pd.read_csv(file_path)

# 定義查詢函數（這裡使用模擬查詢）
def get_region_from_station(station_name):
    # 模擬一個查詢過程
    region_map = {
        '茶改東部分場': '台東縣',
        '桃改樹林分場': '桃園市',
        '茶改北部分場': '新北市',
        '桃園農改': '桃園市',
        '茶改場': '南投縣',
        '農工中心': '苗栗縣'
    }
    return region_map.get(station_name, '未知地區')

# 遍歷 CSV 文件中的站名
station_names = weather_data['站名']
station_to_region = {station: get_region_from_station(station) for station in station_names}

# 打印站名和對應的地區
for station, region in station_to_region.items():
    print(f"{station}: {region}")
