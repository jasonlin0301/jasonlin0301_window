import json
import requests
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import List, Dict, Any

def download_json():
    url = "https://raw.githubusercontent.com/LanvisWei/MLproject_Solar_Irradiance/main/weather_data.json"  

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"連線失敗: {e}")
    else:
        all_data = res.json()
        return all_data

class WeatherInfo(BaseModel):
    站名: str
    平均氣溫: str
    絕對最高氣溫: str
    絕對最高氣溫日期: str
    絕對最低氣溫: float
    絕對最低氣溫日期: str
    平均相對濕度: str
    總降雨量: str
    平均風速: str
    最多風向: str
    總日照時數: str
    總日射量: str
    平均地溫_0cm: str
    平均地溫_5cm: str
    平均地溫_10cm: str
    平均地溫_20cm: str
    平均地溫_50cm: str
    平均地溫_100cm: str
    Year: int
    Month: int

    @field_validator('平均氣溫', '絕對最高氣溫', '平均相對濕度', '總降雨量', '平均風速', '總日照時數', '總日射量',
                     '平均地溫_0cm', '平均地溫_5cm', '平均地溫_10cm', '平均地溫_20cm', '平均地溫_50cm', '平均地溫_100cm',
                     mode='before')
    def parse_float(cls, value):
        try:
            return float(value)
        except ValueError:
            return value

class WeatherData(BaseModel):
    data: List[WeatherInfo]

def load_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    weather_data = WeatherData(data=all_data)
    return [info.dict() for info in weather_data.data]

class FilterData:
    @staticmethod
    def get_selected_info(station_name: str, data: List[Dict[str, Any]]) -> WeatherInfo:
        filtered_data = list(filter(lambda item: item['站名'] == station_name, data))
        if not filtered_data:
            raise ValueError(f"站名為 '{station_name}' 的數據不存在")
       
if __name__ == "__main__":
    file_path = "weather_data.json"
    data = load_data(file_path)