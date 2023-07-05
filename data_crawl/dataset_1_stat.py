import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service

# Declare browser
s = Service('chromedriver.exe')
main_driver = webdriver.Chrome(service=s)

# Open URL
main_driver.get('https://1xbet.whoscored.com/Statistics')

players = {
    "names" : [],
    "clubs" : [],
    "ages" : []
}
cnt = 0
tmp_len = 0
while True:
    top_players_box = main_driver.find_element(By.ID, 'top-player-stats')
    player_links = top_players_box.find_elements(By.XPATH, "//a[@class='player-link']")
    links = []
    for player_link in player_links:
        links.append(player_link.get_attribute('href'))

    player_names = [span.text for span in top_players_box.find_elements(By.XPATH, "//span[contains(@class, 'iconize')]")]
    player_clubs = [span.text[0:-1] for span in top_players_box.find_elements(By.CLASS_NAME, "team-name") if span.text != '']
    player_age_and_role = [span.text for span in top_players_box.find_elements(By.XPATH, "//div[@id='top-player-stats']//span[@class='player-meta-data']") if span.text != '']
    player_ages = [player_age_and_role[i] for i in range(len(player_age_and_role)) if i % 2 == 0]
    players['names'] = players['names'] + player_names
    players['clubs'] = players['clubs'] + player_clubs
    players['ages'] = players['ages'] + player_ages

    for link in links:
        sub_driver = webdriver.Chrome(service=s)
        sub_driver.get(link)

        # Defensive
        defensive_page = sub_driver.find_element(By.XPATH, "//a[text()='Defensive']")
        defensive_page.click()
        sleep(5)
        defensive_titles = [el.text for el in defensive_page.find_elements(By.XPATH, '//thead[@id="player-table-statistics-head"]//th') if el.text != ''][1:]
        Drb_index = defensive_titles.index("Drb")
        defensive_titles.pop(Drb_index)
        for defensive_title in defensive_titles:
            if defensive_title not in players:
                players[defensive_title] = []

        defensive_stats = [el.text for el in defensive_page.find_elements(By.XPATH, '//tbody//strong') if el.text != ''][1:]
        defensive_stats.pop(Drb_index)
        for i in range(len(defensive_titles)): 
            players[defensive_titles[i]].append(defensive_stats[i])
        
        tmp_len = len(players[defensive_titles[0]])


        # Offensive
        offensive_page = sub_driver.find_element(By.XPATH, "//a[text()='Offensive']")
        offensive_page.click()
        sleep(5)
        offensive_titles = [el.text for el in offensive_page.find_elements(By.XPATH, '//thead[@id="player-table-statistics-head"]//th') if el.text != ''][3:-1]
        for offensive_title in offensive_titles:
            if offensive_title not in players:
                players[offensive_title] = []

        offensive_stats = [el.text for el in offensive_page.find_elements(By.XPATH, '//tbody//strong') if el.text != ''][3:-1]
        for i in range(len(offensive_titles)):
            players[offensive_titles[i]].append(offensive_stats[i])
        
        
        # Passing
        passing_page = sub_driver.find_element(By.XPATH, "//a[text()='Passing']")
        passing_page.click()
        sleep(5)
        passing_titles = [el.text for el in passing_page.find_elements(By.XPATH, '//thead[@id="player-table-statistics-head"]//th') if el.text != ''][3:-1]
        for passing_title in passing_titles:
            if passing_title not in players:
                players[passing_title] = []

        passing_stats = [el.text for el in passing_page.find_elements(By.XPATH, '//tbody//strong') if el.text != ''][3:-1]
        for i in range(len(passing_titles)):
            if len(players[passing_titles[i]]) < tmp_len:
                players[passing_titles[i]].append(passing_stats[i])


        # Summary
        summary_page = sub_driver.find_elements(By.XPATH, "//a[text()='Summary']")[-1]
        summary_page.click()
        sleep(5)
        summary_titles = [el.text for el in summary_page.find_elements(By.XPATH, '//thead[@id="player-table-statistics-head"]//th') if el.text != ''][-3:-1]
        for summary_title in summary_titles:
            if summary_title not in players:
                players[summary_title] = []

        summary_stats = [el.text for el in summary_page.find_elements(By.XPATH, '//tbody//strong') if el.text != ''][-3:-1]
        for i in range(len(summary_titles)):
            players[summary_titles[i]].append(summary_stats[i])

        sub_driver.close()

    next_button = main_driver.find_elements(By.XPATH, '//a[@id="next"]')[-1]
    next_button.click()
    sleep(10)
    cnt += 1
    if cnt == 150:
        break

df = pd.DataFrame.from_dict(players, orient='index').transpose()
df.to_csv('data.csv', index=False, encoding='utf-8')

    