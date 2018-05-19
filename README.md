# Version Tracking for Legislation

**Problem Statement**

In its current state, an end-user (NZ resident or legislator) can view the acts, bills and legislative instruments on the government website - ‘http://legislation.govt.nz’. The legislation is available in the form of a ‘PDF’ or ‘HTML’ document. One can also see the different versions of the same legislation. Though this is a good portal, we observer a couple of shortcomings. 

1. There is no easy way to identify the differences of legislation between any two versions of the same document.
2. An end-user has no way to request changes in legislation (specified in a document).

In order to address these shortcomings, we brainstormed a few ideas and one of them was to try and store the legislation in ‘human-readable’ form in Github (https://github.com/). Doing this would allow us to use Github’s out-of-box features of storing version history, tracing the differences between versions and support a ‘pull-request’ workflow.

**Process**

First, get the xml files of each act (and its amendments) from legislation.govt.nz/subscribe: xmldownload.py

Second, process each xml file and create a markdown / asciidoc version starting at the first version of each act, in subdirectory /legislation/act-name/<version>_<act name>.adoc: xmltransformer.py

Third, iterate through subdirectories:

1. Take the first version, remove <version> and _, copy it to ../legislation/
2. Git commit & push
3. Take the second version, remove <version> and _, copy it to ../legislation/ (replace existing file)
4. Git commit & push
5. Etc, until all files in each subdirectory are pushed
  
# Dependencies

Python 3

BeautifulSoup

