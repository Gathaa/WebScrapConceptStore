from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.petitfute.com/d567-region-de-tunis/c1168-shopping-mode-cadeaux/c1176-cadeaux/c1240-concept-store"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find all <h3> elements with class 'mb-0'
    h3_elements = soup.find_all('h3', class_='mb-0')
    
    # Find phone numbers
    address_divs = soup.find_all('div', class_='adresse-listing article-text')
    phone_numbers = []
    
    for address_div in address_divs:
        a_tags = address_div.find_all('a')
        for a_tag in a_tags:
            if 'tel:' in a_tag.get('href', '') or any(char.isdigit() for char in a_tag.text):
                phone_numbers.append(a_tag.text.strip())
    
    # Now, write the names and phone numbers to a CSV file
    csv_filename = 'names_and_phone_numbers.csv'
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header row
        csv_writer.writerow(['Name', 'Phone Number'])
        
        # Write rows with names and corresponding phone numbers
        for i in range(min(len(h3_elements), len(phone_numbers))):
            csv_writer.writerow([h3_elements[i].text.strip(), phone_numbers[i]])
            
    print(f"Data has been successfully exported to {csv_filename}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
