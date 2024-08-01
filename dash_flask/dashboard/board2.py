import os
import dash
import traceback
from dash import html
import base64

# 創建 Dash 應用
app2 = dash.Dash(__name__, requests_pathname_prefix='/dashboard/app2/')
app2.title = '太陽能系統評估'

# 顯示選定圖像的函數
def display_image(image_path, width='80%', height='auto'):
    try:
        # 打印圖像路徑來檢查是否正確
        print(f"嘗試顯示圖像: {image_path}")
        
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')
        return html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': width, 'height': height})
    except Exception as e:
        return html.Div(f"無法顯示圖片: {str(e)}")

# 假設 button_texts 是一個列表，包含按鈕的文本和圖像路徑
button_texts = [
    ("統計摘要", os.path.join('dash_flask/image/data.png')),
    ("盒鬚圖", os.path.join('dash_flask/image/boxplot_no_outliers.png')),
    ("每日平均日照時數", os.path.join('dash_flask/image/line_H.png')),
    ("平均日照時數常態分佈", os.path.join('dash_flask/image/normaldistribution_H.png')),
    ("每日平均太陽輻射量", os.path.join('dash_flask/image/line_R.png')),
    ("平均日射量常態分佈", os.path.join('dash_flask/image/normaldistribution_R.png')),
    ("熱力圖", os.path.join('dash_flask/image/heatmap.png')),
    ("線性回歸", os.path.join('dash_flask/image/linear_regression.png')),
]

# 創建主要的 layout
app2.layout = html.Div([
    html.Div([
        html.H1("太陽能系統評估計算"),
        html.Div([
            html.Div([
                html.Button(text, id=f'button-{idx}', n_clicks=0) for idx, (text, _) in enumerate(button_texts)
            ], style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='image-display', style={'textAlign': 'center'})
        ]),
        html.Button("太陽能系統評估計算", id='calc-button', n_clicks=0),
        html.Div(id='calculator-output', style={'textAlign': 'center'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100vh'})
])

# 回調函數來更新圖像
@app2.callback(
    dash.dependencies.Output('image-display', 'children'),
    [dash.dependencies.Input(f'button-{idx}', 'n_clicks') for idx, _ in enumerate(button_texts)]
)
def update_image(*args):
    try:
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'button-0'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id.startswith('button-'):
            idx = int(button_id.split('-')[1])
            text, path = button_texts[idx]

            # 根據按鈕文本設定圖像大小
            if text == "統計摘要":
                return display_image(path, width='100%', height='auto')
            elif text == "每日平均日照時數":
                return display_image(path, width='60%', height='auto')
            elif text == "每日平均太陽輻射量":
                return display_image(path, width='60%', height='auto')
            else:
                return display_image(path)
    except Exception as e:
        traceback.print_exc()
        return html.Div(f"圖片顯示出現錯誤: {str(e)}")

if __name__ == '__main__':
    app2.run_server(host='127.0.0.1', port=8056, debug=False)
