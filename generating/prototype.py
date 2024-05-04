"""
Паттерн "Прототип"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Прототип" - с. 146
"""

__author__ = 'Мауталиев С. И.'

import random
from copy import deepcopy

# функцию создания лабиринта просто скопируем уже существующую, логика не меняется
from abstract_factory import create_maze
from common import MapSite, Maze as MazeBase, Direction, print_obj_type


# Здесь нам потребуются новые классы-прототипы для дверей, комнат и т.д...

# Реализуем только логику прототипирования, остальное уже написано в MazeBase
class Maze(MazeBase):
    def __init__(self, other=None):
        super().__init__()
        if other:
            self.__rooms = deepcopy(other.__rooms)

    def clone(self):
        return Maze(self)


# А классы-прототипы дверей, комнат и т.д... перепишем, так как их логика поменяется сильнее
class Wall(MapSite):
    def __init__(self, other=None):
        print_obj_type(other or self)

    def clone(self):
        return Wall(self)

    def enter(self):
        pass


class BombedWall(Wall):
    def __init__(self, other=None):
        self.durability = 100
        if other:
            self.durability = other.durability
        super().__init__(other)

    def clone(self):
        return BombedWall(self)


class Room(MapSite):
    def __init__(self, other=None):
        self.navigation = Direction.get_navigation()
        self.room_no = None
        if other:
            self.navigation = other.navigation
            self.room_no = other.room_no
        print_obj_type(other or self)

    def initialize(self, no: int):
        self.room_no = no

    def enter(self):
        pass

    def get_side(self, direction: Direction) -> MapSite:
        return self.navigation.get(direction)

    def set_side(self, direction: Direction, obj: MapSite):
        self.navigation[direction] = obj

    def clone(self):
        return Room(self)


class RoomWithABomb(Room):
    def __init__(self, other=None):
        self.bomb_damage = random.randint(1, 200)
        if other:
            self.bomb_damage = other.bomb_damage
        super().__init__()


class Door(MapSite):
    def __init__(self, other=None):
        self.__room1 = None
        self.__room2 = None
        if other:
            # не понимаю, почему не упало, из-за этого даже задал свой первый вопрос на стак оверфлоу
            # https://ru.stackoverflow.com/questions/1578964/why-i-can-refer-to-private-attribute-of-an-object-python
            # и еще на англ. версии такой же
            self.__room1 = other.__room1
            self.__room2 = other.__room2
        print_obj_type(other or self)

    def initialize(self, room1: Room, room2: Room):
        """Опускаем инициализацию из конструктора в отдельный метод"""
        self.__room1 = room1
        self.__room2 = room2

    def clone(self):
        """Клонировать объект"""
        return Door(self)

    def enter(self):
        print('Открыли дверь между комнатами {r1} и {r2}'.format(r1=self.__room1.number, r2=self.__room2.number))


class MazePrototypeFactory:
    def __init__(self, maze: Maze, wall: Wall, room: Room, door: Door):
        self.__prototype_maze = maze
        self.__prototype_wall = wall
        self.__prototype_room = room
        self.__prototype_door = door
        super().__init__()

    def make_wall(self) -> Wall:
        return self.__prototype_wall.clone()

    def make_door(self, r1: Room, r2: Room) -> Door:
        door = self.__prototype_door.clone()
        door.initialize(r1, r2)
        return door

    def make_room(self, no) -> Room:
        room = self.__prototype_room.clone()
        room.initialize(no)
        return room

    def make_maze(self) -> Maze:
        return self.__prototype_maze.clone()


# Очень интересно, что по факту мы собираем по частям нужную нам "фабрику" через наборы прототипов
simple_maze_factory = MazePrototypeFactory(
    Maze(), Wall(), Room(), Door()
)
bombed_maze_factory = MazePrototypeFactory(
    Maze(), BombedWall(), RoomWithABomb(), Door()
)
# И даже так)) Хотя BombedWall и Room не сочитались раньше, тут это возможно, хоть и бесмысленно
strange_maze_factory = MazePrototypeFactory(
    Maze(), BombedWall(), Room(), Door()
)


create_maze(simple_maze_factory)
create_maze(bombed_maze_factory)
create_maze(strange_maze_factory)
