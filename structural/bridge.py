"""
Паттерн "Мост"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Мост" - с. 184
"""
import random
from abc import ABCMeta, abstractmethod

from generating.singleton import singleton


class Window:
    """
    Класс абстракции. Реализует в себе высокоуровневые операции над объектом. В данном случае это окно.
    Окно может быть разное:
     - Окно приложения (ApplicationWindow)
     - Окно иконки (IconWindow)
     - Диалоговое окно и т.д...
    Эти окна реализованы в подклассах. Собой они дополняют интерфейс Window, потому что у нового типа окна появляются
    новые операции.

    Но конкретная реализация окна для разных платформ будет разная, поэтому конкретный код операций содержится в классе
    WindowImp и его подклассы реализуют этот код для разных платформ
    """
    def __init__(self):
        # вот именно это отношение и называется "Мостом", когда сама реализация у нас где-то в другом месте
        self._implementation = self.__get_implementation()

    def open(self):
        if not self._implementation:
            self._implementation = self.__get_implementation()
        standard_top_point, standard_bottom_point = (0, 0), (10, 10)
        self._implementation.imp_top(standard_top_point)
        self._implementation.imp_bottom(standard_bottom_point)
        self._implementation.device_rect()

    def close(self):
        if not self._implementation:
            self._implementation = self.__get_implementation()
        self._implementation.erase_rect()

    @staticmethod
    def __get_implementation():
        return WindowSystemFactory().get_implementation_for_system()

    @property
    def implementation_name(self):
        return self._implementation.__class__.__name__


class ApplicationWindow(Window):
    """
    Дополнение Window. Окно приложения. Класс расширяет интерфейс Window
    """
    def __init__(self, title=None):
        self.__title = title
        super().__init__()

    def draw_content(self):
        if not self._implementation:
            self._implementation = self.__get_implementation()
        self._implementation.print(self.__title)


class IconWindow(Window):
    """
    Окно иконки. Пусть этот класс сужает интерфейс родителя по своим каким-то правилам
    """
    def __init__(self, icon=None):
        self.__icon = icon
        super().__init__()

    def close(self):
        return


class WindowImp(metaclass=ABCMeta):
    """
    Класс реализации. Абстрактный
    В большинстве своем предоставляет низкоуровневые операции над объектом.
    """
    @abstractmethod
    def imp_top(self, point):
        pass

    @abstractmethod
    def imp_bottom(self, point):
        pass

    @abstractmethod
    def device_rect(self):
        pass

    @abstractmethod
    def erase_rect(self):
        pass

    @abstractmethod
    def print(self, value):
        pass


class XWindowImp(WindowImp):
    """
    Класс реализации для системы XWindow
    Здесь просто симулируем работу, пусть для XWindow будут выводиться принты на русском
    """
    def imp_top(self, point):
        print(f'Назначили верхнюю точку {point}')

    def imp_bottom(self, point):
        print(f'Назначили верхнюю точку {point}')

    def device_rect(self):
        print('Нарисовали прямоугольник по верхней и нижней точке')

    def erase_rect(self):
        print('Стерли прямоугольник')

    def print(self, value):
        print(value)


class PMWindowImp(WindowImp):
    """
    Класс реализации для системы PMWindow
    Здесь просто симулируем работу, пусть для XWindow будут выводиться принты на английском
    """
    def imp_top(self, point):
        print(f'Set top point {point}')

    def imp_bottom(self, point):
        print(f'Set bottom point {point}')

    def device_rect(self):
        print(f'Draw rectangle by top and bottom points')

    def erase_rect(self):
        print(f'Erased rectangle')

    def print(self, value):
        # Пусть операция print не поддерживается в PM
        pass


@singleton
class WindowSystemFactory:
    """
    Пример, как могут сочетаться паттерны - WindowSystemFactory должна быть одна, поэтому сделаем ее "Одиночкой"
    В описании примера приводится, что WindowSystemFactory - абстракная фабрика (что следует из названия), но тут все
    очень упрощенно
    Пример паттерна "Абстрактная фабрика" - generating/abstract_factory.py
    Пример паттерна "Одиночка" - generating/singleton.py
    """
    imps = {
        'X': XWindowImp(),
        'PM': PMWindowImp(),
    }

    def get_implementation_for_system(self):
        return random.choice(list(self.imps.values()))


# симулируем работу приложения
def check_result(window: Window):
    print(type(window))
    window.open()
    if isinstance(window, ApplicationWindow):
        window.draw_content()
    window.close()
    print('\n\n')


# Как итог у нас будет поддерживаться реализация 3 окон в 2 ОС
# Если бы не был использован паттерн мост, то пришлось бы писать классы, которые привязаны к конкретной ОС
# то есть XWindow, PMWindow, XApplicationWindow, PMApplicationWindow, XIconWindow, PMIconWindow
# мы написали 5 классов (не считая абстрактного WindowImp) вместо 6 возможных (выше упомянуто), сделали приложение
# более гибким
# А теперь представим, что нужно доработать наши окна под MacOS. Для этого с паттерном Мост мы напишем лишь 1 класс:
# MacWindowImp, а если бы не был использован паттерн, то пришлось бы писать MacWindow, MacApplicationWindow и
# MacIconWindow
if __name__ == '__main__':
    for window_class in (Window, ApplicationWindow, IconWindow):
        checked_systems = set()
        while len(checked_systems) < 2:
            window_ = window_class()
            if window_.implementation_name not in checked_systems:
                checked_systems.add(window_.implementation_name)
                check_result(window_)
