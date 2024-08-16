import sys
import io
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

original_stdout = sys.stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# r = requests.get('https://liquipedia.net/brawlstars/Brawl_Stars_Championship/2024/Season_1/North_America/Monthly_Finals')
# soup = BeautifulSoup(r.content, 'html.parser')

# tournaments = soup.find_all('div', class_='navigation-not-searchable navbox')

# links = []

# for t in tournaments:
#     t = t.find_all('a', href=re.compile(r"^/brawlstars/Brawl_Stars_Championship/2024/Season_"))

#     for link in t:
#         links.append('https://liquipedia.net' + link['href'])

def scrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    matches = soup.find_all('div', class_='brkts-popup-body')

    modes = []
    maps = []

    bscores = []
    rscores = []

    fpicks = []

    b1picks = []
    b2picks = []
    b3picks = []
    r1picks = []
    r2picks = []
    r3picks = []

    b1bans = []
    b2bans = []
    b3bans = []
    r1bans = []
    r2bans = []
    r3bans = []

    for match in matches:
        #scrape bans and picks
        pickdata = []

        firstpicks = match.find_all('img', alt="First pick")

        if not firstpicks:
            continue

        for pick in firstpicks:
            data = pick['src']
            
            if data == "/commons/images/a/ab/Arrow_sans_left.svg":
                fpicks.append("Blue")
            else:
                fpicks.append("Red")

        scores = match.find_all('div', string=lambda text: text and text.strip().isdigit())
        scores = [x.get_text(strip=True) for x in scores]

        for i in range(len(scores)):
            if i % 2 == 0:
                bscores.append(scores[i])
            else:
                rscores.append(scores[i])

        pickdata = []

        bluepicks = match.find_all('div', class_='brkts-popup-side-color-blue')
        
        for pick in bluepicks:
            pick = pick.find_all('a', href=re.compile(r"^/brawlstars/"))

            for item in pick:
                pickdata.append(item['title'])

        n = len(pickdata)

        for i in range(n // 2):
            if i % 3 == 0:
                b1picks.append(pickdata[i])
            elif i % 3 == 1:
                b2picks.append(pickdata[i])
            else:
                b3picks.append(pickdata[i])

        for i in range(n // 2, n):
            if i % 3 == 0:
                b1bans.append(pickdata[i])
            elif i % 3 == 1:
                b2bans.append(pickdata[i])
            else:
                b3bans.append(pickdata[i])

        pickdata = []

        redpicks = match.find_all('div', class_="brkts-popup-side-color-red")
        
        for pick in redpicks:
            pick = pick.find_all('a', href=re.compile(r"^/brawlstars/"))

            for item in pick:
                pickdata.append(item['title'])
        
            n = len(pickdata)

        for i in range(n // 2):
            if i % 3 == 0:
                r1picks.append(pickdata[i])
            elif i % 3 == 1:
                r2picks.append(pickdata[i])
            else:
                r3picks.append(pickdata[i])

        for i in range(n // 2, n):
            if i % 3 == 0:
                r1bans.append(pickdata[i])
            elif i % 3 == 1:
                r2bans.append(pickdata[i])
            else:
                r3bans.append(pickdata[i])

        # scrape modes and maps
        mapsandmodes = match.find_all('div', class_='brkts-popup-body-element brkts-popup-body-game')

        for m1 in mapsandmodes:
            m1 = m1.find_all('div', class_="brkts-popup-spaced")
            m1 = [x for x in m1 if "brkts-popup-spaced-map-skip" not in x['class']]

            for m2 in m1:
                m2 = m2.find_all('a', href=re.compile(r"^/brawlstars/"))

                isMode = True

                for item in m2:
                    data = item['title']

                    if isMode:
                        modes.append(data)
                    else:
                        maps.append(data)

                    isMode = not isMode

    df = pd.DataFrame({'Mode': modes, 'Map': maps, 'Blue Score': bscores, 'Red Score': rscores, 'First': fpicks, 
                    'Blue Pick 1': b1picks, 'Blue Pick 2': b2picks, 'Blue Pick 3': b3picks, 
                    'Red Pick 1': r1picks, 'Red Pick 2': r2picks, 'Red Pick 3': r3picks, 
                    'Blue Ban 1': b1bans, 'Blue Ban 2': b2bans, 'Blue Ban 3': b3bans, 
                    'Red Ban 1': r1bans, 'Red Ban 2': r2bans, 'Red Ban 3': r3bans})

    return df

links = []

links.append('https://liquipedia.net/brawlstars/Esports_City_Fest_Andorra_Invitational')
links.append('https://liquipedia.net/brawlstars/CBBS/Season_4')
links.append('https://liquipedia.net/brawlstars/Brawl_Stars_World_Finals/2023')
links.append('https://liquipedia.net/brawlstars/Brawl_Stars_World_Finals/2022')

df = pd.DataFrame({'Mode': [], 'Map': [], 'Blue Score': [], 'Red Score': [], 'First': [], 
                    'Blue Pick 1': [], 'Blue Pick 2': [], 'Blue Pick 3': [], 
                    'Red Pick 1': [], 'Red Pick 2': [], 'Red Pick 3': [], 
                    'Blue Ban 1': [], 'Blue Ban 2': [], 'Blue Ban 3': [], 
                    'Red Ban 1': [], 'Red Ban 2': [], 'Red Ban 3': []})

for link in links:
    data = scrape(link)

    df = pd.concat([df, data])

df.to_csv('./output/output.csv', index=False)