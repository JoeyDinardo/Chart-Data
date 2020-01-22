import csv
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
#goes through html and returns url of photo
def mlbPhotos (name):
    url = "https://www.baseball-reference.com//players//" + name [0:1] + "//" + name [0:(len (name)-4)] + ".shtml"
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, "html.parser")
    mydivs = soup.find("div", {"class": "media-item"})
    if mydivs == None:
        mydivs = soup.find("div", {"class": "media-item multiple"})
    if (mydivs == None):
        return "https://d2p3bygnnzw9w3.cloudfront.net/req/999999999/images/klecko/placeholder.jpg"
    img = mydivs.find ('img')['src']
    return img

#writes to csv file
def writeToFile (csv_reader, fileName):
    f = open (fileName,"w")
    for row in csv_reader:
        for value in row:
            f.write (value + ",")
        f.write ("\n") 
    
def differentPhotos (name):
    nameArr = name.split ();
    nameFin = ""
    for nameOne in nameArr:
        print (nameOne)
        if (nameFin != ""):
            nameFin = nameFin + "_" + nameOne
        else:
            nameFin = nameOne
    url = "https://en.wikipedia.org/wiki/" + nameFin
    print (url)
    response = requests.get(url) 
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", attrs={'class':'infobox biography vcard'})
    tableBol = 1
    if (table == None):
        tableBol = 2
        table = soup.find("table", attrs={'class':'infobox vcard'})
    if (table == None):
        tableBol = 3
        table = soup.find("table", attrs={'class':'infobox bordered vcard'})
        if (table == None):
            return "https://d2p3bygnnzw9w3.cloudfront.net/req/999999999/images/klecko/placeholder.jpg"
    table_body = table.find ("tbody")
    if (table_body.find ('img')== None):
        if (tableBol == 1):
            table = soup.find("table", attrs={'class':'infobox vcard'})
            if (table == None):
                table = soup.find("table", attrs={'class':'infobox bordered vcard'})
                if (table == None):
                    return "https://d2p3bygnnzw9w3.cloudfront.net/req/999999999/images/klecko/placeholder.jpg"
    if (table_body.find ('img')== None):
        print ("3")
        return "https://d2p3bygnnzw9w3.cloudfront.net/req/999999999/images/klecko/placeholder.jpg"
    img = table_body.find ('img')['src']
    print (img [2:])
    return img [2:]
    


with open("C:\\Users\\skill.DESKTOP-CFTHB0I\\OneDrive\\Documents\\CSVFiles\\richestAthlete.csv") as csv_file:
    data = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count !=0:
            row [1] = differentPhotos (row [0])
            data.insert (line_count, row)
        else:
            data.insert (line_count,row)
        line_count+=1
        print (line_count)
    writeToFile (data, "testDifferent.csv")    
