from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import re
import os
import xml.dom.minidom

def read_url(url, start_year):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    indexPage = BeautifulSoup(a, 'html.parser')
    
    baseUrl = 'http://legislation.govt.nz'
    
    #Find any directories to recurse
    dirs = (indexPage.find_all('li', class_='directory'))
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
            if year != None and year >= start_year:
                #print('Going in to dir ' + dirUrl)
                
                #Recurse in to the directory
                read_url(dirUrl, start_year)
                
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    
    #Find any files to download
    files = (indexPage.find_all('li', class_='file'))
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
            req = Request(fileUrl)
            xmlFile = urlopen(req).read()

            #Make the xml pretty for easy reading in the file
            xmlString = xml.dom.minidom.parseString(xmlFile.decode("utf-8"))
            pretty_xml_as_string = xmlString.toprettyxml()

            #set up the directory to save the file
            #this will be relative to the location of the python script!
            file_path = os.path.join(script_dir, link['href'])
            relative_file_path = "." + file_path
            
            #If the directory doesn't exist yet, create it recursively
            dirname = os.path.dirname(relative_file_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            #Open the new file and write the xml as a utf8 string
            file = open(relative_file_path, 'w')
            file.write(pretty_xml_as_string)
            file.close()
            print("Downloaded to: " + relative_file_path)
        
read_url("http://legislation.govt.nz/subscribe/act/public", 2018)
