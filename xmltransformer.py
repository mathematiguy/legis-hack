import os
import sys
import re
from bs4 import BeautifulSoup

def xml_transform_asciidoc(file_path):
    #setup the name of the output file
    output_name = os.path.basename(file_path)[:-4] + "_output.xml"
    output_file_path = os.path.join(os.path.dirname(file_path), output_name)
    
    print("Generating output: " + output_file_path)
    
    #creae the output file and open it
    with open(file_path) as inputFile:
        #parse the xml and get only the body tag
        soup = BeautifulSoup(inputFile, "lxml-xml")
        body = soup.find('body')
        
        bodyString = body.decode()
        
        #Uncomment the following 3 lines if pretty printing is enabled on downloader
        #pattern = re.compile("(\n|\r)\t{2,}")
        #bodyString = re.sub(pattern, "", bodyString)
        #bodyString = re.sub(pattern, "", bodyString)
        
        #save the output file
        with open(output_file_path, "w") as outputFile:
            outputFile.write(bodyString)
        
#walks through the directory the script is located, passing matching files to the transform function
def walk_dir():
    walk_dir = os.path.dirname(os.path.realpath(__file__))
    #print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            #regex to check if the file is original downloaded xml
            pattern = re.compile("[a-f0-9]{16}\.xml")
            match = pattern.search(filename)
            if match:
                file_path = os.path.join(root, filename)
                xml_transform_asciidoc(file_path)
                    
walk_dir()

