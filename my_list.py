from dataclasses import dataclass


class MagicList(list):

    def __init__(self, *args, cls_type=None,  **kwargs):
        super(MagicList, self).__init__(*args, **kwargs)
        self.cls_type = cls_type

    def __getitem__(self, key: str):
        if self.cls_type:
            self.__setitem__(key, None)
        return super().__getitem__(key)

    def __check_value(self, value):
        return self.cls_type() if self.cls_type else value

    def __setitem__(self, key: str, value):
        if len(self) > key:
            super().__setitem__(key, value)
        elif len(self) == key:
            self.append(self.__check_value(value))
        else:
            raise IndexError('list index out of range 1')


@dataclass
class Person:
    age: int = 1


my_list = MagicList(cls_type=Person)
my_list[0].age = 5

print(my_list)

