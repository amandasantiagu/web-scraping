import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re
import csv


def generate_csv(data: list, headers: list = ['Ano', 'Nome da Música', 'Artista', 'Gênero']):
    with open('musicas.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow({'Ano': row['Ano'], 'Nome da Música': row['Nome da Música'], 'Artista': row['Artista'], 'Gênero': row.get('Gênero', 'não encontrado')})

def extract_genre(data: list):
    genre = data.get('Genre', 'não encontrado').split('\n')
    genres = [i for i in genre if i != '']
    cleaned_genres = [re.sub(r'\[\d+\]', '', genre) for genre in genres]
    return cleaned_genres


def iterate_on_list(data: list):
    formated_data = []
    for item in data:
        extracted_gender = extract_genre(item['Wikipedia Info'])
        print({'Ano': item['Ano'], 'Nome da Música': item['Nome da Música'], 'Artista': item['Artista'], 'Gênero': extracted_gender})
        formated_data.append({'Ano': item['Ano'], 'Nome da Música': item['Nome da Música'], 'Artista': item['Artista'], 'Gênero': extracted_gender})
    return formated_data


def main():
    with open('musicas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data_csv = iterate_on_list(data)
    generate_csv(data_csv, headers=['Ano', 'Nome da Música', 'Artista', 'Gênero'])


if __name__ == '__main__':
    main()
