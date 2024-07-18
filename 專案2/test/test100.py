import pandas as pd

# Load the uploaded CSV file
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2.csv'
data = pd.read_csv(file_path)

# Calculate the number of days in each month
data['days_in_month'] = pd.to_datetime(data[['Year', 'Month']].assign(DAY=1)).dt.daysinmonth

# Convert the columns to numeric, forcing errors to NaN
data['總日照時數h'] = pd.to_numeric(data['總日照時數h'], errors='coerce')
data['總日射量MJ/ m2'] = pd.to_numeric(data['總日射量MJ/ m2'], errors='coerce')

# Calculate average daily sunshine hours and solar radiation
data['平均每日日照時數'] = data['總日照時數h'] / data['days_in_month']
data['平均每日日射量'] = data['總日射量MJ/ m2'] / data['days_in_month']

# Save the modified dataframe to a new CSV file with UTF-8 encoding
new_file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2_with_daily_averages.csv'
data.to_csv(new_file_path, index=False, encoding='utf-8')

print(f"New file saved at: {new_file_path}")
