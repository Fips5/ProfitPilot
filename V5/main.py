import json

with open(r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\output.json', 'r') as file:
    json_data = json.load(file)

sentiment_dict = {}

for company, articles in json_data.items():
    positive_count = 0
    negative_count = 0
    
    for article in articles.values():
        if article["conclusion"] == "positive":
            positive_count += 1
        elif article["conclusion"] == "negative":
            negative_count += 1

    if positive_count > negative_count:
        sentiment_dict[company] = 1  # Positive predominant
    elif negative_count > positive_count:
        sentiment_dict[company] = 0  # Negative predominant
    else:
        sentiment_dict[company] = 0.5  # Equal positive and negative counts

# Output the result
print(sentiment_dict)