from bs4 import BeautifulSoup
import requests
import pandas as pd
url = "https://www.petitfute.com/d567-region-de-tunis/c1168-shopping-mode-cadeaux/c1176-cadeaux/c1240-concept-store"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    h3_elements = [h3.text.strip() for h3 in soup.find_all('h3', class_='mb-0')]
    q_elements = [q.text.strip() for q in soup.find_all('q', class_='col fst-italic')]
    address_divs = soup.find_all('div', class_='adresse-listing article-text')
    phone_numbers = []
    for address_div in address_divs:
        a_tags = address_div.find_all('a')
        for a_tag in a_tags:
            if 'tel:' in a_tag.get('href', '') or any(char.isdigit() for char in a_tag.text):
                phone_numbers.append(a_tag.text.strip())
    location_divs = soup.find_all('div', class_='col-12 col-sm')
    locations = [location.text.strip() for location in location_divs]
    data = {
        'Name': h3_elements,
        'Description': q_elements,
        'Phone Number': phone_numbers,
        'Location': locations
    }
    df = pd.DataFrame(data)
    excel_filename = 'ConceptStore.xlsx'
    df.to_excel(excel_filename, index=False)
    print(f"Data has been successfully exported to {excel_filename}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
