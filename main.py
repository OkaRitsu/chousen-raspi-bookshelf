# -*- coding: utf-8 -*-

import time

from bookshelf_manager import BookShelfManager


def main():
    manager = BookShelfManager()
    try:
        while True:
            position = int(input('移動させる場所を指定してください（cm）: '))
            manager.move_and_lift_up(position)
            time.sleep(1)
    except:
        manager.stop()


if __name__ == '__main__':
    main()
