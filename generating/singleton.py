"""
Паттерн "Одиночка"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Одиночка" - с. 157
"""

__author__ = 'Мауталиев С. И.'


# На этот раз мне надоело переписывать уже существующую логику фабрик (как я делал в примете "Прототип"),
# поэтому реализуем только часть, ответственную за логику данного паттерна
from abstract_factory import MazeFactory, BombedMazeFactory, EnchantedMazeFactory, create_maze


# В самом учебнике более подробная реализация с наследованием, а здесь же просто декоратор навесим на класс
def singleton(class_):
    """Декоратор для того, чтобы класс был объявлен в приложении только единожды"""
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


# По сути, в рассматриваемом примере из книги синглтон вообще и не нужен, но они просто показывают, что фабрика
# лабиринта по логике должна быть только 1 на все приложение, и это реализуется через паттерн
@singleton
class MazeFactorySingleton(MazeFactory):
    pass


@singleton
class BombedFactorySingleton(BombedMazeFactory):
    pass


@singleton
class EnchantedFactorySingleton(EnchantedMazeFactory):
    pass


# Дважды создаем объект, а это одно и то же, если нет, то ошибка
if not MazeFactorySingleton() is MazeFactorySingleton():
    raise Exception('Not a singleton!')
if not BombedFactorySingleton() is BombedFactorySingleton():
    raise Exception('Not a singleton!')
if not EnchantedFactorySingleton() is EnchantedFactorySingleton():
    raise Exception('Not a singleton!')


# Проверим, что основной функционал фабрик не поломался
create_maze(MazeFactorySingleton())
create_maze(BombedMazeFactory())
create_maze(EnchantedMazeFactory())

