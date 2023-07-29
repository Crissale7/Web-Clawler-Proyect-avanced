# Web Clawler Proyect avanced alpha 3.0


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

import time
import json
import hashlib
from urllib.robotparser import RobotFileParser

configure_logging()

class MiSpider(CrawlSpider):

  name = 'mi-crawler'
  
  rules = (
    Rule(LinkExtractor(), callback='parse_page', follow=True),
  )

  def __init__(self, *args, **kwargs):
    # URLs iniciales
    self.start_urls = ['https://www.example.com']

    # Politeness delay
    self.download_delay = 1

    # Profundidad máxima
    self.max_depth = 2

    #Cola FIFO 
    self.fifo_urls = [] 

    super().__init__(*args, **kwargs)

  def parse_page(self, response):
    url = response.url

    #Extraer metadatos
    title = response.css('title::text').get()
    description = response.xpath('//meta[@name="description"]/@content').get()

    #Calcular hash
    page_hash = hashlib.sha256(response.body).hexdigest()

    #Guardar resultado
    item = {
       'url': url,
       'status': response.status,
       'title': title,
       'description': description,
       'page_hash': page_hash       
    }

    #Exportar a JSON
    self.export_data(item)

  def export_data(self, item):
    with open('results.json', 'a') as f:
      json.dump(item, f) 
      f.write('\n')

# Ejecutar spider   
process = CrawlerProcess()
process.crawl(MiSpider)
process.start()