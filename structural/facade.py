"""
Паттерн "Фасад"

 Подробности см. в книге "Паттерны объектно-ориентированного проектирования" Э. Гамма и др., 2022
 Паттерн "Фасад" - с. 221
"""

# Допустим, у нас имеется подсистема "Компилятор", которая состоит из множества классов: Сканер, парсер и т.д...
# В целом, все эти отдельно взятые классы предоставляют огромные возможности для клиента, но они очень сложные.
# Большинству клиентов нужны простые операции, им не интересно, что выполняется внутри. Для этого им и создается фасад,
# который предоставляет им простой интерфейс, не вдаваясь в детали, что происходит внутри.
# Но часть клиентов все еще может использовать внутренние классы для своих нужд


class Compiler:
    """
    Класс компилятора
    """
    def compile(self, program: str):
        scanner = Scanner(program)
        scanner.scan()
        parser = Parser()
        parser.parse(program)
        Executor(parser, SyntaxAnalyzer()).execute(scanner)


class Scanner:
    """Сканер"""
    def __init__(self, program):
        self.program = program

    def scan(self):
        print(f'Сканирую текст: {self.program}')


class Parser:
    """Парсер"""
    def parse(self, program):
        print(f'Разбираю текст: {program}')


class SyntaxAnalyzer:
    """Синтаксический анализатор"""
    def analyze(self, scanner: Scanner) -> bool:
        # Навесим какое-то условие
        return 'э' not in scanner.program


class Executor:
    """Выполнитель"""
    def __init__(self, parser, syntax_analyzer):
        self.parser = parser
        self.syntax_analyzer = syntax_analyzer

    def execute(self, scanner):
        if self.parser and self.syntax_analyzer.analyze(scanner):
            print(scanner.program)


def main():
    print('Клиент может, конечно, делать все сам:')
    program = 'Экивоки'
    scanner = Scanner(program)
    scanner.scan()
    parser = Parser()
    parser.parse(program)
    Executor(parser, SyntaxAnalyzer()).execute(scanner)

    print('\n\nА может не париться:')
    Compiler().compile(program)


main()
