"""
Общие классы для показания работы паттернов

Предположим, что у нас есть приложения для создания лабиринта.
Объявим следующие сущности:
 - MapSite (часть лабиринта)
   - Комната
   - Стена
   - Дверь
 - Maze (лабиринт)

См. ведение в контекст (что за лабиринт используется) - с. 108
"""

__author__ = 'Мауталиев С. И.'


from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import NoReturn

from helpers import except_error, print_obj_type


class Direction(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    @classmethod
    def get_navigation(cls) -> dict:
        return {way: None for way in cls}


class MapSite(object):
    """Часть лабиринта. Абстрактный"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def enter(self):
        """Войти"""


class Room(MapSite):
    """Комната"""
    def __init__(self, no: int):
        self.__navigation = Direction.get_navigation()
        self.__room_no = no
        print_obj_type(self)

    def enter(self):
        pass

    def get_side(self, direction: Direction) -> MapSite:
        return self.__navigation.get(direction)

    def set_side(self, direction: Direction, obj: MapSite):
        self.__navigation[direction] = obj


class Maze:
    """Лабиринт"""
    def __init__(self):
        self.__rooms = []

    def add_room(self, room: Room) -> NoReturn:
        self.__rooms.append(room)

    @except_error
    def get_room(self, n: int) -> Room:
        return self.__rooms[n]