"""
Паттерн "Декоратор"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Декоратор" - с. 209
"""
from typing import Union


class VisualComponent:
    """
    Абстрактный класс представления визуального компонента, объявляющий его операции
    """
    def __init__(self, length: Union[float, int], width: Union[float, int]):
        self.length = length
        self.width = width

    def draw(self):
        raise NotImplementedError

    def resize(self, multiplier: Union[float, int]):
        raise NotImplementedError


class BaseDecorator(VisualComponent):
    """
    Абстрактный класс с базовой реализацией, декорирующий объекты VisualComponent
    От него наследуются конкретные декораторы
    """
    def __init__(self, component: VisualComponent):
        self.component = component
        super().__init__(self.component.width + 1, self.component.length + 1)

    def draw(self):
        self.component.draw()

    def resize(self, multiplier: Union[float, int]):
        self.component.resize(multiplier)


class Window(VisualComponent):
    """Класс окна"""

    def __init__(self, length: Union[float, int], width: Union[float, int]):
        super(Window, self).__init__(length, width)
        self.__content = None

    def draw(self):
        print('='*int(self.length))
        for i in range(int(self.width-2)):
            print("|" + ' '*int(self.length/2 - 1) + self.__get_content() + ' '*int(self.length/2 - 1) + '|')
        print('='*int(self.length))

    def resize(self, multiplier: Union[float, int]):
        self.length *= multiplier
        self.width *= multiplier
        self.draw()

    def set_content(self, content: VisualComponent):
        self.__content = content

    def __get_content(self):
        if self.__content:
            return self.__content.draw()
        return ' '


class BorderDecorator(BaseDecorator):
    """Декоратор, рисующий отдельную рамку из звездочек вокруг объекта"""
    def draw(self):
        self.__draw_border()
        self.component.draw()
        self.__draw_border()

    def __draw_border(self):
        print('*'*int(self.component.length))


class TextView(VisualComponent):
    """Поле ввода"""
    def __init__(self, text: str):
        super(TextView, self).__init__(0, 0)
        self.text = text

    def draw(self):
        return self.text

    def resize(self, multiplier: Union[float, int]):
        self.text = self.text * multiplier


def main():
    """Нарисовать окна"""

    print('Простой пример декоратора')
    Window(5, 5).draw()
    print('\n')
    BorderDecorator(Window(5, 5)).draw()

    print('\n\nДекораторы декорируют друг друга, при это еще есть контент')
    window = Window(10, 9)
    window.set_content(TextView('a'))
    BorderDecorator(window).draw()
    print('\n')
    BorderDecorator(BorderDecorator(window)).draw()


main()
