# scripts/scrape_unitecnar.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse

def crawl_and_scrape_site():
    """
    Crawlea el sitio desde la página de inicio, descubriendo y scrapeando
    enlaces internos para evadir el bloqueo del sitemap.
    """
    HOME_URL = "https://www.unitecnar.edu.co/"
    print(f"Paso 1: Iniciando Crawler desde la página de inicio: {HOME_URL}")

    # --- Configuración de Selenium Stealth ---
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    links_to_visit = set([HOME_URL])
    visited_links = set()
    all_content = {}

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        stealth(driver, languages=["es-ES", "es"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
        
        while links_to_visit:
            current_url = links_to_visit.pop()
            if current_url in visited_links:
                continue

            print(f"Procesando: {current_url}")
            visited_links.add(current_url)

            try:
                driver.get(current_url)
                time.sleep(3) # Espera para carga de JS
                
                # Extraer contenido de la página actual
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                main_content = soup.find('main') or soup.find('article') or soup.body
                content_text = main_content.get_text(separator='\n', strip=True)
                all_content[current_url] = content_text
                
                # Descubrir nuevos enlaces internos en la página actual
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    # Unir la URL base con el enlace encontrado
                    full_url = urljoin(HOME_URL, href)
                    # Asegurarnos de que es una URL interna y no un archivo
                    if urlparse(full_url).netloc == urlparse(HOME_URL).netloc and not full_url.endswith(('.pdf', '.jpg', '.png', '.zip')):
                        if full_url not in visited_links:
                            links_to_visit.add(full_url)
            
            except Exception as e:
                print(f"  -> Error procesando {current_url}: {e}")

    finally:
        if driver:
            driver.quit()
            print("\nNavegador cerrado.")
    
    # --- Guardar el contenido consolidado ---
    if all_content:
        if not os.path.exists('knowledge_base'):
            os.makedirs('knowledge_base')
            
        file_path = 'knowledge_base/full_site_content.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            for url, text in all_content.items():
                f.write(f"\n\n--- Contenido de {url} ---\n\n{text}")
        print(f"Proceso completado. Contenido de {len(all_content)} páginas guardado en: {file_path}")
    else:
        print("No se pudo extraer contenido del sitio.")


if __name__ == "__main__":
    crawl_and_scrape_site()