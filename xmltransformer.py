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
        
        cfTags = body.find_all('cf')
        for cfTag in cfTags:
            cfTag.decompose()
            
        notesTags = body.find_all('notes')
        for notesTag in notesTags:
            notesTag.decompose()
            
        labels = body.find_all('label')
        for label in labels:
            text = label.contents
            if len(text) > 0:
                label.replace_with('\n\n' + text[0] + ' ')
            else:
                label.replace_with('\n')
                
        #process rules for how to handle various tags
        defTerms = body.find_all('def-term')
        for defTerm in defTerms:
            text = defTerm.contents
            if len(text) > 0:
                defTerm.replace_with('*' + text[0] + '* ')
                
        defParas = body.find_all('def-para')
        for defPara in defParas:
            contents = defPara.contents
            if len(contents) > 0:
                content = contents[0].extract()
                newTag = soup.new_tag('text')
                newTag.string = '\n\n'
                defPara.insert_before(newTag)
                defPara.insert_before(content)
                
        crossheads = body.find_all('crosshead')
        for crosshead in crossheads:
            crosshead.replace_with('\n\n')
            
        eqnLines = body.find_all('eqn-line')
        for eqnLine in eqnLines:
            text = eqnLine.contents
            if len(text) > 0:
                eqnLine.replace_with('\n\n ' + text[0] + '\n\n')
                
        variableDefs = body.find_all('variable-def')
        for variableDef in variableDefs:
            text = variableDef.contents
            if len(text) > 0:
                variableDef.replace_with('\n\n' + text[0] + ' ')
                
        
        
        bodyString = body.get_text()
        #bodyString = body.decode()
        
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
