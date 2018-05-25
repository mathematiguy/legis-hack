import os
import sys
import re
from bs4 import BeautifulSoup, element
from multiprocessing import Pool, cpu_count

def xml_transform_asciidoc(file_path):
    #setup the name of the output file
    root_path = os.path.dirname(os.path.realpath(__file__))
    file_title = os.path.basename(file_path)[:-4]
    files_folder_name = file_title[5:]
    
    #create the output file and open it
    with open(file_path) as inputFile:
        #parse the xml and get only the body tag
        soup = BeautifulSoup(inputFile, "lxml-xml")
        
        output_file_name = file_title + ".adoc"
        output_file_path = os.path.join(root_path, 'legislation/adoc', files_folder_name, output_file_name)

        dirname = os.path.dirname(output_file_path) + "/"

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        title = soup.find("title").contents[0]
        
        print("Processing: %s" % title)
        print("Generating output: " + output_file_path)
        
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
            contents = defTerm.contents
            if len(contents) > 0:
                try:
                    if isinstance(contents[0], element.Tag):
                        content = contents[0].extract()
                        newTag = soup.new_tag('text')
                        newTag.string = '\n\n'
                        defTerm.insert_before(newTag)
                        defTerm.insert_before(content)
                    if isinstance(contents[0], str):
                        defTerm.replace_with('*' + contents[0] + '*')
                except IndexError:
                    print("Skipping %s due to IndexError" % contents)
                    continue
                
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
            contents = variableDef.contents
            if len(contents) > 0:
                if isinstance(contents[0], element.Tag):
                    content = contents[0].extract()
                    newTag = soup.new_tag('text')
                    newTag.string = '\n\n'
                    variableDef.insert_before(newTag)
                    variableDef.insert_before(content)
                if isinstance(contents[0], str):
                    variableDef.replace_with('\n\n' + contents[0] + ' ')
        
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

    pool = Pool(processes = cpu_count() - 1)

    walk_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'legislation/xml')
    
    file_paths = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if filename.endswith(".xml"):
                file_paths.append(os.path.join(root, filename))

    pool.map_async(xml_transform_asciidoc, file_paths)
    pool.close()
    pool.join() 

walk_dir()

