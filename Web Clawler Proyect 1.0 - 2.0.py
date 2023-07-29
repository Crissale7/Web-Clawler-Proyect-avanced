# Web Clawler Proyect Alpha 1.0

import requests
from bs4 import BeautifulSoup 
import re
import sqlite3
from urllib.robotparser import RobotFileParser

dominios_permitidos = ['www.example.com']

def rastrear(url):
  try:
    if es_dominio_permitido(url):
      respuesta = requests.get(url)
      soup = BeautifulSoup(respuesta.content, 'html.parser')
  except Exception as e:
    print(f'Error al cargar URL {url}: {e}')
  else:
    guardar_en_db(url, respuesta.status_code, len(respuesta.content))
    
    for enlace in soup.find_all('a'):
      nuevo_url = enlace.get('href')
      if es_enlace_valido(nuevo_url):
        # Lógica de encolar nuevo URL para rastreo  

def es_dominio_permitido(url):
  return url.split('/')[2] in dominios_permitidos

def es_enlace_valido(url):
  patron = re.compile(r'^https?')
  return re.match(patron, url) is not None

def guardar_en_db(url, status, tamano):
  conexion = sqlite3.connect('resultados_crawl.db')
  cursor = conexion.cursor()
  
  cursor.execute('INSERT INTO resultados VALUES (?,?,?)', (url, status, tamano))
  
  conexion.commit()
  conexion.close()
  
if __name__ == '__main__':

  url_inicial = 'https://www.example.com/'
  
  rp = RobotFileParser()
  rp.set_url(url_inicial + 'robots.txt')
  rp.read()
  
  cola_urls = [url_inicial]
  
  while cola_urls:
    url_actual = cola_urls.pop(0)
    if rp.can_fetch('*', url_actual):
      rastrear(url_actual)

  print('Rastreo finalizado')