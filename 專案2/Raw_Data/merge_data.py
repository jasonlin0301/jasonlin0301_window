import pandas as pd
import os

# 初始化存儲所有數據的列表
all_data = []

# 指定年份範圍
start_year = 1999
end_year = 2024

# 遍歷每個年度文件
for year in range(start_year, end_year + 1):
    file_name = f'data_{year}.csv'
    if os.path.exists(file_name):
        print(f"讀取 {file_name}")
        yearly_data = pd.read_csv(file_name, encoding='utf-8-sig')
        all_data.append(yearly_data)
    else:
        print(f"找不到 {file_name}，跳過")

# 檢查是否有任何數據文件被讀取
if not all_data:
    print("找不到任何數據文件，請確保數據文件存在")
    exit()

# 合併所有年度的數據
combined_data = pd.concat(all_data, ignore_index=True)

# 保存合併後的數據為CSV
combined_data.to_csv('data_1999_to_2024.csv', index=False, encoding='utf-8-sig')

# 保存合併後的數據為JSON
combined_data.to_json('data_1999_to_2024.json', orient='records', force_ascii=False)

print("1999年至2024年的數據已保存為CSV和JSON格式")
