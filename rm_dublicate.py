import csv


input_csv = '/Users/ulanagusar/Desktop/selenium/bbc_scrab.csv'
output_csv = 'bbc_article.csv'


seen_links = set()


with open(input_csv, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    fields = reader.fieldnames


    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()


        for row in reader:
            link = row['link'].strip()
            if link not in seen_links:
                seen_links.add(link)  
                writer.writerow(row)  


