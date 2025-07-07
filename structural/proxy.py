"""
Паттерн "Заместитель"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Приспособленец" - с. 246
"""
import datetime
from time import sleep


# Есть некий класс графического объекта, который можно отрисовать
class Graphic:
    def draw(self):
        pass

    def load(self):
        pass

    def save(self):
        pass


# Есть класс Изображение, который отвечает за отображение изображения, но при инициализации экземпляра происходит
# долгая операция загрузки в память изображения (метод load)
# Задача: оптимизировать загрузку страницы, отложив вызов load
class Image(Graphic):
    def __init__(self, path):
        self.path = path
        self.file = self.load()

    def load(self):
        sleep(3)

    def draw(self):
        print('Отобразили объект')


# Реализуем заместитель, который будет создавать экземпляр класса-субъекта только при вызове конечной операции
class ImageProxy(Graphic):
    def __init__(self, path):
        self.path = path
        self.__subject = None

    def draw(self):
        return self.subject.draw()

    def load(self):
        return self.subject.load()

    @property
    def subject(self):
        if self.__subject:
            return self.__subject
        self.__subject = Image(self.path)
        return self.__subject


# Посмотрим, как нам поможет загрузка
# В данном случае мы быстрее прогрузим страницу, т.к. загрузка файла вызовется отложенно
def main():
    print('Без использования заместителя')
    start = datetime.datetime.now()
    image = Image('anypath')
    end = datetime.datetime.now()
    print(f'Загрузка страницы закончена через {end-start}')
    start = datetime.datetime.now()
    image.draw()
    end = datetime.datetime.now()
    print(f'Отрисовка документа закончена через {end-start}\n\n')

    print('С использованием заместителя')
    start = datetime.datetime.now()
    image = ImageProxy('anypath')
    end = datetime.datetime.now()
    print(f'Загрузка страницы закончена через {end-start}')
    start = datetime.datetime.now()
    image.draw()
    end = datetime.datetime.now()
    print(f'Отрисовка документа закончена через {end-start}\n\n')


if __name__ == '__main__':
    main()