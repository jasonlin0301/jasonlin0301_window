import pandas as pd
import os

# 初始化存储所有数据的列表
all_data = []

# 指定年份范围
start_year = 1999
end_year = 2023  # 结束年份修改为2023

# 遍历每个年度文件
for year in range(start_year, end_year + 1):
    file_name = f'data_{year}.csv'
    if os.path.exists(file_name):
        print(f"读取 {file_name}")
        yearly_data = pd.read_csv(file_name, encoding='utf-8-sig')
        all_data.append(yearly_data)
    else:
        print(f"找不到 {file_name}，跳过")

# 检查是否有任何数据文件被读取
if not all_data:
    print("找不到任何数据文件，请确保数据文件存在")
    exit()

# 合并所有年度的数据
combined_data = pd.concat(all_data, ignore_index=True)

# 保存合并后的数据为CSV
combined_data.to_csv('_data_1999_to_2023.csv', index=False, encoding='utf-8-sig')

# 保存合并后的数据为JSON
combined_data.to_json('_data_1999_to_2023.json', orient='records', force_ascii=False)

print("1999年至2023年的数据已保存为CSV和JSON格式")
