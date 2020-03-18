import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from slack_client import slacker

URL = 'https://www.mohfw.gov.in/'
response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
extract_ith_row = lambda i: extract_contents(soup.find_all('tr')[i].find_all('td')) 

header = extract_contents(soup.tr.find_all('th'))

stats = []
all_rows = soup.find_all('tr')
for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    if stat:
        if len(stat) == 5:
            # last row
            stat = ['', *stat]
        stats.append(stat)

table = tabulate(stats, headers=header, tablefmt='psql')
slack_text = f'Please find CoronaVirus Summary for India below:\n```{table}```'

slacker()(slack_text)
