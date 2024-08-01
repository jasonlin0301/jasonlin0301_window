from dash import html, dcc, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine

# 初始化 Dash 應用
app3 = dash.Dash(__name__, requests_pathname_prefix='/dashboard/app3/', external_stylesheets=[dbc.themes.BOOTSTRAP])
app3.title = '太陽能系統計算器'

# 連接到 PostgreSQL 資料庫
DATABASE_URL = "postgresql://tvdi_postgresql_etik_user:4jYKNZqoOCkdoHsQIdHBOiL27yixeBTM@dpg-cqhf92aju9rs738kbi8g-a.singapore-postgres.render.com/tvdi_postgresql_etik_o8g3"
engine = create_engine(DATABASE_URL)

# 讀取 SQL 資料
def load_data():
    query = "SELECT * FROM averages"
    df = pd.read_sql(query, engine)
    return df

# 讀取數據
dash_web_df = load_data()

# 定義太陽能系統相關常數
WATT_PER_PANEL = 400
PANEL_PRICE_RANGE = (250, 360)
USD_TO_TWD = 30
DAILY_ENERGY_THRESHOLD = 11
SYSTEM_EFFICIENCY = 0.8
AREA_PER_PANEL = 1.7

ROOF_MOUNT_PRICE_RANGE = (1000, 3000)
GROUND_MOUNT_PRICE_RANGE = (2000, 4000)
STRING_INVERTER_PRICE_RANGE = (1000, 2500)
MICROINVERTER_PRICE_RANGE = (3000, 5000)
BATTERY_PRICE_RANGE = (4000, 7000)
CHARGE_CONTROLLER_PRICE_RANGE = (100, 500)
DISCONNECT_SWITCH_PRICE_RANGE = (50, 200)
LABOR_COST_RANGE = (3000, 7000)

def calculate_daily_energy(floor_area_tsubo, esh):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    total_watt = num_panels * WATT_PER_PANEL
    daily_energy = total_watt * esh * SYSTEM_EFFICIENCY / 1000
    return daily_energy

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

def suggest_installation(floor_area_tsubo, esh, roof_mount=True):
    daily_energy = calculate_daily_energy(floor_area_tsubo, esh)
    installation_cost = estimate_installation_cost(floor_area_tsubo, roof_mount)
    suggestion = "建議安裝" if daily_energy > DAILY_ENERGY_THRESHOLD else "不建議安裝"
    return suggestion, daily_energy, installation_cost

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Button('首頁', id='home-button', n_clicks=0, className="btn btn-primary", style={'fontSize': 20}),
        ], width="auto", className="d-flex align-items-start mb-3")
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H1("太陽能系統評估計算", className="text-center mb-4", style={'fontSize': 36}),
        ], width=12)
    ], className="justify-content-center"),
    
    dbc.Row([
        dbc.Col([
            html.Label("選擇區域:", className="form-label", style={'fontSize': 20}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in dash_web_df['行政區'].unique()],
                value=dash_web_df['行政區'].unique()[0],
                style={'width': '100%'}
            ),
            html.Label("樓地板面積 (坪):", className="form-label mt-3", style={'fontSize': 20}),
            dcc.Input(
                id='floor-area-input',
                type='number',
                value=50,
                step=1,
                style={'width': '100%', 'fontSize': 20}
            ),
            html.Label("是否安裝屋頂架設?", className="form-label mt-3", style={'fontSize': 20}),
            dcc.RadioItems(
                id='roof-mount-radio',
                options=[
                    {'label': '是', 'value': True},
                    {'label': '否', 'value': False}
                ],
                value=True,
                inline=True,
                style={'fontSize': 20}
            ),
            html.Button('提交', id='submit-button', n_clicks=0, className="mt-3 btn btn-primary", style={'fontSize': 20}),
            html.Div(id='result-output', className="mt-4", style={'fontSize': 20})
        ], width=6, className="text-start")
    ], className="justify-content-center")
], fluid=True)

@app.callback(
    Output('result-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('region-dropdown', 'value'),
    State('floor-area-input', 'value'),
    State('roof-mount-radio', 'value')
)
def update_output(n_clicks, region, floor_area_tsubo, roof_mount):
    if n_clicks > 0:
        try:
            floor_area_tsubo = float(floor_area_tsubo)
            if 'ESH' not in dash_web_df.columns:
                return "資料錯誤: DataFrame 中缺少 'ESH' 列"
            
            esh = dash_web_df[dash_web_df['行政區'] == region]['ESH'].mean()
            
            if pd.isna(esh):
                return "資料錯誤: 無法找到該區域的 ESH 資料"
            
            suggestion, daily_energy, installation_cost = suggest_installation(floor_area_tsubo, esh, roof_mount)
            return (
                f"{suggestion}\n"
                f"每日預估發電量: {daily_energy:.2f} 度\n"
                f"預估安裝成本: {installation_cost:.2f} 新台幣"
            )
        except ValueError:
            return "輸入錯誤: 請輸入有效的樓地板面積"
    return ""

@app.callback(
    Output('home-button', 'n_clicks'),
    Input('home-button', 'n_clicks')
)
def go_home(n_clicks):
    if n_clicks > 0:
        return dash.no_update  # 用於觸發導航，根據實際需求修改此行

# 確保 `server` 屬性
app3.server = app3.server
