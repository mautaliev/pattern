"""
Паттерн "Адаптер"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Адаптер" - с. 171
"""

from dataclasses import dataclass


@dataclass
class Point:
    """Просто спомогательный класс для имитации точки"""
    x: int
    y: int


class Manipulator:
    """Просто вспомогательный класс для имитации мапипулятора"""
    def __init__(self):
        print(f"Создан манипулятор {self}")


class Shape:
    """
    Класс фигуры. Предположим, что наше приложение завязано на интерфейс данного класса
    """
    def __init__(self):
        self.bottom_left: Point or None = None
        self.top_right: Point or None = None

    def bounding_box(self, bottom_left, top_right):
        """Фигура определяется 2 противоположными прямоугольника"""
        self.bottom_left = bottom_left
        self.top_right = top_right

    def create_manipulator(self):
        """Создает мапипулятор - объект для управления текущей фигурой"""
        return Manipulator()

    def check_state(self):
        """Проверить состояние объекта"""
        print(f'Shape=({self.bottom_left, self.top_right})')


class TextView:
    """
    Стороннее решение с другим интерфейсом
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.weight = 0
        self.height = 0

    def get_origin(self, x, y):
        """Определить начальную точку объекта"""
        self.x = x
        self.y = y

    def get_extend(self, height, weight):
        """Определить высоту и ширину"""
        self.height = height
        self.weight = weight

    def get_info(self):
        return self.x, self.y, self.weight, self.height


class TextShape(Shape):
    """
    Адаптер. Используем стороннее решение и адаптируем его к нашему приложению
    """
    def __init__(self, text_view: TextView):
        self.text_view = text_view
        super(TextShape, self).__init__()

    def bounding_box(self, bottom_left, top_right):
        """В этой операции используем под капотом сторонее решение и адаптируем интерфейсы"""
        x, y = bottom_left.x, bottom_left.y
        weight = top_right.x - bottom_left.x
        height = top_right.y - bottom_left.y
        self.text_view.get_origin(x, y)
        self.text_view.get_extend(height, weight)

    def create_manipulator(self):
        """В используемом нами готовом решении такой операции нет, так что тут сами делаем"""
        return super().create_manipulator()

    def check_state(self):
        print(self.text_view.get_info())


def application_simulator(shape: Shape):
    """
    Симулятор работы приложения
    :param shape: фигура
    :return:
    """
    bottom_left = Point(0, 0)
    top_right = Point(10, 10)

    shape.bounding_box(bottom_left, top_right)
    shape.create_manipulator()
    shape.check_state()

    print('\n\n')


# Приложение для обычных фигур работает так
just_shape = Shape()
application_simulator(just_shape)

# А вот так приложение будет работать для новой фигуры с текстом, для которой под капотом используется сторонее решение
text_shape = TextShape(TextView())
application_simulator(text_shape)
