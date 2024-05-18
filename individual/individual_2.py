#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import pathlib

"""
Необходимо разработать аналог утилиты «three» в Linux. 
Необходимо использовать возможности модуля «argparse» для управления отображением 
дерева каталогов файловой системы и добавить дополнительные уникальные возможности в программу.
Программа должна выводить дерево каталогов и файлов при указании в качестве параметра пути к каталогу.
"""


def tree(directory, args, prefix="", level=0):
    """
    Функция, которая рекурсивно выводит содержимое каталога.
    """

    # Получение содержимого текущего каталога
    contents = list(directory.iterdir())

    # Если задан параметр --directory, то выводятся только каталоги
    if args.directory:
        filtered_contents = []
        for file in contents:
            if file.is_dir():  # Проверка текущего объекта
                filtered_contents.append(file)
        contents = filtered_contents

    # Если задан --file, выводятся только файлы.
    if args.file:
        filtered_contents = []
        for file in contents:
            if file.is_file():  # Проверка объекта на то, является ли он файлом
                filtered_contents.append(file)
        contents = filtered_contents

    '''
    Команда tree обычно использовала декорации, чтобы показать дерево каталогов.
    Подсчитывается количество файлов в текущем каталоге.
    Перед последним ставится декорация └──.
    '''

    decoration = ["├── "] * (len(contents) - 1) + ["└── "]

    # Анализ и вывод полученных данных
    for pointer, path in zip(decoration, contents):
        print(prefix + pointer + path.name)
        # Если текущий элемент - каталог, то вызывается функция tree для этого каталога
        if path.is_dir():
            # Определение украшения для вложенных элементов (| или отступ)
            if pointer == "├── ":
                extension = "│   "
            else:
                extension = "    "
            tree(path, args, prefix=prefix + extension, level=level + 1)


def main(command_line=None):
    """
    Главная функция программы.
    """
    # Создать основной парсер командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to list."
    )

    # Необходимо запретить одновременное использование --file и --directory
    choose = parser.add_mutually_exclusive_group()
    # Выводятся только каталоги
    choose.add_argument(
        "--directory",
        action="store_true",
        help="List directories only."
    )
    # Выводятся только файлы
    choose.add_argument(
        "--file",
        action="store_true",
        help="List files only."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.0.1"
    )

    # Разбор аргументов командной строки
    args = parser.parse_args(command_line)
    try:
        directory = pathlib.Path(args.directory).resolve(strict=True)
    except FileNotFoundError:
        print("Этот файл не был найден!", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    tree(directory, args)


if __name__ == "__main__":
    main()
