"""
Паттерн "Компоновщик"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Мост" - с. 196
"""
from abc import ABCMeta, abstractmethod


# Для примера будет реализована иерархия компонента, в книге в разделе "Пример кода" используется другой пример
# но он какой-то менее интересный
class Component(metaclass=ABCMeta):
    """
    Абстрактный класс для описания интерфейса, общего для листового и обычного узлов
    """

    @abstractmethod
    def multiple_size(self, x: float):
        """Увеличить размер"""

    @abstractmethod
    def add(self, other):
        """Добавить элемент"""

    @abstractmethod
    def remove(self, other):
        """Удалить элемент"""


class Composite(Component):
    """
    Класс, реализующий общую логику для представления узла, который может содержать в себе потомков
    """
    def __init__(self, height: float = None, weight: float = None):
        """
        Конструктор. Задает размеры
        :param height:
        :param weight:
        """
        self.height = height
        self.weight = weight
        self.children = []

    def multiple_size(self, x: float):
        """
        Изменить размер. Меняется размер всех потомков.
        :param x: множитель
        :return:
        """
        self.height *= x
        self.weight *= x
        print(f'Новые размеры для {self}: ({self.weight}, {self.height})')
        for child in self.children:
            child.multiple_size(x)

    def add(self, other):
        """
        Добавить потомка
        :param other: элемент для добавления
        :return:
        """
        if not other or other in self.children:
            return
        self.children.append(other)

    def remove(self, other):
        """
        Удалить потомка
        :param other: элемент для удаления
        :return:
        """
        if not other or other not in self.children:
            return
        self.children.remove(other)


class Leaf(Component):
    """
    Класс для представления элемента, который является листовым и не может содержать в себе потомков
    """

    def __init__(self, height: float = None, weight: float = None):
        """
        Конструктор. Задает размеры
        :param height:
        :param weight:
        """
        self.height = height
        self.weight = weight

    def multiple_size(self, x: float):
        """
        Изменить размер. Меняется размер всех потомков.
        :param x: множитель
        :return:
        """
        self.height *= x
        self.weight *= x
        print(f'Новые размеры для {self}: ({self.weight}, {self.height})')

    def add(self, other):
        """
        Добавить потомка
        :param other: элемент для добавления
        :return:
        """
        return

    def remove(self, other):
        """
        Удалить потомка
        :param other: элемент для удаления
        :return:
        """
        return


def use_by_client():

    # Сделаем примерную структуру окна приложения
    root_window = Composite(300, 300)
    root_window.add(title := Leaf(50, 50))
    root_window.add(text := Leaf(100, 50))
    root_window.add(widget := Composite(200, 200))
    widget.add(picture := Composite(10, 10))  # оставим картинку пустым узлом

    print('И теперь попробуем взаимодействовать')
    title.multiple_size(0.5)
    text.multiple_size(0.5)
    root_window.multiple_size(2)
    widget.multiple_size(3)
    picture.multiple_size(0.5)
    print('\n\n')

    # Попробуем поудалять без смысла
    title.remove(text)
    text.remove(title)
    widget.remove(root_window)

    # И со смыслом
    widget.remove(picture)
    root_window.remove(title)

    # И проверим, что удалились
    root_window.multiple_size(1.5)
    widget.multiple_size(0.5)


if __name__ == '__main__':
    use_by_client()
