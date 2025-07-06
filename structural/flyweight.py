"""
Паттерн "Приспособленец"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Приспособленец" - с. 231
"""

# Библиотека для разноцветного вывода в консоль
from colorama import init, Fore, Back, Style

from dataclasses import dataclass

from generating.singleton import singleton


class Glyph:
    """
    Класс для отображения графических объектов (в данный момент - это символы)
    Используется паттерн Компоновщик (см. в .composite.py)
    """

    def draw(self, glyph_context) -> None:
        """
        Отобразить свое содержимое в окне
        :param glyph_context: контекст
        :return:
        """

    def insert(self, glyph, glyph_context):
        """
        Добавить подобъект
        :param glyph: подобъект
        :param glyph_context: контекст
        :return:
        """


class Character(Glyph):
    """
    Символ. Графический объект без вложенности
    """
    def __init__(self, char):
        """Конструктор"""
        self.__char = char

    def draw(self, glyph_context) -> None:
        """Отобразить символ"""
        print(glyph_context.get() + self.__char)


class Group(Glyph):
    """Группа символов. Графический объект без вложенности"""
    def __init__(self):
        """Конструктор"""
        self.__storage = []

    def draw(self, glyph_context) -> None:
        """
        Нарисовать графический объект
        :param glyph_context:
        :return:
        """
        for item, context in self.__storage:
            item.draw(context or glyph_context)

    def insert(self, glyph, glyph_context=None):
        """
        Добавить графический объект в группу
        :param glyph:
        :param glyph_context:
        :return:
        """
        self.__storage.append((glyph, glyph_context))


@singleton
class GlyphFactory:
    """
    Фабрика графических объектов. См. паттерн "Одиночка" в generating/singleton.py
    """
    def __init__(self):
        """Конструктор"""
        self.__storage = {}
        self.__call_counter = 0

    def get(self, character: str) -> Character:
        """
        Получить приспособленца
        :param character: символ приспособленца
        :return: приспособленец
        """
        self.__call_counter += 1
        if obj := self.__storage.get(character):
            return obj
        obj = Character(character)
        self.__storage[character] = obj
        return obj

    def get_pattern_profit(self):
        """
        Узнать, какой результат дало использование паттерна
        :return:
        """
        print(f'Использование паттерна приспособленец помогло '
              f'создать {len(self.__storage)} объектов Glyph вместо {self.__call_counter}')


@dataclass
class Context:
    """Контекст графического объекта. Тоже по факту является приспособленцем"""
    font: Fore
    back: Back
    style: Style

    def get(self):
        return (self.font or '') + (self.back or '') + (self.style or '')


@dataclass
class ContextFactory:
    """
    Фабрика графических объектов. См. паттерн "Одиночка" в generating/singleton.py
    """
    def __init__(self):
        """Конструктор"""
        self.__storage = {}
        self.__call_counter = 0

    def get(self, fore: Fore, back: Back, style: Style) -> Context:
        """
        Получить приспособленца
        """
        self.__call_counter += 1
        if obj := self.__storage.get((fore, back, style)):
            return obj
        obj = Context(fore, back, style)
        self.__storage[(fore, back, style)] = obj
        return obj

    def get_pattern_profit(self):
        """
        Узнать, какой результат дало использование паттерна
        :return:
        """
        print(f'Использование паттерна приспособленец помогло '
              f'создать {len(self.__storage)} объектов Context вместо {self.__call_counter}')


def main():
    """
    Имитируем работу клиента
    :return:
    """

    # Клиент объявляет фабрику, для того, чтобы получать графические объекты
    glyph_factory = GlyphFactory()
    context_factory = ContextFactory()
    # Строит строку следующим образом
    string = Group()
    # Каждому символу можно задать свой контекст
    string.insert(glyph_factory.get('H'), context_factory.get(Fore.RED, Back.GREEN, Style.BRIGHT))
    string.insert(glyph_factory.get('e'), context_factory.get(Fore.WHITE, Back.GREEN, Style.NORMAL))
    string.insert(glyph_factory.get('l'), context_factory.get(Fore.RED, Back.GREEN, Style.BRIGHT))
    string.insert(glyph_factory.get('l'), context_factory.get(Fore.RED, Back.GREEN, Style.BRIGHT))
    string.insert(glyph_factory.get('o'), context_factory.get(Fore.WHITE, Back.GREEN, Style.NORMAL))
    string.insert(glyph_factory.get(' '), context_factory.get(Fore.WHITE, Back.BLUE, Style.NORMAL))
    string.insert(glyph_factory.get('w'), context_factory.get(Fore.GREEN, Back.WHITE, Style.NORMAL))
    string.insert(glyph_factory.get('o'), context_factory.get(Fore.RED, Back.GREEN, Style.BRIGHT))
    string.insert(glyph_factory.get('r'), context_factory.get(Fore.GREEN, Back.WHITE, Style.NORMAL))
    string.insert(glyph_factory.get('l'), context_factory.get(Fore.GREEN, Back.WHITE, Style.NORMAL))
    string.insert(glyph_factory.get('d'), context_factory.get(None, None, None))
    string.draw(context_factory.get(Fore.CYAN, None, None))

    glyph_factory.get_pattern_profit()
    context_factory.get_pattern_profit()


if __name__ == '__main__':
    main()
