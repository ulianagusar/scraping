import csv
import json


with open('bbc_article.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    
    articles_json = {}
    
    for row in reader:
        article_json = {
            "query": row['query'],
            "link": row['link'],
            "date": row['date'],
            "extracted_text": row['extracted_text']
        }
        
        articles_json[row['title']] = article_json

with open('bbc_articles.json', 'w', encoding='utf-8') as json_file:
    json.dump(articles_json, json_file, ensure_ascii=False, indent=4)

