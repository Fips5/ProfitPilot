import json
import pandas as pd

# Define file paths
buy_orders_path = r'C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\buy_orders.json'
close_orders_path = r'C:\Users\David\Documents\ProfitPilot\V5\Live_Price_Analysis\close_orders.json'
excel_output_path = r'C:\Users\David\Documents\ProfitPilot\V5\raport_construction\6.11-7.11.xlsx'

# Step 1: Read the JSON data from the buy orders file
with open(buy_orders_path, 'r') as file:
    buy_orders_data = json.load(file)

# Step 2: Read the JSON data from the close orders file
with open(close_orders_path, 'r') as file:
    close_orders_data = json.load(file)

# Step 3: Convert the JSON data into pandas DataFrames
buy_orders_df = pd.DataFrame(buy_orders_data)
close_orders_df = pd.DataFrame(close_orders_data)

# Step 4: Merge the DataFrames on 'id' and 'symbol'
merged_df = pd.merge(buy_orders_df, close_orders_df, on=['id', 'symbol'], suffixes=('_open', '_close'))

# Step 5: Rename and reorder the columns appropriately
merged_df = merged_df.rename(columns={
    'id': 'ID',
    'symbol': 'SYMBOL',
    'timestamp_open': 'OPEN',
    'timestamp_close': 'CLOSE'
})[['ID', 'SYMBOL', 'OPEN', 'CLOSE']]

# Step 6: Sort the DataFrame by 'ID' and 'SYMBOL'
merged_df.sort_values(by=['ID', 'SYMBOL'], inplace=True)

# Step 7: Write the DataFrames to an Excel file with separate sheets
with pd.ExcelWriter(excel_output_path) as writer:
    merged_df.to_excel(writer, sheet_name='fin orders', index=False)

print(f"Data successfully written to {excel_output_path}")
