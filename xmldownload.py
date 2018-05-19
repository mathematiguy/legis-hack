from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import re

def read_url(url):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    
    baseUrl = 'http://legislation.govt.nz'
    
    #Find any directories to recurse
    dirs = (soup.find_all('li', class_='directory'))
    for i in dirs:
        #find link addresses
        link = i.find('a')
        dirUrl = baseUrl + link['href']
        #print(dirUrl)
        
        #Regex to check if this directory is newer than year 2000
        pattern = re.compile("public/([0-9]{4})")
        match = pattern.search(dirUrl)
        #print(match)
        if match:
            #print("Group 1: " + match.group(1))
            year = int(match.group(1))
            if year != None and year > 2000:
                #print('Going in to dir ' + dirUrl)
                
                #Recurse in to the directory
                read_url(dirUrl)
    
    #Find any files to download
    files = (soup.find_all('li', class_='file'))
    for i in files:
        #get the link to the file
        link = i.find('a')
        fileUrl = baseUrl + link['href']
        
        #regex to check if the file is XML within the appropriate dir structure
        pattern = re.compile("[0-9]{4}/[0-9]{2}\.[0-9]{1}/(.*\.xml)")
        match = pattern.search(fileUrl)
        if match:
            #download the file here...
            print("Download file: " + fileUrl)
        

read_url("http://legislation.govt.nz/subscribe/act/public")
