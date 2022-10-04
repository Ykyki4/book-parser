from pathlib import Path, PurePath

import requests
def download_file(path, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)
def get_book():
    for id in range(10):
        url = f"https://tululu.org/txt.php?id={id}"
        filename = f'book_{id}.txt'
        Path('books/').mkdir(parents=True, exist_ok=True)
        path = PurePath('books', filename)
        download_file(path, url)

if __name__ == "__main__":
    get_book()