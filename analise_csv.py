import os
import pandas as pd
import re
from collections import Counter
from ast import literal_eval
from pathlib import Path
import matplotlib.pyplot as plt

def read_csv(file_path):
    return pd.read_csv(file_path)

def count_genres_and_artists(df):
    genre_counter = Counter()
    artist_counter = Counter()

    for _, row in df.iterrows():
        artist_counter[row['Artista']] += 1

        genres = literal_eval(row['Gênero'])
        if isinstance(genres, list):
            for genre in genres:
                for sub_genre in re.split(r'[·,]', genre):
                    cleaned_genre = sub_genre.strip().lower()
                    if cleaned_genre != 'não encontrado':
                        genre_counter[cleaned_genre] += 1

    return genre_counter, artist_counter

def plot_most_common(counter, title, xlabel, ylabel, num_items=10):
    items = counter.most_common(num_items)
    labels, values = zip(*items)

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{title}.png')
    plt.show()


def main():
    path = Path(__file__).parent.absolute()

    for file in os.listdir(path):
        if not file.endswith('.csv'):
            continue
        df = read_csv(path / file)

        genre_counter, artist_counter = count_genres_and_artists(df)

        print("Gêneros com mais músicas:")
        for genre, count in genre_counter.most_common():
            print(f"{genre}: {count}")

        print("\nArtistas com mais músicas:")
        for artist, count in artist_counter.most_common():
            print(f"{artist}: {count}")

        plot_most_common(genre_counter, f'Gêneros com mais músicas ({file.split('_')[0]})', 'Gêneros', 'Número de prêmios')
        plot_most_common(artist_counter, f'Artistas com mais músicas({file.split('_')[0]})', 'Artistas', 'Número de prêmios')


if __name__ == "__main__":
   main()
