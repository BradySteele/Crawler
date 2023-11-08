import requests
from bs4 import BeautifulSoup
import json

# List of URLs to scrape
urls = [
#Plug in URL
]

# Function to scrape HTML content from a URL
def scrape_html_content(url):
    headers = {
        'User-Agent': 'SET AS NEEDED'
    }

    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    
    if response.status_code == 200:
        return response.content
    return None

# Function to parse HTML content using Beautiful Soup
def parse_html(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = {}

        # Extract text from paragraphs (<p> tags)
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        parsed_data['paragraphs'] = paragraphs

        # Extract text from list items (<li> tags)
        list_items = [li.get_text(strip=True) for li in soup.find_all('li')]
        parsed_data['list_items'] = list_items

        # Extract text from ordered lists (<ol> tags)
        ordered_lists = [ol.get_text(strip=True) for ol in soup.find_all('ol')]
        parsed_data['ordered_lists'] = ordered_lists

        # Extract text from heading elements (<h1>, <h2>, etc.)
        headings = []
        for i in range(1, 7):  # Check h1 to h6 tags
            heading_tags = [heading.get_text(strip=True) for heading in soup.find_all(f'h{i}')]
            headings.extend(heading_tags)
        parsed_data['headings'] = headings

        # Refine text extraction from div elements
        divs = [div.get_text(separator=' ', strip=True) for div in soup.find_all('div')]
        # Filter out duplicates using a set
        unique_divs = list(set(divs))
        # Remove empty strings from the list
        unique_divs = [text for text in unique_divs if text]
        parsed_data['divs'] = unique_divs

        specific_span = soup.find('span', id='specific-id')
        if specific_span:
            parsed_data['specific_span'] = specific_span.get_text()

        # Extract text from nested <p> tags within a specific <div> with class 'static_content'
        div_content = soup.find('div', class_='static_content')
        if div_content:
            nested_paragraphs = [p.get_text(strip=True) for p in div_content.find_all('p') if p.get_text(strip=True)]
            parsed_data['nested_paragraphs'] = nested_paragraphs

        return parsed_data
    return None

data_by_url = {}

# Iterate through the URLs, scrape, parse, and save the data
for url in urls:
    html_content = scrape_html_content(url)
    parsed_data = parse_html(html_content)

    if parsed_data:
        # Check for duplicate content in divs
        div_content = parsed_data['divs']
        unique_div_content = list(set(div_content))
        parsed_data['divs'] = unique_div_content

        # Store parsed data under the URL key in the data_by_url dictionary
        data_by_url[url] = parsed_data
        print(f"Data parsed for URL: {url}")
    else:
        print(f"Failed to parse data for URL: {url}")

# Save all data to a single JSON file
output_file = "data_by_url.json"
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data_by_url, file, indent=4)
print(f"All data saved to {output_file}")
