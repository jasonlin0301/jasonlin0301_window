import dash
from dash import dcc, html
import pandas as pd
from PIL import Image
import base64
import calculator  # 確保已經有這個模組

# 假設 button_texts 是一個列表，包含按鈕的文本和圖像路徑
button_texts = [
    ("統計摘要", 'temp_solar/data.png'),
    ("盒鬚圖", 'temp_solar/boxplot_no_outliers.png'),
    ("每日平均日照時數", 'temp_solar/line_H.png'),
    ("平均日照時數常態分佈", 'temp_solar/normaldistribution_H.png'),
    ("每日平均太陽輻射量", 'temp_solar/line_R.png'),
    ("平均日射量常態分佈", 'temp_solar/normaldistribution_R.png'),
    ("熱力圖", 'temp_solar/heatmap.png'),
    ("線性回歸", 'temp_solar/linear_regression.png'),
]

# 創建 Dash 應用
app = dash.Dash(__name__)

# 加載數據
file_path = 'temp_solar/processed_data_v2.csv'
data = pd.read_csv(file_path)

# 設置顯示圖像的函數
def display_image(image_path):
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return f'data:image/png;base64,{encoded_image.decode()}'

# 創建主要的 layout
app.layout = html.Div([
    html.H1("CSV查看器與圖片"),
    
    # 創建 Treeview
    html.Div([
        dcc.TreeView(
            id='tree',
            columns=[{'name': col, 'id': col} for col in data.columns],
            data=[{'id': index, 'values': list(row)} for index, row in data.iterrows()]
        )
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    # 創建按鈕和圖像顯示框
    html.Div([
        html.Div([
            html.Button(text, id=f'button-{idx}', n_clicks=0) for idx, (text, _) in enumerate(button_texts)
        ]),
        html.Div(id='image-display')
    ], style={'width': '50%', 'display': 'inline-block'}),
    
    # 添加計算器按鈕
    html.Button("太陽能系統評估計算", id='calc-button', n_clicks=0),
    html.Div(id='calculator-output')
])

# 回調函數來更新圖像和計算器部分
@app.callback(
    dash.dependencies.Output('image-display', 'children'),
    [dash.dependencies.Input(f'button-{idx}', 'n_clicks') for idx, _ in enumerate(button_texts)]
)
def update_image(n_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'button-0'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id.startswith('button-'):
        idx = int(button_id.split('-')[1])
        path = button_texts[idx][1]
        return html.Img(src=display_image(path), style={'width': '80%', 'height': '80%'})

@app.callback(
    dash.dependencies.Output('calculator-output', 'children'),
    [dash.dependencies.Input('calc-button', 'n_clicks')]
)
def update_calculator(n_clicks):
    if n_clicks > 0:
        return calculator.create_ui()

if __name__ == '__main__':
    app.run_server(debug=True)
