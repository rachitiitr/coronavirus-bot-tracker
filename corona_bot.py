import requests
from bs4 import BeautifulSoup

URL = 'https://www.mohfw.gov.in/'
response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

header = extract_contents(soup.tr.find_all('th'))
stats = extract_contents(soup.find_all('tr')[-1].find_all('td'))
