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

# 找出年份和月份的選單定位
year_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]')))  # 使用XPath定位年份選單
month_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Month"]')))  # 使用XPath定位月份選單

# 打開年份選單並選擇1999年
year_dropdown.click()
time.sleep(1)  # 確保下拉選單打開
year_option = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Year"]/option[text()="1999"]')))
year_option.click()

# 打開月份選單並選擇1月
month_dropdown.click()
time.sleep(1)  # 確保下拉選單打開
month_option = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Month"]/option[text()="1"]')))
month_option.click()

# 顯式等待表格加載完成
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
time.sleep(3)  # 追加等待時間確保數據完全加載

# 使用pandas讀取HTML表格
tables = pd.read_html(browser.page_source)

# 關閉瀏覽器
browser.quit()

# 假設我們需要的是第一個表格
df = tables[0]

# 打印抓取到的數據
print(df)

# 保存為CSV
df.to_csv('data_1999_01.csv', index=False, encoding='utf-8-sig')

# 保存為JSON
df.to_json('data_1999_01.json', orient='records', force_ascii=False)

print("1999年1月的數據已保存為CSV和JSON格式")
