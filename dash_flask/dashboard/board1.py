from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import os
from sqlalchemy import create_engine
import df

# 初始化 Dash 應用
app1 = Dash(__name__, requests_pathname_prefix='/dashboard/app1/')
app1.title = '臺灣太陽能系統評估表單'

# 確定目錄設置正確，使用相對路徑設置文件路徑
current_dir = os.getcwd()
target_dir = os.path.join(current_dir, 'dash_web')

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
print("DataFrame columns:", df.columns)

# 去除欄位名稱中的空白字符
df.columns = df.columns.str.strip()
print("Cleaned DataFrame columns:", df.columns)

# 確認必需的欄位是否存在
required_columns = ['站名', '平均氣溫', '絕對最高氣溫', '絕對最低氣溫',
                    '總日照時數h', '總日射量MJ/ m2', 'Year', 'Month', '行政區']
for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' is missing from the DataFrame")

# 設定應用的佈局
app1.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in df['站名'].unique()],
                value='桃園市',  # 根據你的數據選擇一個默認值
                id='xaxis-column'
            ),
            dcc.RadioItems(
                options=[{'label': 'Linear', 'value': 'Linear'}, {'label': 'Log', 'value': 'Log'}],
                value='Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in df['站名'].unique()],
                value='桃園市',  # 根據你的數據選擇一個默認值
                id='yaxis-column'
            ),
            dcc.RadioItems(
                options=[{'label': 'Linear', 'value': 'Linear'}, {'label': 'Log', 'value': 'Log'}],
                value='Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='indicator-graphic'),
    dcc.Slider(
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=None,
        id='year--slider',
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
])

@app1.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value')
)
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    dff = df[df['Year'] == year_value]

    # 檢查選擇的欄位是否在 DataFrame 中
    if xaxis_column_name not in dff['站名'].values:
        raise ValueError(f"'{xaxis_column_name}' is not a valid indicator name for x-axis")
    if yaxis_column_name not in dff['站名'].values:
        raise ValueError(f"'{yaxis_column_name}' is not a valid indicator name for y-axis")

    xValue = dff[dff['站名'] == xaxis_column_name]['總日照時數h']
    yValue = dff[dff['站名'] == yaxis_column_name]['總日射量MJ/ m2']
    hoverValue = dff[dff['站名'] == yaxis_column_name]['行政區']
    
    fig = px.scatter(
        x=xValue,
        y=yValue,
        hover_name=hoverValue
    )
    
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest'
    )
    
    fig.update_xaxes(
        title=xaxis_column_name,
        type='linear' if xaxis_type == 'Linear' else 'log'
    )
    
    fig.update_yaxes(
        title=yaxis_column_name,
        type='linear' if yaxis_type == 'Linear' else 'log'
    )
    
    return fig

# 運行應用
# if __name__ == '__main__':
#     app1.run_server(debug=True)
