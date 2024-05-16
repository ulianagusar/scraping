
import datetime

import csv
import requests
from bs4 import BeautifulSoup
import json

# замість "Follow East of England news on Facebook" ми вказуєм "8STOP8" 
#, щоб потім по цьому обрізати текст , бо те , що йде далі містить текст 
#з нижніх полів сайту ( контакти ,соцмережі і тп )



# витягуєм html з сайту та переводим у json
def get_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

     
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        json_string = script_tag.string if script_tag else ""
        data = json.loads(json_string) if json_string else {}
        return data
    except requests.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return ""
    
# збирає зміст полів 'text' , тут використовується словник ,
# бо ця структура зберігає порядок і не зберігає дублікати 
#( None , яке ми кладем у значення випадку ніякого сенсу не несе , 
#бо потім ми всеодно збираємо лише ключі )
def fetch_text_from_url(data):
   
    try:

        unique_sentences = {}

        def extract_text(data):
            if isinstance(data, dict):
                for key, value in data.items():
                    if key == 'text':
                        if "Follow East of England news on Facebook" not in value:
                            unique_sentences[value.strip()] = None
                        else:
                            unique_sentences["8STOP8"] = None
                    else:
                        extract_text(value)
            elif isinstance(data, list):
                for item in data:
                    extract_text(item)

        extract_text(data)

        full_text = " ".join(unique_sentences.keys())
        return full_text.strip()
    except requests.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return ""
# обрізаєм текст
def extract_text_before_stop(text, stop_word='8STOP8'):
    stop_index = text.find(stop_word)
    if stop_index != -1:
        return text[:stop_index]
    return text

# витягуєм заголовок
def extract_headline(data, article_id, has_articles):
    key = f'@"news",{"\"articles\"," if has_articles else ""}"{article_id}",'  
    contents = data['props']['pageProps']['page'][key]['contents']
    
    for content in contents:
            if content['type'] == 'headline':
                text = content['model']['blocks'][0]['model']['text']
                return text
    return None
# витягуєм час
def extract_timestamp(data, article_id, has_articles):
    key = f'@"news",{"\"articles\"," if has_articles else ""}"{article_id}",'
    
    contents = data['props']['pageProps']['page'][key]['contents']
    
    for content in contents:
        if content['type'] == 'timestamp':
            timestamp = content['model']['timestamp']
            date_time = datetime.datetime.utcfromtimestamp(timestamp / 1000)
            return date_time
    return None

        

input_csv = 'cleaned_bbc_link.csv'
output_csv = 'bbc_articles2.csv'
n = 0
with open(input_csv, mode='r', newline='') as infile, \
     open(output_csv, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fields = reader.fieldnames + ['title'] + ['date'] + ['extracted_text'] 
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()

    for row in reader:
        n = n+1 
        # для відслідковування прогресу
        print(n)
        url = row['link'].strip()
        article_id = url.split('/')[-1]
        has_articles = "articles" in url
        data = get_data(url)

        if data != "":
            try  :
                  dat = extract_timestamp(data, article_id ,has_articles)
                  head  = extract_headline(data, article_id, has_articles)
            except Exception as e :
                  dat = ""
                  head = ""
                  print(e)
            full_text = fetch_text_from_url(data)
            extracted_text = extract_text_before_stop(full_text)
        else:
            extracted_text = ""
            dat = ""
        print(head)
        print(dat)
        row['title'] = head
        row['extracted_text'] = extracted_text
        row['date'] = dat
        writer.writerow(row)



