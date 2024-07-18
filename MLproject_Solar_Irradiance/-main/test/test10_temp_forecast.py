import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from matplotlib.font_manager import FontProperties

# Load the data
# file_path = r'D:\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Convert all relevant columns to float
columns_to_convert = ['平均氣溫', '絕對最高氣溫', '絕對最低氣溫']
for col in columns_to_convert:
    data[col] = data[col].apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values in the relevant columns
data = data.dropna(subset=columns_to_convert)

# Remove outliers
def remove_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

# Assuming you want to remove outliers for all relevant columns
for col in columns_to_convert:
    data = remove_outliers(data, col)

# Load the custom font
# font_path = r'D:\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\ChocolateClassicalSans-Regular.ttf'
font_properties = FontProperties(fname=font_path)

# Plotting the data
plt.figure(figsize=(14, 7))

# Plot 平均氣溫
plt.plot(data['Year'], data['平均氣溫'], label='平均氣溫', color='blue', marker='o')
# Plot 絕對最高氣溫
plt.plot(data['Year'], data['絕對最高氣溫'], label='絕對最高氣溫', color='red', marker='o')
# Plot 絕對最低氣溫
plt.plot(data['Year'], data['絕對最低氣溫'], label='絕對最低氣溫', color='green', marker='o')

# Linear regression for trend prediction
def plot_trend(X, Y, label, color):
    X = X.values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, Y)
    trend = model.predict(X)
    plt.plot(data['Year'], trend, label=f'{label} 趨勢', linestyle='--', color=color)

# Plot trends
plot_trend(data['Year'], data['平均氣溫'], '平均氣溫', 'blue')
plot_trend(data['Year'], data['絕對最高氣溫'], '絕對最高氣溫', 'red')
plot_trend(data['Year'], data['絕對最低氣溫'], '絕對最低氣溫', 'green')

# Adding titles and labels
plt.title('溫度趨勢分析', fontproperties=font_properties)
plt.xlabel('年份', fontproperties=font_properties)
plt.ylabel('溫度 (°C)', fontproperties=font_properties)
plt.legend(prop=font_properties)
plt.grid(True)

# Show and save the plot
# plt.savefig(r'D:\github\MLproject_Solar_Irradiance\test\temperature_trends.png')
plt.savefig(r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\temperature_trends.png')
plt.show()
