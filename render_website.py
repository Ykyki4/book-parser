import json
import math
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from parse_tululu_category import parse_args


def on_reload():
    args = parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open(args.json_path, "r", encoding="utf-8") as my_file:
        books = json.load(my_file)

    page_chunk = 10
    col_chunk = 2

    for page, books_page_chunks in enumerate(list(chunked(books, page_chunk)), start=1):
        rendered_page = template.render(
            books_chunks=list(chunked(books_page_chunks, col_chunk)),
            pages_numb=math.ceil(len(books) / page_chunk),
            current_page=page
        )
        Path('pages').mkdir(parents=True, exist_ok=True)
        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == "__main__":
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
