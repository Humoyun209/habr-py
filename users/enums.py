from enum import Enum


class WorkLoad(Enum):
    FULL_TIME = 'Полный рабочий день'
    PART_TIME = 'Неполный рабочий день'
    

class Level(Enum):
    INTERN = 'Стажер (Intern)'
    JUNIOR = 'Младший (Junior)'
    MIDDLE = 'Средний (Middle)'
    SENIOR = 'Старший (Senior)'
    LEAD = 'Ведущий (Lead)'
