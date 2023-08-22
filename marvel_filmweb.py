import requests
from bs4 import BeautifulSoup
from datetime import datetime

movies_chronology = {}

main_link = "https://filmweb.pl"
odpowiedz = requests.get(f"{main_link}/world/Marvel-2/filmsAndSerials")
main_soup = BeautifulSoup(odpowiedz.text, 'html.parser')

movies_link_title = main_soup.find_all("a", class_="preview__link")
titles = []
links = []
future = []
months_numbers = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4,
    'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
    'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12}
not_wanted = {"Ghost Rider" : "all", "Uncanny X" : "all", "Punisher" : 2017,
    "Daredevil": 2015, "X-Men": "all", "Wolverine": "all"}

def text_to_date(text):
    text.strip()
    list_date = text.split()
    try:
        day = int(list_date[0])
        month = months_numbers[list_date[1].lower()]
        year = int(list_date[2])
        return datetime(year, month, day).date()
    except:
        return "brak prawidłowej daty"

for title in movies_link_title:
    titles.append(title.text)
    if title.text == "Iron Man":
        break

for link in movies_link_title:
    links.append(main_link+link['href'])
    if link.text == "Iron Man":
        break

no = 0
for link in links:   
    odpowiedz1 = requests.get(link)
    medium_soup = BeautifulSoup(odpowiedz1.text, 'html.parser')

    movie_type = medium_soup.find("span", {"data-cacheid":"filmMainCover"}).text
    movie_genre = medium_soup.find("span", {"data-cacheid":"filmMainHeader"}).text

    if movie_genre == "Dokumentalny":
        no += 1
        continue

    if movie_type == "serial":
        last_season = medium_soup.find("a", {"class":"squareNavigation__item main"})
        if last_season:
            no_of_seasons = int(last_season["data-value"])
            if no_of_seasons == 1:
                date_text = medium_soup.find("span", class_="block", itemprop="datePublished").text
                movie_date = text_to_date(date_text)
                if type(movie_date) == str:
                    no += 1
                    continue
                movies_chronology[titles[no]] = [link, movie_type, movie_date]
            else:
                odpowiedz2 = requests.get(main_link+last_season["href"])
                minor_soup = BeautifulSoup(odpowiedz2.text, 'html.parser')
                season_date_str = minor_soup.find("time", class_="absoluteDate")["datetime"]
                season_date = datetime.strptime(season_date_str, "%Y-%m-%d").date()
                movies_chronology[titles[no] + ", sezon " + str(no_of_seasons)] = [link, movie_type, season_date]

                seasons_links = medium_soup.find_all("a", {"class":"squareNavigation__item"})
                for link in seasons_links:
                    odpowiedz3 = requests.get(main_link+link["href"])
                    minor_soup = BeautifulSoup(odpowiedz3.text, 'html.parser')
                    season_date_str = minor_soup.find("time", class_="absoluteDate")["datetime"]
                    season_date = datetime.strptime(season_date_str, "%Y-%m-%d").date()
                    movies_chronology[titles[no] + ", sezon " + link["data-value"]] = [main_link+link["href"], movie_type, season_date]
        else:
            future.append(titles[no])
    elif movie_type == "film" or "miniserial":
        date_text = medium_soup.find("span", class_="block", itemprop="datePublished").text
        movie_date = text_to_date(date_text)
        if type(movie_date) == str:
            no += 1
            continue
        movies_chronology[titles[no]] = [link, movie_type, movie_date]

    no += 1

to_remove = []
for title in movies_chronology.keys():
    if movies_chronology[title][2].year > datetime.today().year:
        to_remove.append(title)
        continue
    for movie in not_wanted:
        if movie in title:
            if not_wanted[movie] == "all" or movies_chronology[title][2].year < not_wanted[movie]:
                to_remove.append(title)
to_remove = list(set(to_remove))
for title in to_remove:
    del movies_chronology[title]

movies_chronology = dict(sorted(movies_chronology.items(), key=lambda x: x[1][2]))

i=1
for movie, properties  in movies_chronology.items():
    print(i,"-", movie+":", properties[1], properties[2], properties[0])
    i += 1