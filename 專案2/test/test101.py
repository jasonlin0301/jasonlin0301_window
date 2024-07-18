import pandas as pd

# Load the CSV file
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\processed_data_v2_with_daily_averages.csv'
data = pd.read_csv(file_path)

# Ensure the numeric columns are correctly parsed
data['總日照時數h'] = pd.to_numeric(data['總日照時數h'], errors='coerce')
data['總日射量MJ/ m2'] = pd.to_numeric(data['總日射量MJ/ m2'], errors='coerce')
data['平均每日日照時數'] = pd.to_numeric(data['平均每日日照時數'], errors='coerce')
data['平均每日日射量'] = pd.to_numeric(data['平均每日日射量'], errors='coerce')

# Function to calculate annual averages for each region
def calculate_annual_averages(region):
    # Filter data for the specified region
    filtered_data = data[data['行政區'] == region]
    
    # Group by year and calculate average daily sunshine hours and solar radiation
    annual_averages = filtered_data.groupby('Year').agg({
        '平均每日日照時數': 'mean',
        '平均每日日射量': 'mean'
    }).reset_index()
    
    return annual_averages

# Get the unique regions
regions = data['行政區'].unique()

# Create an empty DataFrame to store the results
results = pd.DataFrame()

# Calculate annual averages for each region and concatenate the results
for region in regions:
    annual_averages = calculate_annual_averages(region)
    annual_averages['行政區'] = region
    results = pd.concat([results, annual_averages], ignore_index=True)

# Save the results to a new CSV file with UTF-8 encoding and BOM for Excel compatibility
output_file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\temp_solar\annual_averages.csv'
results.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"Results saved at: {output_file_path}")
