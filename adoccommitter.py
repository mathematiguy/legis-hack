import subprocess
import os
import sys
import re

def commit_adoc_to_git(file_path):
    #print(file_path)
    uploadScript = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'rename_upload.sh')
    #print(uploadScript)
    subprocess.call([uploadScript, file_path])

def walk_dir():
    walk_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'legislation/adoc')
    
    #print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            #regex to check if the file is original downloaded xml
            pattern = re.compile(".adoc")
            match = pattern.search(filename)
            if match:
                file_path = os.path.join(root, filename)
                commit_adoc_to_git(file_path)
                
    subprocess.call(['git', 'push'])
                    
walk_dir()
