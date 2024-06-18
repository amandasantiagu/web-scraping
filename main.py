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

                            infobox_dict[header.text.strip()] = data.text.strip().replace('·', '\n')

                    return infobox_dict
    return None

def get_song_info(url, raw_text):
    info = {}
    try:
        if 'fatosdesconhecidos' in url:
            if ' – ' in raw_text:
                partes = raw_text.split(' – ')
                ano = partes[0].strip()

                if ' by ' in partes[1]:

                    nome_musica, artista = partes[1].split(' by ')
                    nome_musica = nome_musica.strip()
                    artista = artista.strip()

                else:
                    nome_musica = partes[1].strip()
                    artista = "Desconhecido"
                info = {'ano': ano, 'nome_musica': nome_musica, 'artista': artista}

        elif 'revistabula' in url:
            if '(' in raw_text and ')' in raw_text:
                raw_text = raw_text[1:] if raw_text[0] == '(' else raw_text
                texto_ = raw_text.replace('(', ' - ').replace(')', '').replace(' — ', ' - ')
                partes = texto_.split(' - ')
                ano = partes[0].strip()

                if len(partes) > 2:

                    nome_musica, artista = partes[1].strip(), partes[2].strip()


                else:
                    raise ValueError
                info = {'ano': ano, 'nome_musica': nome_musica, 'artista': artista}
        return info

    except ValueError:
        print("Erro ao processar o texto:", raw_text)
        return info


def find_songs(url: str):
    url_name = url.split('.')[1]
    driver = webdriver.Chrome()
    driver.get(url)

    site_content = driver.page_source

    soup = BeautifulSoup(site_content, 'html.parser')

    musicas = soup.find_all('p')
    print(f"Encontradas {len(musicas)} possíveis músicas.")

    musica_list = []

    for musica in musicas:
        texto = musica.get_text().strip()
        # print("Texto encontrado:", texto)

        info: dict = get_song_info(url, texto)

        nome_musica = info.get('nome_musica', None)
        artista = info.get('artista', None)
        ano = info.get('ano', None)

        if nome_musica is None:
            continue
        try:
            print(f"Ano: {ano}, Nome da Música: {nome_musica}, Artista: {artista}")
            wikipedia_info = get_wikipedia_info(artista, nome_musica)

            musica_list.append({
                "Ano": ano,
                "Nome da Música": nome_musica,
                "Artista": artista,
                "Wikipedia Info": wikipedia_info,
                "Fonte URL": url
            })
        except Exception as e:
            print(f"Erro: \n {e} \n ao obter info da wikipedia para a musica: {musica}")
            continue

    with open(f'{url_name}_musicas.json', 'w', encoding='utf-8') as f:
        json.dump(musica_list, f, ensure_ascii=False, indent=4)
    print("Arquivo JSON criado com sucesso com", len(musica_list), "elementos.")
    driver.quit()
    return {url_name: musica_list}


def main():
    urls: list = [
        'https://www.fatosdesconhecidos.com.br/essas-sao-as-musicas-mais-ouvidas-de-1950-ate-2022/',
        'https://www.revistabula.com/15910-2-a-musica-mais-tocada-no-ano-em-que-voce-nasceu/'

        ]
    final_json = []
    for url in urls:
        songs = find_songs(url)
        final_json.append(songs)

    with open('musicas_final.json', 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=4)
    print("Arquivo JSON criado com sucesso com", len(final_json), "elementos.")


if __name__ == '__main__':
    s_time = time.time()
    main()
    print(f"Tempo de execução: {time.time() - s_time:.2f} segundos.")