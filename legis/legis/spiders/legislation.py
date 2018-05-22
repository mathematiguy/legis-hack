# -*- coding: utf-8 -*-
import os, re
import scrapy
from urllib import urlopen

class LegislationSpider(scrapy.Spider):
    
    def __init__(self, from_year, to_year, **kwargs):
        self.from_year = from_year
        self.to_year = to_year
        super(LegislationSpider, self).__init__(**kwargs)

    name = 'legislation'
    allowed_domains = ['legislation.govt.nz']
    start_urls = ['http://legislation.govt.nz/subscribe/act/public/']
    root_dir = "../legislation/xml"

    def parse(self, response):
        # get the li tags from the current page
        li_tags = response.xpath("/html/body/ul/li")
        file_regex = re.compile("[^/]+$")
        for li in li_tags:
            # check the class of the li tag
            li_class = li.xpath("@class").extract()[0]
            href     = li.xpath("a/@href").extract()[0]
            
            # check the year
            year = re.search("/subscribe/act/public/(\\d+).*", href).group(1)
            if year < self.from_year or year > self.to_year:
                continue

            if li_class == "directory":
                # the tag points to a directory, so get the href 
                next_page = response.urljoin(href)
                # get folder_path from href
                folder_path = os.path.join(self.root_dir, href[1:])

                if not os.path.exists(folder_path):
                    # create folder_path if it doesn't exist
                    self.logger.info("creating path %s" % folder_path)
                    os.makedirs(folder_path)

                # go to the next page
                yield scrapy.Request(next_page, callback = self.parse)

            elif li_class == "file" and href.endswith(".xml"):
                file_url = response.urljoin(href)
                file_path = os.path.join(self.root_dir, href[1:])
                
                if not os.path.isfile(file_path):
                    self.logger.info("reading file %s" % file_path)
                    f = urlopen(file_url)
                    f_text = f.read()
                    with open(file_path, "wb") as f:
                        f.write(f_text)
                else:
                    self.logger.info("file %s already exists" % file_path)
                    continue

            else:
            	if not li_class == "file":
            		self.logger.info("class %s found is not .xml file or directory for tag %s" %(li_class, li.extract()))



                