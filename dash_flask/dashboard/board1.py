import os
import dash
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
from sqlalchemy import create_engine

# 初始化 Dash 應用
app1 = Dash(__name__, requests_pathname_prefix='/dashboard/app1/')
app1.title = '臺灣太陽能系統評估表單'

# 確定目錄設置正確，使用相對路徑設置文件路徑
current_dir = os.getcwd()
target_dir = os.path.join(current_dir, 'dash_flask')

# 設置資料庫連線
db_url = 'postgresql://tvdi_postgresql_etik_user:4jYKNZqoOCkdoHsQIdHBOiL27yixeBTM@dpg-cqhf92aju9rs738kbi8g-a.singapore-postgres.render.com/tvdi_postgresql_etik_o8g3'
engine = create_engine(db_url)

# 假設您的表格名稱是 dash_web，以及要選取的欄位
query = "SELECT * FROM dash_web"

# 使用 Pandas 讀取資料
data = pd.read_sql(query, engine)

# 關閉資料庫連線
engine.dispose()

# 顯示 DataFrame 的欄位名稱
print("DataFrame columns:", data.columns)

# 去除欄位名稱中的空白字符
data.columns = data.columns.str.strip()
print("Cleaned DataFrame columns:", data.columns)

app1.layout = html.Div([
    dcc.Dropdown(
       options = year,
       value = year[0],
       id='year'
    ),
    html.Hr(),
    dash_table.DataTable(id='sites_table')
])
# #如果要連結2個dash,必需要加上app1
# @app1.callback(
#     Output('sites_table','data'),
#     Input('year','value')
# )
# def selected_area(year_value):
#     content = data.get_snaOfArea(area=year_value)
#     df = pd.DataFrame(content)
#     df.columns = ['站點名稱','總數','可借','可還','日期','狀態']
#     return df.to_dict('records')
