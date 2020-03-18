import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from slack_client import slacker

URL = 'https://www.mohfw.gov.in/'
AVOID_HEADERS = ['Total Confirmed cases', '(', ')']

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

def shorten_header(h):
    for kw in AVOID_HEADERS:
        h = h.replace(kw, '')
    return h


if __name__ == '__main__':
    
    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    header = extract_contents(soup.tr.find_all('th'))
    short_header = [shorten_header(h) for h in header]

    stats = []
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            if len(stat) == 5:
                # last row
                stat = ['', *stat]
            stats.append(stat)
    
    table = tabulate(stats, headers=short_header, tablefmt='psql')
    slack_text = f'Please find CoronaVirus Summary for India below:\n```{table}```'
    
    slacker()(slack_text)
