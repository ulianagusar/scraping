
import os
import csv


directory = '/Users/ulanagusar/Desktop/selenium/urls_from_bbc'

csv_filename = 'bbc_link3.csv'

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['query', 'link'])

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            # Extract the file base name without extension
            query = os.path.splitext(filename)[0]
            # Open each text file for reading
            with open(os.path.join(directory, filename), 'r') as text_file:
                # Read each line in the file
                for line in text_file:
                    if line.startswith('[') and line.endswith(']'):
                        # Remove the brackets and split by comma
                        links = line[1:-1].split(', ')
                        for link in links:
                            # Remove the single quotes and extra whitespace
                            clean_link = link.strip().strip("'")
                            if clean_link:  # Ensure the link is not empty
                                writer.writerow([query, clean_link])
                    else:
                        clean_link = line.strip()
                        if clean_link:
                            writer.writerow([query, clean_link])