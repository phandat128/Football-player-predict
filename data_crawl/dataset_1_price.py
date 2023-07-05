import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

data = []
os.environ['PATH'] += "C:/Users/ASUS/Downloads/chromedriver"
driver = webdriver.Chrome()
driver.implicitly_wait(10)


def get_info_in_one_page(_position):
    items = driver.find_element(By.CLASS_NAME, "items")
    items = items.find_elements(By.CLASS_NAME, "hauptlink")

    _count = 0
    _temp = []
    for item in items:
        content = item.find_element(By.TAG_NAME, "a").get_attribute("innerText")
        print(content)
        _count ^= 1
        _temp.append(content)
        if _count == 0:
            _temp.append(_position)
            data.append(_temp)
            _temp = []


root_url = 'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/0/galerie/0?' \
           'ausrichtung={}&spielerposition_id=alle&altersklasse=alle&jahrgang=0&land_id=0&kontinent_id=0&' \
           'yt0=Show&page={}'

query = {
    'Goalkeeper': 'Torwart',
    'Defender': 'Abwehr',
    'Midfielder': 'Mittelfeld',
    'Forward': 'Sturm'
}

for position, value in query.items():
    for page in range(20):
        driver.get(root_url.format(value, page+1))
        get_info_in_one_page(position)

lines = []
for name, price, position in data:
    _price = int(float(price[1:-1]))
    if price[-1] == 'm':
        _price *= 1000000
    elif price[-1] == 'k':
        _price *= 1000

    line = name + "<fff>" + position + "<fff>" + str(_price)
    lines.append(line)

with open("./price.txt", "w", encoding='utf-8') as f:
    f.write('\n'.join(lines))

