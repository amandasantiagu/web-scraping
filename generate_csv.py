import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re
import csv
from pathlib import Path
import os

def generate_csv(file, data: list, headers: list = ['Ano', 'Nome da Música', 'Artista', 'Gênero']):
    with open(file.replace('.json', '.csv'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow({'Ano': row['Ano'], 'Nome da Música': row['Nome da Música'], 'Artista': row['Artista'], 'Gênero': row.get('Gênero', 'não encontrado')})

def split_pop_words(genre):
    result = re.sub(r'(\w)pop(\w)', r'\1,pop,\2', genre, flags=re.IGNORECASE)
    return result

def extract_genre(data: list):
    genre = data.get('Genre', None)
    if not genre:
        genre = data.get('Genres', 'não encontrado').split('\n')
    else:
        genre = genre.split('\n')
    genres = [i for i in genre if i != '']

    cleaned_genres = [re.sub(r'\[\d+\]', '', genre) for genre in genres]

    cleaned_genres = [split_pop_words(genre) for genre in cleaned_genres]
    for word in cleaned_genres:
        if 'pop' in word:
            cleaned_genres.extend(word.split(','))
            cleaned_genres.remove(word)
    return cleaned_genres


def iterate_on_list(data: list):
    formated_data = []
    for item in data:
        extracted_gender = extract_genre(item.get('Wikipedia Info')) if item.get('Wikipedia Info') else ['não encontrado']
        print({'Ano': item['Ano'], 'Nome da Música': item['Nome da Música'], 'Artista': item['Artista'], 'Gênero': extracted_gender})
        formated_data.append({'Ano': item['Ano'], 'Nome da Música': item['Nome da Música'], 'Artista': item['Artista'], 'Gênero': extracted_gender})
    return formated_data


def main():
    path = Path(__file__).parent.absolute()
    for file in os.listdir(path):
        if file.endswith('.json') and 'final' not in file:
            with open(path / file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data_csv = iterate_on_list(data)
            generate_csv(file, data_csv, headers=['Ano', 'Nome da Música', 'Artista', 'Gênero'])


if __name__ == '__main__':
    main()
