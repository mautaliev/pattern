"""
Реализация паттерна "Абстрактная фабрика"

Предположим, что у нас есть приложения для создания лабиринта.
Объявим следующие сущности:
 - MapSite (часть лабиринта)
   - Комната
   - Стена
   - Дверь
 - Maze (лабиринт)
"""

__author__ = 'Мауталиев С. И.'

from abc import ABCMeta, abstractmethod
from enum import IntEnum


class Direction(IntEnum):
    NORTH = 1
    EAST = 3
    SOUTH = 5
    WEST = 7

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
    def __init__(self):
        self.__navigation = Direction.get_navigation()

    def enter(self):
        pass

    def get_side(self, direction: Direction) -> MapSite:
        return self.__navigation.get(direction)

    def set_side(self, direction: Direction, obj: MapSite):
        self.__navigation[direction] = obj


class Wall(MapSite):
    def enter(self):
        pass


class Door(MapSite):
    def enter(self):
        pass


class Maze:
    pass