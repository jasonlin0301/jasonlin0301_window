from dash import Dash,html,dcc,Input,Output,callback,dash_table
import data
import pandas as pd

app2 = Dash(__name__,requests_pathname_prefix='/dashboard/app2/')

areas = [tup[0] for tup in data.get_areas()]
print(areas[0])

app2.layout = html.Div([
    dcc.Dropdown(
       options = areas,
       value = areas[0],
       id='areas'
    ),
    html.Hr(),
    dash_table.DataTable(id='sites_table')
])

@app2.callback(
    Output('sites_table','data'),
    Input('areas','value')
)
def selected_area(areas_value):
    content = data.get_snaOfArea(area=areas_value)
    df = pd.DataFrame(content)
    df.columns = ['站名','平均氣溫','絕對最高氣溫','絕對最低氣溫','總日照時數h','總日射量MJ/m2','Year','Month','行政區']
    return df.to_dict('records')

    