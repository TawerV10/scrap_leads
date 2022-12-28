from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import time
import csv

url = 'https://www.merchantgenius.io'

def get_dates_txt():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    alla = soup.find_all('a')
    count = 1
    for a in alla:
        link = url + a.get('href')
        if '/shop/date/' in link:
            with open('dates.txt', 'a', encoding='utf-8') as file:
                file.write(f'{link}\n')

            print(count, link)
        count += 1

def get_all_links():
    dates = []
    with open('dates.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            dates.append(line)

    length = len(dates)
    correct_links = []
    dates = dates[383:]
    current_num = 384
    for i, date in enumerate(dates):
        print(f'{i + current_num}/{length} - {date.strip()}')

        r = requests.get(date.strip())
        soup = BeautifulSoup(r.text, 'lxml')
        alla = soup.find_all('a')

        count = 1

        for a in alla:
            link = url + a.get('href')
            if '/shop/url/' in link and link not in correct_links:
                with open('links4.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{link}\n')

                correct_links.append(link)
                count += 1

        print(count)
        time.sleep(0.5)

def clear_links():
    links = []
    with open('all_links.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            links.append(line)

    print('Len', len(links))

    unique_links = list(dict.fromkeys(links))
    print('Len', len(unique_links))

    df = pd.DataFrame(unique_links)
    print(df.shape)

    df.to_csv('data_links.csv', index=False)

df = pd.read_csv('data_links.csv') # 1167369
print(df.shape)

lst = df.values.tolist()
link = lst[0][0].replace('\n', '')
print(link)

r = requests.get(link)
soup = BeautifulSoup(r.text, 'lxml')

try:
    name = soup.find('div', class_='blogContent').find('h2').text.strip()
except:
    name = ''
try:
    website = soup.find('div', class_='blogContent').find('span', class_='typeText').find('a').get('href').strip()
except:
    website = ''
try:
    description = soup.find('div', class_='blogContent bcTop').text.strip()
except:
    description = ''

with open('data.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        name, website, description
    ])