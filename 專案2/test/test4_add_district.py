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
additional_mappings = {
    '五峰站': '新竹縣',
    '台中農改': '臺中市',
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
csv_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2023.csv'
csv_data = pd.read_csv(csv_file)

# 讀取JSON文件
json_file = r'D:\github\MLproject_Solar_Irradiance\test\_data_1999_to_2023.json'
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
csv_data.to_csv(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2023.csv', index=False)

# 添加行政區到JSON數據
for entry in json_data:
    station_name = entry.get('站名')
    entry['行政區'] = district_mapping.get(station_name, '')

# 保存修改後的JSON文件
with open(r'D:\github\MLproject_Solar_Irradiance\test\modified_data_1999_to_2023.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)
