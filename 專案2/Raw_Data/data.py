import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 初始化啟動chrome webdriver
driverpath = r"D:\github\MLproject_Solar_Irradiance\chromedriver-win64\chromedriver.exe"  # 瀏覽器驅動程式路徑
service = Service(driverpath)

# 設置Chrome選項以啟用無頭模式
options = Options()
options.add_argument('--headless')  # 啟用無頭模式
options.add_argument('--disable-gpu')  # 如果你使用的是Windows系統，這一步是必要的
options.add_argument('--no-sandbox')  # 對於Linux系統可能是必要的
options.add_argument('--disable-dev-shm-usage')  # 共享內存設置

browser = webdriver.Chrome(service=service, options=options)  # 模擬瀏覽器
wait = WebDriverWait(browser, 10)  # 設置顯式等待時間

url = 'https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html'
browser.get(url)  # 以get方式進入網站
time.sleep(3)  # 網站有loading時間

# 初始化總存儲數據的列表
all_years_data = []

# 遍歷1999年至2024年
for year in range(1999, 2025):
    # 找出年份和月份的選單定位
    year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]')))  # 使用XPath定位年份選單
    month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Month"]')))  # 使用XPath定位月份選單

    # 打開年份選單並選擇對應年份
    year_dropdown.click()
    time.sleep(1)  # 確保下拉選單打開
    year_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Year"]/option[text()="{year}"]')))
    year_option.click()

    # 初始化存儲每年數據的列表
    yearly_data = []

    # 遍歷每年的12個月
    for month in range(1, 13):
        # 打開月份選單並選擇對應月份
        month_dropdown.click()
        time.sleep(1)  # 確保下拉選單打開

        # 檢查月份選項是否存在
        try:
            month_option = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Month"]/option[text()="{month}"]')))
            month_option.click()
        except:
            print(f"{year}年{month}月的數據不可用，跳過")
            continue

        # 顯式等待表格加載完成
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
            time.sleep(3)  # 追加等待時間確保數據完全加載
        except:
            print(f"{year}年{month}月的數據表格未加載，跳過")
            continue

        # 使用pandas讀取HTML表格
        try:
            tables = pd.read_html(browser.page_source)
            df = tables[0]
        except ValueError:
            print(f"{year}年{month}月的表格數據讀取失敗，跳過")
            continue

        # 添加年份和月份列
        df['Year'] = year
        df['Month'] = month

        # 將數據添加到年度列表中
        yearly_data.append(df)

    # 合併每年的數據
    if yearly_data:
        yearly_df = pd.concat(yearly_data, ignore_index=True)

        # 打印每年抓取到的數據
        print(f"{year}年的數據：")
        print(yearly_df)

        # 保存每年的數據為CSV
        yearly_df.to_csv(f'data_{year}.csv', index=False, encoding='utf-8-sig')

        # 保存每年的數據為JSON
        yearly_df.to_json(f'data_{year}.json', orient='records', force_ascii=False)

        # 將每年的數據添加到總列表中
        all_years_data.append(yearly_df)

# 關閉瀏覽器
browser.quit()

# 合併所有年份的數據
if all_years_data:
    final_df = pd.concat(all_years_data, ignore_index=True)

    # 打印所有年份抓取到的數據
    print("所有年份的數據：")
    print(final_df)

    # 保存所有年份的數據為CSV
    final_df.to_csv('_data_1999_to_2024.csv', index=False, encoding='utf-8-sig')

    # 保存所有年份的數據為JSON
    final_df.to_json('_data_1999_to_2024.json', orient='records', force_ascii=False)

    print("1999年至2024年的數據已保存為CSV和JSON格式")
