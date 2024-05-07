import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print('RUNNING AI NEWS ANALYSIS')

article_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\news_extrction\output.json'
output_file_path = r'C:\Users\David\Documents\ProfitPilot\V5\AI_news_anlysis\output.json'
def clear_file(file_path):
    try:
        with open(file_path, "w") as json_file:
            print('***FILE CEARED***')
    except Exception as e:
        print(f"Error creating the JSON file: {e}")

clear_file(output_file_path)


with open(article_file_path, 'r') as f:
    articles_data = json.load(f)

analyzer = SentimentIntensityAnalyzer()

sentiment_results = {}

for symbol, articles in articles_data.items():
    if symbol not in sentiment_results:
        sentiment_results[symbol] = {}

    for link, text in articles.items():
        sentiment_score = analyzer.polarity_scores(text)['compound']

        if sentiment_score >= 0.05:
            conclusion = 'positive'
        elif sentiment_score <= -0.05:
            conclusion = 'negative'
        else:
            conclusion = 'neutral'

        sentiment_results[symbol][link] = {'score': sentiment_score, 'conclusion': conclusion}

with open(output_file_path, 'w') as outfile:
    json.dump(sentiment_results, outfile, indent=4)

print("Sentiment results saved to output JSON file.")
