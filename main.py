import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score
from xgboost import XGBRegressor
import category_encoders as ce

df = pd.read_csv('housePrice.csv')
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except (ValueError, TypeError):
        pass

df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
df['Area'] = df['Area'].fillna(df['Area'].median())

bin_cols = ['Room', 'Parking', 'Warehouse', 'Elevator'] 
df[bin_cols] = df[bin_cols].fillna(df[bin_cols].mode().iloc[0])

df = df.drop(columns=['Price'])
df['Price(USD)'] = pd.to_numeric(df['Price(USD)'], errors='coerce')
df['Price(USD)'] = df['Price(USD)'].fillna(df['Price(USD)'].median())
df['Price(USD)'] = np.log1p(df['Price(USD)'])

df['Address'] = df['Address'].fillna('Unknown').astype(str)

X = df[['Area', 'Room', 'Parking', 'Warehouse', 'Elevator', 'Address']]
y = df['Price(USD)']

encoder = ce.TargetEncoder(cols=['Address'])
X_encoded = encoder.fit_transform(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
