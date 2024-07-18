> 文長、想看重點直接捲到最後。

# theory 

### 等效日射小時（Equivalent Sun Hours, ESH）和峰值日射小時（Peak Sun Hours, PSH）是與太陽能系統設計相關的重要概念。


> 等效日射小時（Equivalent Sun Hours, ESH）

> 來源：
> * Solarmazd​ ([SOALRMAZD](https://solarmazd.com/peak-sun-hours-psh-what-does-it-mean-and-how-to-estimate-it/))​
> * RenewableWise​ ([Renewablewise](https://www.renewablewise.com/peak-sun-hours-calculator/))​
> * Palmetto​ ([Palmetto](https://palmetto.com/solar/what-are-peak-sun-hours))​
> * Dot Watts​ ([Dot Watts®](https://palmetto.com/solar/what-are-peak-sun-hours))

等效日射小時表示一天內太陽能輻射量轉化為在1千瓦每平方公尺（1kW/m²）條件下工作的總時間。這個指標有助於評估太陽能系統在特定地區的性能。等效日射小時的計算公式如下：

# **ESH = DailySolarIrradiation (kWh/m²/day) / (1kW/m²)**

### 峰值日射小時（Peak Sun Hours, PSH）

峰值日射小時與等效日射小時相似，通常被視為同義詞。它指的是一天中等效於太陽能電池板在最大功率下運行的總小時數。PSH也使用日均太陽能輻射量來計算，兩者的公式是一樣的，因此在實際應用中，**ESH** 和 **PSH** 通常**可以互換使用**。

* 如果某地一天接收到 6 kWh/m² 的太陽能量，則該地的 ESH 為 6 小時，意味著該地接收到相當於 6 小時的 1000 W/m² 的陽光。

* Daily Energy Production=Power Rating of Panel×ESH

    - 每日能量產出=太陽能板功率×ESH

* example : If you have a 200-watt solar panel and the ESH in your location is 5 hours. Daily Energy Production=200 W×5 hours=1,000 Wh or 1 kWh.

    - 如果你有一塊 200 瓦的太陽能板，而你所在位置的 ESH 為 5 小時，每日能量產出=200 W×5 小時=1000 Wh 或 1 kWh

# 資料來源

> 交通部中央氣象署 首頁>生活>農業>農業觀測>全部觀測網月資料

## [日射量資料](https://www.cwa.gov.tw/V8/C/L/Agri/Agri_month_All.html)
​
> 使用selenium及webdriver-manager建立虛擬webviewer抓取java資料庫資料並建立.csv及.json #但後來只用CSV，並下載對應的瀏覽器driver

```python

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

```

[csv](./Raw_Data/_data_1999_to_2024.csv)
```csv
 站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month
 茶改場,15.3,25.5,1/23,7.6,1/15,82.6,73.5,4.0,*,63.3,*176.74,*16.4,*16.4,*16.8,*17.2,*17.9,*19.5,1999,1 
 桃園農改,16.1,23.3,1/19,8.8,1/15,81.0,65.5,5.4,45.0,65.7,175.6,17.8,17.5,17.3,18.0,18.9,19.9,1999,1
 五峰站,11.9,21.1,1/14,3.5,1/15,91.3,118.5,0.4,135.0,88.6,227.5,14.6,14.6,14.9,15.3,15.9,17.1,1999,1
 苗栗農改,15.7,25.7,1/19,8.6,1/15,95.9,39.5,2.4,22.5,XXX,XXX,17.8,18.1,18.3,18.5,18.9,19.9,1999,1
 台中農改,17.1,27.4,1/19,10.7,1/15,83.2,16.0,2.5,360.0,166.4,237.07,19.6,19.9,20.3,20.6,21.0,21.8,1999,1
```

## 主要設備

建立一個完整的太陽能蓄電系統需要以下主要設備和相應的價格範圍(USD)：

### 太陽能板 (Solar Panels)

* Monocrystalline Panels: 單價約為每瓦 $0.60 至 $1.00，400W 的單板價格約為 $250-$360​ <[Solar](https://www.solar.com/learn/solar-panel-cost/)><[GoGreenSolar.com](https://www.gogreensolar.com/pages/solar-components-101)>​​
* Polycrystalline Panels: 單價約為每瓦 $0.50 至 $0.80，300W 的單板價格約為 $150-$240。
* Thin-Film Panels: 單價約為每瓦 $0.40 至 $0.70，適用於特定應用場景如柔性安裝​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

    - 單晶矽太陽能板的大小和主流功率:
        > 目前，主流的單晶矽太陽能板功率為400W左右。這類太陽能板的尺寸一般約為1.7平方米（1.7m²），具體尺寸因製造商而異，但大多數在1.6米×1米左右。

    - 屋頂面積和可安裝容量計算
        >台灣30坪的樓地板面積約為99平方米（1坪約等於3.3平方米）。假設屋頂面積與樓地板面積相當，即約99平方米。

    - 每片400W的單晶矽太陽能板大約需要1.7平方米的安裝面積。要計算可以安裝的總容量，首先需要確定可用的實際屋頂面積，考慮到可能的遮蔽物（如通風口、屋頂突出物等）和維護通道。假設**可用面積約為70%**：

        > 可用屋頂面積：
        99m²×0.70=69.3m²
        99平方米×0.70=69.3平方米

        > 每片太陽能板的安裝面積為1.7平方米，計算可安裝的太陽能板數量：
        69.3m²/1.7m²(片)≈40.76(片)
        取整數，最多可安裝40片太陽能板。

        > 每片太陽能板功率為400W，總容量為：
        40(片)×400(W/片)=16000W，即16kW。

### 太陽能架設與安裝設備 (Racking and Mounting Equipment)

* Roof Mounts: 單個系統價格約為 $1000 至 $3000。
* Ground Mounts: 單個系統價格約為 $2000 至 $4000​ <[EnergySage](https://www.energysage.com/solar/solar-panel-setup-what-you-need-to-know/)​​><[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>。

### 逆變器 (Inverters)

* String Inverters: 單價約為 $1000 至 $2500，壽命約 10-15 年。
* Microinverters: 單價約為每瓦 $1.00 至 $1.20，系統總價約為 $3000-$5000，壽命約 25 年<[GoGreenSolar.com](https://www.gogreensolar.com/pages/solar-components-101)><[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

### 蓄電池 (Batteries)

* 鉛酸電池: 每千瓦時價格約為 $200 至 $300。
* 鋰離子電池: 每千瓦時價格約為 $400 至 $700，10kWh 系統價格約為 $4000-$7000​ <[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>​。

### 電力調節器 (Charge Controllers)

* MPPT Controllers: 單價約為 $100 至 $500，根據系統規模和功能不同​ <[ShopSolar.com](https://shopsolarkits.com/blogs/learning-center/solar-panel-system-equipment)​>​。

### 斷路器 (Disconnect Switch)

* 單價約為 $50 至 $200，用於安全維護和緊急關閉系統​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

### 勞力與技術費用

* 安裝太陽能系統的人工成本約為 $3000 至 $7000，根據系統規模和複雜性而異。專業電工的費用可能更高​ <[Solar](https://www.solar.com/learn/solar-panel-cost/)>​。

#### 施工時間

建置一個完整的家庭太陽能系統一般需要 1-3 週，包括現場勘查、系統設計、安裝和測試​ <[Fenice Energy](https://blog.feniceenergy.com/building-a-complete-solar-electric-system-components-and-setup/)>​。

## 計算太陽能系統的產生度數

預設的可達成條件：
* EHS (Equivalent Sun Hours) = 2.5 小時
* 系統容量 = 16000W (16kW)
* 系統效率 = 80%

計算公式：

P=Sxη×ESH/E
- S 是系統容量(KW)
- E 是每日能量需求（kWh/day）
- η 是系統效率

16000W×2.5hr×0.80=32000Wh，可以產生32度電。

## 台灣平均家戶用電量

根據台灣電力公司（Taipower）和其他相關資料，台灣家庭的平均每月用電量約為300至400度電​ (ShopSolar.com)​​ (Fenice Energy)​。我們取中間值350度電來做進一步分析。

> 計算年用電量和每日用電量

平均每月用電量=350kWh
平均每年用電量=350kWh×12月=4200kWh
平均每日用電量=4200kWhx365天≈11.5kWh，11.5度電

32 > 11.5， Z大於B，只是沒有錢，我也不住透天。
所以不是日照量的問題，是大樓跟公寓的住宅密集度的問題....(?

## 由html label新增行政區

> F12 謝謝你

```pyhton

    import pandas as pd
    import json
    from bs4 import BeautifulSoup

    # HTML原始碼
    html_code = """
    <select id="ST" name="st" size="1"><optgroup label="新北市" id="新北市"><option value="72AI40">桃改樹林分場</option><option value="82A750">茶改北部分場</option></optgroup><optgroup label="桃園市" id="桃園市"><option value="72C440">桃園農改</option><option value="82C160">茶改場</option><option value="A2C560">農工中心</option></optgroup><optgroup label="新竹縣" id="新竹縣"><option value="72D080">桃改五峰分場</option><option value="72D680">桃改新埔分場</option></optgroup><optgroup label="苗栗縣" id="苗栗縣"><option value="B2E890">畜試北區分所</option><option value="K2E710">苗改生物防治研究中心</option><option value="K2E360">苗栗農改</option></optgroup><optgroup label="臺中市" id="臺中市"><option value="K2F750">種苗繁殖</option><option value="G2F820">農業試驗所</option></optgroup><optgroup label="彰化縣" id="彰化縣"><option value="CAG100">王功漁港</option><option value="72G600">臺中農改</option></optgroup><optgroup label="南投縣" id="南投縣"><option value="72HA00">中改埔里分場</option><option value="E2HA20">林試畢祿溪站</option><option value="U2HA40">臺大內茅埔</option><option value="U2HA30">臺大和社</option><option value="U2H480">臺大溪頭</option><option value="U2HA50">臺大竹山</option><option value="82H320">茶改中部分場</option><option value="82H840">茶改南部分場</option><option value="42HA10">萬大發電廠</option><option value="E2H360">蓮華池</option></optgroup><optgroup label="雲林縣" id="雲林縣"><option value="72K220">南改斗南分場</option><option value="12J990">口湖工作站</option><option value="E2K600">四湖植物園</option><option value="A2K360">水試臺西試驗場</option><option value="CAJ050">海口故事園區</option><option value="A2K630">臺大雲林校區</option><option value="V2K620">麥寮合作社</option></optgroup><optgroup label="嘉義市" id="嘉義市"><option value="G2L020">農試嘉義分所</option></optgroup><optgroup label="嘉義縣" id="嘉義縣"><option value="72M360">南改義竹分場</option><option value="72M700">南改鹿草分場</option><option value="CAL110">布袋國中</option><option value="G2M350">農試溪口農場</option></optgroup><optgroup label="臺南市" id="臺南市"><option value="72N240">七股研究中心</option><option value="CAN140">六官養殖協會</option><option value="CAN130">水試所海水繁養殖中心</option><option value="B2N890">畜試所</option><option value="A2N290">臺南蘭花園區</option><option value="72N100">臺南農改</option></optgroup><optgroup label="高雄市" id="高雄市"><option value="E2P980">林試六龜中心</option><option value="E2P990">林試扇平站</option><option value="G2P820">農試鳳山分所</option><option value="72V140">高改旗南分場</option></optgroup><optgroup label="屏東縣" id="屏東縣"><option value="CAQ030">崎峰國小</option><option value="12Q980">恆春工作站</option><option value="12Q970">東港工作站</option><option value="B2Q810">畜試南區分所</option><option value="72Q010">高雄農改</option></optgroup><optgroup label="宜蘭縣" id="宜蘭縣"><option value="B2U990">畜試東區分所</option><option value="72U480">花改蘭陽分場</option></optgroup><optgroup label="花蓮縣" id="花蓮縣"><option value="72T250">花蓮農改</option></optgroup><optgroup label="臺東縣" id="臺東縣"><option value="72S200">東改班鳩分場</option><option value="72S590">東改賓朗果園</option><option value="E2S980">林試太麻里1</option><option value="E2S960">林試太麻里2</option><option value="82S580">茶改東部分場</option></optgroup></select>
    """

    # 解析HTML
    soup = BeautifulSoup(html_code, 'html.parser')

    # 提取站名和對應的行政區
    district_mapping = {}
    for optgroup in soup.find_all('optgroup'):
        district = optgroup['label']
        for option in optgroup.find_all('option'):
            station = option.text
            district_mapping[station] = district

    # 手動添加未匹配的站名對應行政區
    # 因為政府機關兩邊頁面的名稱不同，只能手動。
    additional_mappings = {
        '五峰站': '新竹縣',
        '台中農改': '台中市',
        '雲林分場': '雲林縣',
        '義竹分場': '嘉義縣',
        '恆春畜試': '屏東縣',
        '蘭陽分場': '宜蘭縣',
        '斑鳩分場': '台東縣',
        '文山茶改': '台北市',
        '大湖分場': '苗栗縣',
        '新竹畜試': '新竹縣',
        '凍頂茶改': '南投縣',
        '魚池茶改': '南投縣',
        '嘉義農試': '嘉義縣',
        '旗南農改': '屏東縣',
        '鳳山農試': '高雄市',
        '臺東茶改': '台東縣',
        '賓朗果園': '屏東縣',
        '旗南分場': '屏東縣'
    }
    district_mapping.update(additional_mappings)

    # 讀取CSV文件
    csv_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2024.csv'
    csv_data = pd.read_csv(csv_file)

    # 讀取JSON文件
    json_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2024.json'
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # 添加行政區到CSV數據
    csv_data['行政區'] = csv_data['站名'].map(district_mapping)

    # 找出沒有匹配的站名
    unmatched_stations = csv_data[csv_data['行政區'].isna()]['站名'].unique()

    # 打印沒有匹配的站名
    print("未匹配的站名:")
    print(unmatched_stations)

    # 保存修改後的CSV文件
    csv_data.to_csv(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2024.csv', index=False)

    # 添加行政區到JSON數據
    for entry in json_data:
        station_name = entry.get('站名')
        entry['行政區'] = district_mapping.get(station_name, '')

    # 保存修改後的JSON文件
    with open(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2024.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


```

``` CSV

    站名,平均氣溫,絕對最高氣溫,絕對最高氣溫日期,絕對最低氣溫,絕對最低氣溫日期,平均相對濕度 %,總降雨量mm,平均風速m/s,最多風向,總日照時數h,總日射量MJ/ m2,平均地溫(0cm),平均地溫(5cm),平均地溫(10 cm),平均地溫(20 cm),平均地溫(50 cm),平均地溫(100 cm),Year,Month,行政區
    茶改場,15.3,25.5,1/23,7.6,1/15,82.6,73.5,4.0,*,63.3,*176.74,*16.4,*16.4,*16.8,*17.2,*17.9,*19.5,1999,1,桃園市
    桃園農改,16.1,23.3,1/19,8.8,1/15,81.0,65.5,5.4,45.0,65.7,175.6,17.8,17.5,17.3,18.0,18.9,19.9,1999,1,桃園市
    五峰站,11.9,21.1,1/14,3.5,1/15,91.3,118.5,0.4,135.0,88.6,227.5,14.6,14.6,14.9,15.3,15.9,17.1,1999,1,新竹縣
    苗栗農改,15.7,25.7,1/19,8.6,1/15,95.9,39.5,2.4,22.5,XXX,XXX,17.8,18.1,18.3,18.5,18.9,19.9,1999,1,苗栗縣
    台中農改,17.1,27.4,1/19,10.7,1/15,83.2,16.0,2.5,360.0,166.4,237.07,19.6,19.9,20.3,20.6,21.0,21.8,1999,1,台中市

```

# 敘述統計、盒鬚圖、折線圖、常態分佈圖、線性回歸 

### 統計值

```python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 檢查當前工作目錄
current_dir = os.getcwd()
print("Current Working Directory:", current_dir)

# 設定檔案路徑
file_path = os.path.join('..', 'temp_solar', 'processed_data_v2.csv')

# 字體設置
font_path = os.path.join('..', 'ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

df = pd.read_csv(file_path)

# 定義需要計算的欄位
columns_to_analyze = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']

# 初始化統計結果字典
stats_dict = {}
describe_dict = {}

# 計算每個欄位的統計量
for column in columns_to_analyze:
    d = pd.to_numeric(df[column], errors='coerce').dropna()
    stats = {
        '計數': d.count(),
        '最小值': d.min(),
        '最大值': d.max(),
        '最小值索引': d.idxmin(),
        '最大值索引': d.idxmax(),
        '10%分位數': d.quantile(0.1),
        '總和': d.sum(),
        '均值': d.mean(),
        '中位數': d.median(),
        '眾數': d.mode().tolist(),  # 眾數可以有多個值
        '方差': d.var(),
        '標準差': d.std(),
        '偏度': d.skew(),
        '峰度': d.kurt()
    }
    stats_dict[column] = stats
    describe_dict[column] = d.describe().to_dict()

# 將統計數據轉換為 DataFrame
stats_df = pd.DataFrame(stats_dict)
describe_df = pd.DataFrame(describe_dict)

# 創建圖表以顯示統計數據
fig, ax = plt.subplots(figsize=(15, 5))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=stats_df.values, colLabels=stats_df.columns, rowLabels=stats_df.index, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.1, 1.2)
plt.title('統計摘要', fontsize=16, fontproperties=font_properties)

# 設置表格內文字體
for key, cell in table.get_celld().items():
    cell.set_text_props(fontproperties=font_properties)

output_path = os.path.join('..', 'temp_solar', 'data.png')
plt.savefig(output_path, bbox_inches='tight')

# 顯示統計數據圖表
plt.show()
```

### 盒鬚圖

```python
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 檢查當前工作目錄
print("Current Working Directory:", os.getcwd())

# 設定工作目錄
os.chdir('..')
print("Updated Working Directory:", os.getcwd())

# 設定檔案路徑
file_path = os.path.join('temp_solar', 'processed_data_v2.csv')
data = pd.read_csv(file_path)

# 設定字體
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 選擇相關的數值列
numerical_cols = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫', '總日照時數h', '總日射量MJ/ m2']

# 刪除數值列中有缺失值的行
data_clean = data.dropna(subset=numerical_cols)

# 將數值列轉換為浮點型
data_clean[numerical_cols] = data_clean[numerical_cols].apply(pd.to_numeric, errors='coerce')

# 計算Q1（第25百分位）和Q3（第75百分位）
Q1 = data_clean[numerical_cols].quantile(0.25)
Q3 = data_clean[numerical_cols].quantile(0.75)

# 計算IQR（四分位距）
IQR = Q3 - Q1

# 過濾掉異常值
data_no_outliers = data_clean[~((data_clean[numerical_cols] < (Q1 - 1.5 * IQR)) | (data_clean[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 繪製盒鬚圖
plt.figure(figsize=(12, 8))
data_no_outliers.boxplot(column=numerical_cols)
plt.title('Box Plot of Numerical Columns (without outliers)', fontproperties=font_properties)
plt.xticks(rotation=45, fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)

# 儲存圖片
output_path = os.path.join('temp_solar', 'boxplot_no_outliers.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
```

### 折線圖

```python

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
print("Current Working Directory:", current_dir)
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')
print("Updated Working Directory:", os.getcwd())

# 讀取數據
file_path = os.path.join('temp_solar', 'annual_averages.csv')
data = pd.read_csv(file_path)

# 定義字體屬性
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 函數來可視化每個地區的年平均日照時數
def visualize_all_regions_sunshine_hours():
    regions = data['行政區'].unique()
    
    plt.figure(figsize=(15, 10))
    
    for region in regions:
        filtered_data = data[data['行政區'] == region]
        plt.plot(filtered_data['Year'], filtered_data['平均每日日照時數'], marker='o', linestyle='-', label=region)
    
    plt.title('Annual Average Daily Sunshine Hours for All Regions', fontproperties=font_properties)
    plt.xlabel('Year', fontproperties=font_properties)
    plt.ylabel('Average Daily Sunshine Hours (hours)', fontproperties=font_properties)
    plt.legend(prop=font_properties, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    
    output_path = os.path.join('temp_solar', 'line_H.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.show()

# 可視化所有地區的年平均日照時數
visualize_all_regions_sunshine_hours()
```

### 常態分佈圖

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import os

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
print("Current Working Directory:", current_dir)
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')
print("Updated Working Directory:", os.getcwd())

# 讀取數據
file_path = os.path.join('temp_solar', 'processed_data_v2_with_daily_averages.csv')
data = pd.read_csv(file_path)

# 定義字體屬性
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 清理 '總日照時數h' 列，移除非數字字符
data['總日照時數h'] = pd.to_numeric(data['總日照時數h'], errors='coerce')

# 移除 NaN 值
data_filtered = data['總日照時數h'].dropna()

# 計算IQR並移除異常值
Q1 = data_filtered.quantile(0.25)
Q3 = data_filtered.quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

data_no_outliers = data_filtered[(data_filtered >= lower_bound) & (data_filtered <= upper_bound)]

# 繪製常態分佈圖並存為PNG文件
plt.figure(figsize=(10, 6))
count, bins, ignored = plt.hist(data_no_outliers, 30, density=True, alpha=0.6, color='g', edgecolor='black')

mu, sigma = data_no_outliers.mean(), data_no_outliers.std()
best_fit_line = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
                 np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
plt.plot(bins, best_fit_line, '--', color='red')

plt.xlabel('總日照時數h', fontproperties=font_properties)
plt.ylabel('頻率', fontproperties=font_properties)
plt.title('去除異常值後的總日照時數常態分佈圖', fontproperties=font_properties)

plt.grid(True)
output_path = os.path.join('temp_solar', 'normaldistribution_H.png')
plt.savefig(output_path, bbox_inches='tight')
plt.show()
```

### 線性回歸 Y=日射量 X=平均溫度、最高溫度、最低溫度、日照時數

```python
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
print("Current Working Directory:", current_dir)
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')
print("Updated Working Directory:", os.getcwd())

# 讀取資料
file_path = os.path.join('temp_solar', 'processed_data_v2_with_daily_averages.csv')
data = pd.read_csv(file_path)

# 設定字體屬性
font_path = os.path.join('ChocolateClassicalSans-Regular.ttf')
font_properties = FontProperties(fname=font_path)

# 定義轉換函數，將值轉換為浮點數，並將非數字值替換為NaN
def to_float(value):
    try:
        if isinstance(value, str) and '*' in value:
            return float(value.replace('*', ''))
        return float(value)
    except ValueError:
        return np.nan

# 將轉換函數應用到相關的列
columns_to_check = ['平均氣溫', '總日照時數h', '總日射量MJ/ m2']
for col in columns_to_check:
    data[col] = data[col].apply(to_float)

# 刪除包含NaN值的行
data = data.dropna(subset=columns_to_check)

# 去除離散值（使用IQR法）
Q1 = data[columns_to_check].quantile(0.25)
Q3 = data[columns_to_check].quantile(0.75)
IQR = Q3 - Q1
data = data[~((data[columns_to_check] < (Q1 - 1.5 * IQR)) | (data[columns_to_check] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 再次檢查並刪除包含NaN值的行
data = data.dropna()

# 定義自變量和應變量
X = data[['平均氣溫', '總日照時數h']].values  # 使用平均氣溫和總日照時數作為自變量
Y = data['總日射量MJ/ m2'].values  # 依變量是總日射量

# 確認X和Y中沒有NaN值
assert not np.isnan(X).any(), "X contains NaN values"
assert not np.isnan(Y).any(), "Y contains NaN values"

# 將資料分成訓練集和測試集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

# 擬合線性回歸模型
linear_regressor = LinearRegression()
linear_regressor.fit(X_train, Y_train)

# 預測並評估模型
Y_pred = linear_regressor.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

print(f'均方誤差: {mse}')
print(f'R平方值: {r2}')

# 繪製結果圖
plt.scatter(Y_test, Y_pred, color='blue', label='實際值 vs 預測值')
plt.plot([Y_test.min(), Y_test.max()], [Y_test.min(), Y_test.max()], color='red', linewidth=2, label='理想預測')
plt.xlabel('實際總日射量', fontproperties=font_properties)
plt.ylabel('預測總日射量', fontproperties=font_properties)
plt.title('線性回歸: 總日射量 vs 平均氣溫和總日照時數', fontproperties=font_properties)
plt.legend(prop=font_properties)

# 在圖表上添加均方誤差和R平方值
plt.text(Y_test.min(), Y_test.max(), f'均方誤差: {mse:.2f}\nR平方值: {r2:.2f}', 
         fontsize=12, verticalalignment='top', fontproperties=font_properties)

output_path = os.path.join('temp_solar', 'linear_regression.png')
plt.savefig(output_path, bbox_inches='tight')

plt.show()
```

# Final window and calculator

### calculator.py

>MJ/m² 轉換為kW/m² 的公式：1 MJ/m² = 0.2778 kW/m²

```python
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')

# 讀取CSV資料
file_path = os.path.join('temp_solar', 'annual_averages.csv')
annual_averages_df = pd.read_csv(file_path)

# 定義太陽能系統相關常數
WATT_PER_PANEL = 400  # 每塊太陽能板的瓦數
PANEL_PRICE_RANGE = (250, 360)  # 每塊太陽能板的價格區間（美元）
USD_TO_TWD = 30  # 美元兌新台幣匯率
DAILY_ENERGY_THRESHOLD = 11  # 每日能量需求閾值（度）
SYSTEM_EFFICIENCY = 0.8  # 太陽能系統效率
AREA_PER_PANEL = 1.7  # 每塊太陽能板所需的面積（平方公尺）

# 其他設備價格範圍（美元）
ROOF_MOUNT_PRICE_RANGE = (1000, 3000)
GROUND_MOUNT_PRICE_RANGE = (2000, 4000)
STRING_INVERTER_PRICE_RANGE = (1000, 2500)
MICROINVERTER_PRICE_RANGE = (3000, 5000)
BATTERY_PRICE_RANGE = (4000, 7000)  # 鋰離子電池
CHARGE_CONTROLLER_PRICE_RANGE = (100, 500)
DISCONNECT_SWITCH_PRICE_RANGE = (50, 200)
LABOR_COST_RANGE = (3000, 7000)

# 定義根據樓地板面積計算每日預估發電量的函數
def calculate_daily_energy(floor_area_tsubo, esh):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    total_watt = num_panels * WATT_PER_PANEL
    daily_energy = total_watt * esh * SYSTEM_EFFICIENCY / 1000  # 轉換成度
    return daily_energy

# 定義根據樓地板面積預估安裝價格的函數
def estimate_installation_cost(floor_area_tsubo, roof_mount=True):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    panel_cost = num_panels * (sum(PANEL_PRICE_RANGE) / 2)
    
    mount_cost = sum(ROOF_MOUNT_PRICE_RANGE) / 2 if roof_mount else sum(GROUND_MOUNT_PRICE_RANGE) / 2
    inverter_cost = sum(STRING_INVERTER_PRICE_RANGE) / 2
    battery_cost = sum(BATTERY_PRICE_RANGE) / 2
    controller_cost = sum(CHARGE_CONTROLLER_PRICE_RANGE) / 2
    switch_cost = sum(DISCONNECT_SWITCH_PRICE_RANGE) / 2
    labor_cost = sum(LABOR_COST_RANGE) / 2
    
    total_cost_usd = panel_cost + mount_cost + inverter_cost + battery_cost + controller_cost + switch_cost + labor_cost
    total_cost_twd = total_cost_usd * USD_TO_TWD
    
    return total_cost_twd

# 定義建議是否安裝的函數
def suggest_installation(floor_area_tsubo, esh, roof_mount=True):
    daily_energy = calculate_daily_energy(floor_area_tsubo, esh)
    installation_cost = estimate_installation_cost(floor_area_tsubo, roof_mount)
    suggestion = "建議安裝" if daily_energy > DAILY_ENERGY_THRESHOLD else "不建議安裝"
    return suggestion, daily_energy, installation_cost

# 定義處理按鈕點擊的函數
def on_submit(region_var, floor_area_var, result_var):
    region = region_var.get()
    try:
        floor_area_tsubo = float(floor_area_var.get())
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的樓地板面積")
        return
    
    esh = annual_averages_df[annual_averages_df['行政區'] == region]['ESH'].mean()
    
    if esh is None or pd.isna(esh):
        messagebox.showerror("資料錯誤", "無法找到該區域的ESH資料")
        return
    
    suggestion, daily_energy, installation_cost = suggest_installation(floor_area_tsubo, esh)
    
    result_var.set(f"{suggestion}\n每日預估發電量: {daily_energy:.2f} 度\n預估安裝成本: {installation_cost:.2f} 新台幣")

# GUI 應用設定
def create_ui(window):
    # 建立視窗部件
    ttk.Label(window, text="選擇區域:").grid(column=0, row=0, padx=10, pady=10)
    region_var = tk.StringVar()
    region_combo = ttk.Combobox(window, textvariable=region_var)
    region_combo['values'] = annual_averages_df['行政區'].unique().tolist()
    region_combo.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(window, text="樓地板面積 (坪):").grid(column=0, row=1, padx=10, pady=10)
    floor_area_var = tk.StringVar()
    ttk.Entry(window, textvariable=floor_area_var).grid(column=1, row=1, padx=10, pady=10)

    result_var = tk.StringVar()
    ttk.Label(window, textvariable=result_var).grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    ttk.Button(window, text="提交", command=lambda: on_submit(region_var, floor_area_var, result_var)).grid(column=0, row=2, columnspan=2, padx=10, pady=10)

# # 測試函數
# if __name__ == '__main__':
#     root = tk.Tk()
#     root.title("太陽能系統安裝建議")
#     create_ui(root)
#     root.mainloop()

```

### window.py 主程式

```python
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import os
import calculator  # 確保已經有這個模組

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
print("Current Working Directory:", current_dir)
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')
print("Updated Working Directory:", os.getcwd())

# 從CSV加載數據
file_path = os.path.join('temp_solar', 'processed_data_v2.csv')
data = pd.read_csv(file_path)

# 顯示選定圖像的函數
def display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((800, 600))  # 調整圖像大小以適應窗口
    img = ImageTk.PhotoImage(image)
    img_label.config(image=img)
    img_label.image = img

# 創建主窗口
root = tk.Tk()
root.title("CSV查看器與圖片")

# 創建Treeview小部件
tree = ttk.Treeview(root)
tree["columns"] = list(data.columns)
tree["show"] = "headings"

for col in data.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor='center')

# 將數據添加到Treeview
for index, row in data.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(side="left", fill="y")

# 創建按鈕和圖像顯示的框架
frame = ttk.Frame(root)
frame.pack(side="right", fill="both", expand=True)

# 創建按鈕
button_texts = [
    ("統計摘要", os.path.join('temp_solar', 'data.png')),
    ("盒鬚圖", os.path.join('temp_solar', 'boxplot_no_outliers.png')),
    ("每日平均日照時數", os.path.join('temp_solar', 'line_H.png')),
    ("平均日照時數常態分佈", os.path.join('temp_solar', 'normaldistribution_H.png')),
    ("每日平均太陽輻射量", os.path.join('temp_solar', 'line_R.png')),
    ("平均日射量常態分佈", os.path.join('temp_solar', 'normaldistribution_R.png')),
    ("熱力圖", os.path.join('temp_solar', 'heatmap.png')),
    ("線性回歸", os.path.join('temp_solar', 'linear_regression.png')),
]

for text, path in button_texts:
    button = ttk.Button(frame, text=text, command=lambda p=path: display_image(p))
    button.pack(fill="x")

# 添加執行calculator的按鈕
def open_calculator():
    calc_window = tk.Toplevel(root)
    calc_window.title("太陽能系統評估工具")
    calculator.create_ui(calc_window)

calc_button = ttk.Button(frame, text="太陽能系統評估計算", command=open_calculator)
calc_button.pack(fill="x")

# 顯示圖像的標籤
img_label = ttk.Label(frame)
img_label.pack(fill="both", expand=True)

# 運行應用程序
root.mainloop()
```
![window](./螢幕擷取畫面%202024-07-18%20002159.png)
![calculator01](./螢幕擷取畫面%202024-07-18%20002313.png)![calculator02](./螢幕擷取畫面%202024-07-18%20002343.png)

> 主程式加載了整理過後的CSV、各項圖表、並增加了一個按鈕呼叫calculator計算器，計算的公式來源及預估金額之前已提過。

> 價格的部分來自北美跟歐洲，台灣安裝價格大概會在50%-70%不等，台灣沒有可查詢到的公開資訊。

> # 結論: 要不要裝設太陽能系統、最重要的因素是口袋深度，有很多錢就裝。沒有錢還是繼續用愛發電(笑)，但可支配樓地板面積足夠的話太陽能目前能自給自足並且還能賣多於的電給台電，收購價大約為每度10元左右。