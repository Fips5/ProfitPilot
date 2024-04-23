import json 
import pandas as pd
import numpy as np

with open(r'C:\Users\David\Documents\ProfitPilot\V5\fundamentl_extraction\one_co.json', 'r') as file:
    data = json.load(file)
    
score_bord = []

for item in data:
    for company, info in item.items():
        df = pd.DataFrame(info, index=[0])
        print(f"DataFrame for {company}:")
        print(df)
        score = 0


