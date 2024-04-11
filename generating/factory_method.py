"""
Фабричный метод

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Фабричный метод" - с. 135
"""

__author__ = 'Мауталиев С. И.'

from abstract_factory import create_maze, BombedWall, RoomWithBomb, EnchantedRoom, EnchantedDoor
from common import Maze, Room, Wall, Door


# Как я понял, главным отличием "Фабричного метода" (А) от "Абстрактной фабрики" (Б) является то, что Б предоставляет
# инструментарий, т.е. клиент использует фабрику чтобы получать какие-то части продукта, чтобы самому в итоге построить
# продукт, а в А клиент сразу использует фабрику для получения готового продукта
# (но может я и ошибаюсь)
class MazeGame:
    """Фабрика. Создает продукт - лабиринт. В конкретном случае является и абстрактной, и конкретной"""
    def create_maze(self) -> Maze:
        """Создадим лабиринт. Этот метод называется фабричным"""
        # Так как паттерн в целом похож на абстрактную фабрику
        # Чтобы не писать лишний код, просто переиспользуем уже написанный код создания лабиринта
        # Благо интерфейсы совпадают
        return create_maze(self)

    def make_maze(self) -> Maze:
        return Maze()

    def make_room(self, no: int) -> Room:
        return Room(no)

    def make_wall(self) -> Wall:
        return Wall()

    def make_door(self, room1: Room, room2: Room) -> Door:
        return Door(room1, room2)


class BombedMazeGame(MazeGame):
    """Конкретная фабрика. Создает лабиринт с бомбами"""

    # Все классы уже были созданы в Абстракной фабрике, так что просто вернем их
    def make_wall(self) -> Wall:
        return BombedWall()

    def make_room(self, no: int) -> Room:
        return RoomWithBomb(no)


class EnchantedMazeGame(MazeGame):
    """Конкретная фабрика 2. Создает зачарованный лабиринт"""

    def make_room(self, no: int) -> Room:
        return EnchantedRoom(no)

    def make_door(self, room1: EnchantedRoom, room2: EnchantedRoom) -> Door:
        return EnchantedDoor(room1, room2)


MazeGame().create_maze()
BombedMazeGame().create_maze()
EnchantedMazeGame().create_maze()
