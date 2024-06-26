import pandas as pd

# 讀取CSV文件，創建一個對照表將站名對應到區域
station_to_district = pd.read_csv('stations_districts.csv')

# 假設CSV文件包含兩列：'站名' 和 '區域'
# 將站名對應到區域，並轉換成DataFrame（這一步其實已經在讀取CSV時完成）
df = pd.DataFrame(station_to_district, columns=['站名', '區域'])

# 計算每個區域的出現次數
district_counts = df['區域'].value_counts()

# 印出每個區域及其對應的數據數量
print("每個區域的數據數量:")
for district, count in district_counts.items():
    print(f"{district}: {count}")
