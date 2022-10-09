# book-parser

Утилита используется для автоматического скачивания книг с сайта [tululu.org](https://tululu.org) и для последующего просмотра их на собственном сайте.

## Установка
1. Скачайте python3.
1. Изолируйте проект с помощью pipenv/venv.
1. Используйте pip для установки всех пакетов:

    ```pip install -r requirements.txt```

## Использование

Когда вы уже установили утилиту: 
* Зайдите в терминал (Если у вас Windows, надо найти приложение cmd в поиске пуск) 
* Перейдите в папку с утилитой с помощью команду `cd путь`
### В репозитории существует два скрипта:
 
#### tululu.py

Запускайте скрипт с двумя аргументами, первый это от какого id книги скачивать, второй до какого. Пример команды:
    
 ```python tululu.py 20 30```
    
После чего, в терминал будет выводиться название книги и её жанры, если книги под таким id не существует, в терминал выведется это. В папке с скриптом, будут созданы две папки books, images, далее в папку books скачается книга в txt формате, а в папку images скачается картинка в png, если картинки нет, скачается nopic.gif 
#### parse_tululu_category.py

У скрипта есть 6 аргументов:

* --start_page с какой страницы начинать скачивать книги и --end_page на какой заканчивать, если вы не указываете до какой, то будет скачиваться до последней. 
* --dest_folder путь к каталогу куда скачивать все данные, по умолчанию путь скрипта. 
* --skip_txt и --skip_imgs, отвечают за то, пропускать ли скачивание книг или картинок, по умолчанию False.
* --json_path, путь к файлу .json куда записывать все данные о книгах, по умолчанию books_info.json в каталоге с скриптом.

Примеры команды:
    
  ```python parse_tululu_category.py -start 400 -end 501 --skip_imgs```
    
Скачивается с 400 по 500 страницу, картинки пропускаются

 ```python parse_tululu_category.py -start 600 --skip_txt --dest_folder C:\my_books```
    
Скачивается с 600 по 701 страницу, пропускаются книги, путь указан

Скачивание данных происходит также как и в предыдущем скрипте, за исключением того что появляется json файл с информацией по каждой книге, и в терминал выводится лишь текущая страница.

После того как вы уже получили json, запускайте скрипт **render_website.py**, никаких аргументов он не принимает, при помощи данных из json и **template.html** он сделает для вас папку pages с страницами ввиде **index{page}.html**, кол-во страниц варьируется от количества книг которых вы скачали, на каждой странице по 10 книг. 
Пока скрипт запущен, вы можете посетить сайт по ссылке http://127.0.0.1:5500/pages/index1.html или любое другое значение страницы вместо 1. 

Также, вы можете посмотреть некоторое количество книг по ссылке https://ykyki4.github.io/book-parser/pages/index1.html.
