import time
from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
players = []

def convert_to_numeric(value):
    suffixes = {
        'K': 1e3,
        'M': 1e6,
        'B': 1e9
    }
    pattern = r'(\d+\.?\d*)([KMB])'
    match = re.match(pattern, value)
    if match:
        number = float(match.group(1))
        suffix = match.group(2)
        return number * suffixes[suffix]
    else:
        return value

start_page = int(input ('Type start page: '))
amount_page = int(input ('Type amount page: '))
while (amount_page > 0):
    r = requests.get('https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&pn%5B0%5D=27&pn%5B1%5D=25&pn%5B2%5D=23&pn%5B3%5D=22&pn%5B4%5D=21&pn%5B5%5D=20&col=vl&sort=desc&offset={}'.format(str((start_page-1)*60)),headers=headers)
    tree = html.fromstring(r.content)
    player_container = tree.xpath('//table/tbody')[0]
    player_names = [el.text for el in player_container.xpath('./tr/td[2]/a[1]/div')]
    player_ages = [el.text for el in player_container.xpath('./tr/td[3]')]
    player_links = player_container.xpath('./tr/td[2]/a[1]/@href')

    for i in range(len(player_links)):
        player = {

        }
        player['name'] = player_names[i]
        player['age'] = player_ages[i]
        link = "https://sofifa.com" + player_links[i]

        r = requests.get(link, headers=headers)
        tree = html.fromstring(r.content)
        li_element = tree.xpath("//li[label='Contract valid until']")[0]
        feature = (li_element.xpath('./label')[0].text)
        contract_valid_until = (li_element.xpath(".//text()")[1])
        player[feature] = contract_valid_until
        main_info = tree.xpath('//section/div/div')
        for info in main_info:
            feature = info.xpath("./div[@class='sub']")[0].text
            rating = ''
            if info.text:
                rating = info.text[1:]
                cleaned_string = ''.join([char for char in rating if ord(char) < 128])
                rating = convert_to_numeric(cleaned_string)
            else:
                rating = info.xpath('./span')[0].text
            player[feature] = rating 

        categories = tree.xpath("//div[@class='center'][2]//div[@class='card']//ul")[0:-1]
        for category in categories:
            stats = category.xpath("./li")
            for stat in stats:
                feature = stat.xpath('./span')[1].text
                rating = stat.xpath('./span')[0].text
                player[feature] = rating

        players.append(player)
    amount_page -= 1
    start_page += 1


print(players)
df = pd.DataFrame(players)
df.to_csv('attack.csv', index=False, encoding='utf-8')

# get_info_player('https://sofifa.com' + '/player/230621/gianluigi-donnarumma/230037/')