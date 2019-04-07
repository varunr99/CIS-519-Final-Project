from bs4 import BeautifulSoup
import requests
import csv
import urllib.request
import re

base_url = "https://www.basketball-reference.com"

page = requests.get(base_url + "/playoffs")
soup = BeautifulSoup(page.content, "html.parser")

years = soup.find('table', id='champions_index').find('tbody').findAll('tr')


with open("data.csv", mode="a") as csv_file:
    writer = csv.writer(csv_file)

    i = 0
    while (i < 39):

        year = years[i]

        if (year.find('th') != None):
            year_link = year.find('th').contents[0].get('href')
            year_num= year.find('th').contents[0].contents[0]
            
            year_url = base_url + year_link
            year_page = requests.get(year_url)
            year_soup = BeautifulSoup(year_page.content, "html.parser")

            playoff = year_soup.find('table', id='all_playoffs').find('tbody').findAll('tr')

            for p in playoff:
                games = list(p.findAll('td'))
                if (len(games) == 3):
                    series_link = games[2].a.get('href')

                    series_url = base_url + series_link
                    series_page = requests.get(series_url)
                    series_soup = BeautifulSoup(series_page.content, "html.parser")

                    summaries = series_soup.findAll('div', {'class': 'game_summary'})

                    for summary in list(summaries):

                        team_and_opponent = []

                        info = summary.find('tbody')
                        rows = info.findAll('tr')

                        ##############Basic Info#############

                        game = rows[0].contents[0].contents[0].split(",")[0].strip()
                        date = rows[0].contents[0].contents[0].split(",")[1].strip() + " " + year_num

                        team_and_opponent.append(game)
                        team_and_opponent.append(date)

                        ##############Home Team#############

                        home = rows[1].findAll('td')

                        if (home[0].contents[0].find('a') == None):
                            home_link = home[0].contents[0].get('href')
                        else:
                            home_link = home[0].contents[0].find('a').get('href')

                        if (isinstance(home[0].contents[0].contents[0], str)):
                            home_name = home[0].contents[0].contents[0]
                        else:
                            home_name = home[0].contents[0].contents[0].contents[0]

                        home_score = home[1].contents[0] 

                        team_and_opponent.append(home_name)
                        team_and_opponent.append(home_score)

                        print(year_num, home_name, game, date)

                        home_url = base_url + home_link

                        comm = re.compile("<!--|-->")
                        home_page = urllib.request.urlopen(home_url)
                        home_soup = BeautifulSoup(comm.sub("", home_page.read().decode('utf-8')), 'html.parser')

                        #print(home_soup)
                        home_stats = home_soup.find('table', id='team_and_opponent').tbody.findAll('tr')

                        count = 0;
                        for stat in home_stats[1]:
                            if (count > 1):
                                if (len(stat.contents) > 0):
                                    team_and_opponent.append(stat.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        count = 0
                        for stat in home_stats[2]:
                            if (count > 1):
                                if (len(stat.contents) > 0):
                                    team_and_opponent.append(stat.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1


                        home_miscs = home_soup.find('table', id='team_misc').tbody.findAll('tr')

                        count = 0;
                        for misc in home_miscs[0]:
                            if (count > 0 and misc.attrs['data-stat'] != 'attendance' and misc.attrs['data-stat'] != 'arena_name'):
                                if (len(misc.contents) > 0):
                                    team_and_opponent.append(misc.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        count = 0;
                        for misc in home_miscs[1]:
                            if (count > 0 and misc.attrs['data-stat'] != 'attendance' and misc.attrs['data-stat'] != 'arena_name'):
                                if (len(misc.contents) > 0):
                                    team_and_opponent.append(misc.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        ##############Away Team#############

                        away = rows[2].findAll('td')

                        if (away[0].contents[0].find('a') == None):
                            away_link = away[0].contents[0].get('href')
                        else:
                            away_link = away[0].contents[0].find('a').get('href')

                        if (isinstance(away[0].contents[0].contents[0], str)):
                            away_name = away[0].contents[0].contents[0]
                        else:
                            away_name = away[0].contents[0].contents[0].contents[0]

                        away_score = away[1].contents[0] 

                        team_and_opponent.append(away_name)
                        team_and_opponent.append(away_score)

                        away_url = base_url + away_link

                        comm = re.compile("<!--|-->")
                        away_page = urllib.request.urlopen(away_url)
                        away_soup = BeautifulSoup(comm.sub("", away_page.read().decode('utf-8')), 'html.parser')

                        away_stats = away_soup.find('table', id='team_and_opponent').tbody.findAll('tr')

                        count = 0;
                        for stat in away_stats[1]:
                            if (count > 1):
                                if (len(stat.contents) > 0):
                                    team_and_opponent.append(stat.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        count = 0
                        for stat in away_stats[2]:
                            if (count > 1):
                                if (len(stat.contents) > 0):
                                    team_and_opponent.append(stat.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1


                        away_miscs = away_soup.find('table', id='team_misc').tbody.findAll('tr')

                        count = 0;
                        for misc in away_miscs[0]:
                            if (count > 0 and misc.attrs['data-stat'] != 'attendance' and misc.attrs['data-stat'] != 'arena_name'):
                                if (len(misc.contents) > 0):
                                    team_and_opponent.append(misc.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        count = 0;
                        for misc in away_miscs[1]:
                            if (count > 0 and misc.attrs['data-stat'] != 'attendance' and misc.attrs['data-stat'] != 'arena_name'):
                                if (len(misc.contents) > 0):
                                    team_and_opponent.append(misc.contents[0])
                                else:
                                    team_and_opponent.append("");
                            count += 1

                        writer.writerow(team_and_opponent)
        i += 1
                    



    
