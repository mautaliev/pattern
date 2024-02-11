"""
Прикладные хелперы
"""

__author__ = 'Мауталиев С. И.'


from typing import Callable, Optional, Any


def except_error(return_value: Optional[Any] = None):
    def decorator(function: Callable):
        """
        Декоратор, который при ошибке функции возвращает определенное значение, по умолчанию None
        :param function:
        :return:
        """
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
            except:
                result = return_value
            return result
        return wrapper
    return decorator


def print_obj_type(object_: Any):
    print(f'Создан экземпляр класса {type(object_)}')
