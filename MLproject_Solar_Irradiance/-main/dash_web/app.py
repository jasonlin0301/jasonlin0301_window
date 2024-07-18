import os
import pandas as pd
from PIL import Image
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# 檢查並設置當前工作目錄
current_dir = os.getcwd()
if os.path.basename(current_dir) != 'MLproject_Solar_Irradiance':
    os.chdir('..')

# 從CSV加載數據
file_path = os.path.join('temp_solar', 'processed_data_v2.csv')
data = pd.read_csv(file_path)

# 初始化 Dash 應用程序
app = dash.Dash(__name__)

# 定義應用程序的布局
app.layout = html.Div([
    html.H1("CSV查看器與圖片"),

    # 顯示數據的表格
    html.Div([
        html.H2("數據表格"),
        dcc.Graph(
            id='data-table',
            figure={
                'data': [{
                    'type': 'table',
                    'header': {
                        'values': data.columns
                    },
                    'cells': {
                        'values': data.values.T  # 轉置數據以正確顯示
                    }
                }]
            }
        )
    ]),

    # 顯示圖像的區域
    html.Div([
        html.H2("圖像顯示"),
        html.Div(id='image-display')
    ]),

    # 按鈕區域
    html.Div([
        html.H2("圖像選擇"),
        html.Div([
            html.Button("統計摘要", id='summary-button', n_clicks=0),
            html.Button("盒鬚圖", id='boxplot-button', n_clicks=0),
            html.Button("每日平均日照時數", id='line_H-button', n_clicks=0),
            html.Button("每日平均太陽輻射量", id='line_R-button', n_clicks=0),
            html.Button("熱力圖", id='heatmap-button', n_clicks=0),
            html.Button("線性回歸", id='linear_regression-button', n_clicks=0),
        ]),
    ]),

    # 太陽能系統評估計算按鈕
    html.Div([
        html.Button("太陽能系統評估計算", id='calculator-button', n_clicks=0),
    ]),

    # 隱藏的容器來保存按鈕點擊的狀態
    html.Div(id='button-states', style={'display': 'none'})
])

# 回調函式來更新圖像顯示
@app.callback(
    Output('image-display', 'children'),
    [
        Input('summary-button', 'n_clicks'),
        Input('boxplot-button', 'n_clicks'),
        Input('line_H-button', 'n_clicks'),
        Input('line_R-button', 'n_clicks'),
        Input('heatmap-button', 'n_clicks'),
        Input('linear_regression-button', 'n_clicks')
    ]
)
def update_image(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    image_path = None
    if button_id == 'summary-button':
        image_path = os.path.join('temp_solar', 'data.png')
    elif button_id == 'boxplot-button':
        image_path = os.path.join('temp_solar', 'boxplot_no_outliers.png')
    elif button_id == 'line_H-button':
        image_path = os.path.join('temp_solar', 'line_H.png')
    elif button_id == 'line_R-button':
        image_path = os.path.join('temp_solar', 'line_R.png')
    elif button_id == 'heatmap-button':
        image_path = os.path.join('temp_solar', 'heatmap.png')
    elif button_id == 'linear_regression-button':
        image_path = os.path.join('temp_solar', 'linear_regression.png')

    if image_path:
        image = Image.open(image_path)
        image.thumbnail((800, 600))
        encoded_image = image_to_base64(image)
        return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

    return html.Div()

# 處理太陽能系統評估計算按鈕的回調函式
@app.callback(
    Output('button-states', 'children'),
    [Input('calculator-button', 'n_clicks')]
)
def open_calculator(n_clicks):
    if n_clicks > 0:
        # 在這裡添加打開計算器的程式碼，例如顯示一個新的視窗或者跳轉到另一個頁面
        pass

if __name__ == '__main__':
    app.run_server(debug=True)
