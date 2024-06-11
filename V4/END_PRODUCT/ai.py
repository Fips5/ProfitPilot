import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

SMA = 3
LMA = 15

EXCEL_FILE_PATH = r"C:\Users\David\Desktop\Pilot\END_PRODUCT\price.xlsx"

def update_excel_and_save_to_j(data):
    try:
        workbook = openpyxl.load_workbook(EXCEL_FILE_PATH)
        sheet = workbook.active
        sheet.delete_rows(1, sheet.max_row)
        for item in data:
            next_row = sheet.max_row + 1
            sheet.cell(row=next_row, column=1, value=item["timestamp"])
            sheet.cell(row=next_row, column=2, value=item["price"])
        workbook.save(EXCEL_FILE_PATH)
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

def plot_predictions(df, predictions, title='Stock Price Prediction using Neural Network'):
    plt.figure(figsize=(16, 6))
    plt.plot(df.index[-len(predictions):], df['Close'].iloc[-len(predictions):].values, label='Actual Prices', linewidth=2)
    plt.plot(df.index[-len(predictions):], predictions, label='Predicted Prices', linestyle='--')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Load data and calculate SMA, LMA
df = pd.read_excel(EXCEL_FILE_PATH, names=['Date', 'Close'])
df['SMA'] = df['Close'].rolling(SMA).mean()
df['LMA'] = df['Close'].rolling(LMA).mean()

# Drop NaN values
df.dropna(inplace=True)

# Features and target
features = df[['Close', 'SMA', 'LMA']]
target = df['Close'].shift(-1)  # Predicting the next day's closing price

# Normalize features and target
scaler = MinMaxScaler()
features_normalized = scaler.fit_transform(features)
target_normalized = scaler.fit_transform(target.values.reshape(-1, 1))

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features_normalized, target_normalized, test_size=0.2, random_state=42)

# Build the neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(features.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
loss = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Data: {loss}')

# Make predictions
predictions = model.predict(X_test)

# De-normalize predictions
predictions_denormalized = scaler.inverse_transform(predictions)

# Plot predictions
plot_predictions(df, predictions_denormalized)
