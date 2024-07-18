import pandas as pd
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Load the data
file_path = r'C:\Users\lanvi\OneDrive\Documents\github\MLproject_Solar_Irradiance\test\processed_data.csv'
data = pd.read_csv(file_path)

# Function to convert values to float, replace non-numeric values with NaN
def to_float(value):
    try:
        return float(value)
    except ValueError:
        return np.nan

# Apply the conversion function to the relevant columns
columns_to_check = ['總日照時數h', '總日射量MJ/ m2', '絕對最高氣溫']
for col in columns_to_check:
    data[col] = data[col].apply(to_float)

# Drop rows with NaN values
data = data.dropna(subset=columns_to_check)

# Define the independent and dependent variables
X = data[['總日照時數h', '總日射量MJ/ m2']]
Y = data['絕對最高氣溫']

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Fit the PLS regression model
pls = PLSRegression(n_components=2)
pls.fit(X_train, Y_train)

# Predict and evaluate the model
Y_pred = pls.predict(X_test)
r2 = r2_score(Y_test, Y_pred)

print(f'R-squared: {r2}')
