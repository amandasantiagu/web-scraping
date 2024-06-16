import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json


def get_wikipedia_info(artista, musica):
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={musica} {artista} song&format=json"

    response = requests.get(search_url)
    if response.status_code == 200:
        search_results = response.json()
        if search_results['query']['search']:
            page_title = search_results['query']['search'][0]['title']
            page_url = f"https://en.wikipedia.org/wiki/{page_title}"
            page_response = requests.get(page_url)

            if page_response.status_code == 200:

                page_content = page_response.text
                soup = BeautifulSoup(page_content, 'html.parser')
                infobox_table = soup.find('table', class_='infobox')

                if infobox_table:

                    infobox_dict = {}
                    rows = infobox_table.find_all('tr')

                    for row in rows:

                        header = row.find('th')
                        data = row.find('td')

                        if header and data:

                            infobox_dict[header.text.strip()] = data.text.strip()

                    return infobox_dict
    return None

url = 'https://www.fatosdesconhecidos.com.br/essas-sao-as-musicas-mais-ouvidas-de-1950-ate-2022/'

driver = webdriver.Chrome()
driver.get(url)

site_content = driver.page_source

soup = BeautifulSoup(site_content, 'html.parser')

musicas = soup.find_all('p')
print(f"Encontradas {len(musicas)} possíveis músicas.")

musica_list = []

for musica in musicas:
    texto = musica.get_text().strip()
    print("Texto encontrado:", texto)
    if ' – ' in texto:
        try:

            partes = texto.split(' – ')
            ano = partes[0].strip()

            if ' by ' in partes[1]:

                nome_musica, artista = partes[1].split(' by ')
                nome_musica = nome_musica.strip()
                artista = artista.strip()

            else:
                nome_musica = partes[1].strip()
                artista = "Desconhecido"

            wikipedia_info = get_wikipedia_info(artista, nome_musica)

            musica_list.append({
                "Ano": ano,
                "Nome da Música": nome_musica,
                "Artista": artista,
                "Wikipedia Info": wikipedia_info,
                "Fonte URL": url
            })
        except ValueError:
            print("Erro ao processar o texto:", texto)
            continue

with open('musicas.json', 'w', encoding='utf-8') as f:
    json.dump(musica_list, f, ensure_ascii=False, indent=4)
print("Arquivo JSON criado com sucesso com", len(musica_list), "elementos.")
driver.quit()
