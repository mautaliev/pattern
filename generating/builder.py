"""
Паттерн "Строитель"

Паттерн состоит из:
 - Распорядителя
 - Строителя (MazeBuilder)

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Строитель" - с. 124
"""

__author__ = 'Мауталиев С. И.'

from typing import Optional, Type

from common import Maze, Room, Direction, Wall, Door


class MazeBuilder:
    """
    Класс строителя. Абстракный.
    В себе содержит интерфейсы для конкретных строителей, которые позволяют создавать отдельные части продукта
    """

    def build_maze(self):
        """Построить лабиринт"""

    def build_room(self, room_no: int):
        """Построить комнату"""

    def build_door(self, room1: int, room2: int):
        """Построить дверь"""

    def get_maze(self) -> Maze:
        """Вернуть лабиринт"""
        raise NotImplementedError


class StandardMazeBuilder(MazeBuilder):
    """
    Класс строителя для постройки обычного лабиринта
    """
    def __init__(self):
        self.__maze: Optional[Maze] = None

    def build_maze(self):
        self.__maze = Maze()

    def build_room(self, room_no: int):
        if self.__maze.get_room(room_no):
            return
        room = Room(room_no)
        room.set_side(Direction.NORTH, Wall())
        room.set_side(Direction.SOUTH, Wall())
        room.set_side(Direction.EAST, Wall())
        room.set_side(Direction.WEST, Wall())
        self.__maze.add_room(room)

    def build_door(self, room1: int, room2: int):
        rooms = {room_no: self.__maze.get_room(room_no) for room_no in (room1, room2)}
        for no, obj in rooms.items():
            if obj is None:
                raise ValueError(f'Не существует комнаты с номером {no}')
        r1, r2 = rooms[room1], rooms[room2]
        door = Door(r1, r2)
        r1.set_side(self.__get_common_wall(r1, r2), door)
        r2.set_side(self.__get_common_wall(r2, r1), door)

    def get_maze(self) -> Maze:
        return self.__maze

    @staticmethod
    def __get_common_wall(room1: Room, room2: Room) -> Direction:
        for way in Direction:
            side_room1 = room1.get_side(way)
            side_room2 = room2.get_side(way)
            if side_room1 and side_room2 and isinstance(side_room1, Wall) and isinstance(side_room2, Wall):
                return way
        raise ValueError('Между дверьми нет возможных общих стен')


class CountingMazeBuilder(MazeBuilder):
    """
    Строитель, который только подсчитывает количество компонентов разного вида, которые могли бы быть созданы
    """
    def __init__(self):
        self.__rooms = self.__doors = 0

    def build_room(self, room_no: int):
        self.__rooms += 1

    def build_door(self, room1: int, room2: int):
        self.__doors += 1

    def get_maze(self) -> None:
        rooms, doors = self.get_counts()
        print('В лабиринте есть {rooms} комнат и {doors} дверей'.format(rooms=rooms, doors=doors))
        return None

    def get_counts(self):
        return self.__rooms, self.__doors


def create_maze(builder: MazeBuilder) -> Maze:
    print('Builder: {}'.format(type(builder)))
    builder.build_maze()
    builder.build_room(1)
    builder.build_room(2)
    builder.build_door(1, 2)
    maze = builder.get_maze()
    print('\n')
    return maze


create_maze(StandardMazeBuilder())
create_maze(CountingMazeBuilder())
