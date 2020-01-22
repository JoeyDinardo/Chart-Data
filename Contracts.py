import requests
from bs4 import BeautifulSoup, Comment
import csv
#returns html from web page
def getSoup (url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup
#returns all urls from table
def getTeams(soup):
    tables = soup.find(text=lambda text: text and isinstance(text, Comment) and 'Team Per Game Stats' in text)
    table_soup = BeautifulSoup(tables, "html.parser")
    urls = table_soup.find_all('a', href=True)
    return urls
#returns salaries from table
def getContracts (soup):
    tables = soup.find(text=lambda text: text and isinstance(text, Comment) and 'Salaries' in text)
    if (tables == None):
        return []
    table_soup = BeautifulSoup(tables, "html.parser")
    tds = table_soup.find_all ("td",{"data-stat":"salary"})
    return tds
#returns names from table
def getContractsName (soup):
    tables = soup.find(text=lambda text: text and isinstance(text, Comment) and 'Salaries' in text)
    if (tables == None):
        return []
    table_soup = BeautifulSoup(tables, "html.parser")
    tds = table_soup.find_all ("td",{"data-stat":"player"})
    return tds
#adds name and year from to csv file
def addCSV (contractValues, names, year):
    with open('C:\\Users\\skill.DESKTOP-CFTHB0I\\OneDrive\\Documents\\CSVFiles\\NBA Progression Each Year Total\\Contracts\\' + str (year) + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range (0,len (names)):
            for y in range (0,len (names [i])):
                if (str (names [i][y]).find ("html")!=-1):
                    print (names [i][y])
                    writer.writerow ([((str (names [i][y].text.encode("utf-8")) +r"\'"+ names [i][y].a['href'][names [i][y].a['href'].rfind ("/")+1 : -5]).replace ("b'","")).replace("'","") ,contractValues[i][y].text  ])
               
            
#Goes through each possible year
for i in range (1992,2021):
    print (i)
    urls = getTeams (getSoup ("https://www.basketball-reference.com/leagues/NBA_" + str (i) + ".html"))
    contractValues = []
    names = []
    for url in urls:
        contractValues.append (getContracts (getSoup ("https://www.basketball-reference.com/" + url['href'])))  
        names.append (getContractsName(getSoup ("https://www.basketball-reference.com/" + url['href'])))
    addCSV (contractValues,names,i)
