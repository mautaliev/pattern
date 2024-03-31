"""
Реализация паттерна "Абстрактная фабрика"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Абстракная фабрика" - с. 113
"""

__author__ = 'Мауталиев С. И.'

import random

from common import Wall, Door, Room, Maze, Direction


# Создадим класс абстракной фабрики для построения лабиринта
# В этой реализации абстракная фабрика будет и конкретной фабрикой, для создания простого лабиринта "без наворочек"
class MazeFactory:
    def __init__(self):
        pass

    @staticmethod
    def make_maze() -> Maze:
        """Создать лабиринт"""
        return Maze()

    @staticmethod
    def make_wall() -> Wall:
        """Создать стену"""
        return Wall()

    @staticmethod
    def make_room(room_no: int) -> Room:
        return Room(room_no)

    @staticmethod
    def make_door(room1: Room, room2: Room) -> Door:
        return Door(room1, room2)


# Создадим необходимые подклассы для первой конкретной фабрики
class EnchantedRoom(Room):
    """Зачарованная комната"""
    __spell_dict = {
        1: 'Абра-кадавра',
        2: 'Авада-кедавра',
        3: 'Фокус-покус',
    }

    def __init__(self, no: int, ):
        super().__init__(no)

        # Отличительная особенность конкретного продукта от абстракного
        # Пусть будет какая-то фигня в виде магической речи
        self.__spell = self.__cast_spell()

    def __cast_spell(self):
        return self.__spell_dict.get(random.randint(1, 3))


class EnchantedDoor(Door):
    """Зачарованная дверь"""
    __spell_dict = {
        1: 'Абра-кадавра',
        2: 'Авада-кедавра',
        3: 'Фокус-покус',
    }

    def __init__(self, door1: EnchantedRoom, door2: EnchantedRoom):
        super().__init__(door1, door2)

        # Отличительная особенность конкретного продукта от абстракного
        # Пусть будет какая-то фигня в виде магической речи
        self.__spell = self.__cast_spell()

    def __cast_spell(self):
        return self.__spell_dict.get(random.randint(1, 3))

    def enter(self, **kwargs):
        if kwargs.get('spell') == self.__spell:
            super().enter(**kwargs)
        else:
            print('Не удалось открыть дверь!')


# Конкретная фабрика создает конкретную реализацию наших объектов по интерфейсу, представляемым абстракной
class EnchantedMazeFactory(MazeFactory):
    @staticmethod
    def make_room(room_no: int) -> EnchantedRoom:
        return EnchantedRoom(room_no)

    @staticmethod
    def make_door(room1: EnchantedRoom, room2: EnchantedRoom) -> EnchantedDoor:
        return EnchantedDoor(room1, room2)


# Создадим конкретные продукты для второй конкретной фабрики
class BombedWall(Wall):
    def __init__(self):
        super().__init__()

        # Эта стена может взрываться, а значит имеет прочность
        self.__durability = 100

    def blew_up(self, damage):
        self.__durability -= damage


class RoomWithBomb(Room):
    def __init__(self, no: int):
        super().__init__(no)

        # Пусть в этой комнате будет бомба с рандомным уроном
        self.__bomb_damage = random.randint(1, 200)

    def enter(self):
        # При входе в эту комнату стены могут взорваться
        # Паттерн обеспечивает нам то, что у всех стен этой комнаты будет метод blew_up
        for direction in self.__navigation:
            if type(self.get_side(direction)) == BombedWall:
                self.get_side(direction).blew_up(self.__bomb_damage)
        super().enter()


# Создадим вторую конкретную фабрику, стены которой могут взрываться
class BombedMazeFactory(MazeFactory):
    @staticmethod
    def make_wall() -> BombedWall:
        return BombedWall()

    @staticmethod
    def make_room(room_no: int) -> RoomWithBomb:
        return RoomWithBomb(room_no)


def create_maze(factory: MazeFactory) -> Maze:
    """
    Создать лабиринт
    :param factory: фабрика создания лабиринта
    :return: лабиринт
    """
    print(f'Создаем лабиринт фабрикой {type(factory)}')

    maze = factory.make_maze()
    room1 = factory.make_room(1)
    room2 = factory.make_room(2)
    door = factory.make_door(room1, room2)

    maze.add_room(room1)
    maze.add_room(room2)

    room1.set_side(Direction.NORTH, factory.make_wall())
    room1.set_side(Direction.EAST, door)
    room1.set_side(Direction.SOUTH, factory.make_wall())
    room1.set_side(Direction.WEST, factory.make_wall())

    room2.set_side(Direction.NORTH, factory.make_wall())
    room2.set_side(Direction.EAST, factory.make_wall())
    room2.set_side(Direction.SOUTH, factory.make_wall())
    room2.set_side(Direction.WEST, door)

    print('\n\n\n')

    return maze


# Теперь мы можем спокойно вызывать функцию create_maze с разными конкретными фабриками и знать, что ничего не упадет
# Ведь фабрика обеспечивает нам то, что объекты будут обязательно совместимы друг с другом
maze1 = create_maze(MazeFactory())
maze2 = create_maze(EnchantedMazeFactory())
maze3 = create_maze(BombedMazeFactory())
