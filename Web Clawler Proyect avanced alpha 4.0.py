#Web Clawler Proyect alpha 4.0

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.exporters import JsonItemExporter, XmlItemExporter

import time
import hashlib
from scrapy.dupefilters import RFPDupeFilter

# Spider de productos
class ProductsSpider(CrawlSpider):

  name = 'products'

  def start_requests(self):
    yield scrapy.FormRequest(
      url='https://www.example.com/login',
      formdata={'user': 'john', 'password': 'secret'},
      callback=self.parse_after_login
    )

  def parse_after_login(self, response):
    # Extraer productos

  def closed(self, reason):
    # Estadísticas crawl
  
  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super(ProductsSpider, cls).from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    return spider  

# Detectar duplicados
class HashDupeFilter(RFPDupeFilter):

  def __init__(self):
    self.fingerprints = set()

  def request_seen(self, request):
    fp = hashlib.sha1(request.url.encode('utf8')).hexdigest()
    if fp in self.fingerprints:
      return True
    self.fingerprints.add(fp)
    return False

# Delay entre requests  
class PoliteSpiderMiddleware:

  def process_request(self, request, spider):
    time.sleep(1)
    
# Logging 
import logging
logging.basicConfig(level=logging.DEBUG)

# Exportar feeds
from scrapy.exporters import JsonItemExporter