import random

class Ship:
    def __init__(self, ship_class, ship_coords):

        if ship_class == 2:
            if not ((ship_coords[1][0] == (ship_coords[0][0] + 1))
                    or (ship_coords[1][1] == (ship_coords[0][1] + 1))):
                raise Exception('Некорректные координаты для корабля с двумя палубами! Ячейки должны быть неразрывными и вводтся слева на право или сверху вниз')

        if ship_class == 3:
            if not ((ship_coords[1][0] == (ship_coords[0][0] + 1) and ship_coords[2][0] == (ship_coords[1][0] + 1))
                    or (ship_coords[1][1] == (ship_coords[0][1] + 1) and ship_coords[2][1] == (ship_coords[1][1] + 1))):
                raise Exception('Некорректные координаты для корабля с тремя палубами! Ячейки должны быть неразрывными и вводтся слева на право или сверху вниз')

        self._ship_class = ship_class
        self._ship_coords = ship_coords
        if ship_class == 1:
            self._max_health = 1
            self._health = 1
        elif ship_class == 2:
            self._max_health = 2
            self._health = 2
        elif ship_class == 3:
            self._max_health = 3
            self._health = 3
        else:
            raise ValueError('Unknown ship class!')
        self._status = 'alive'
        self._destroyed = False

    def __str__(self):
        return f'Класс корабля - {self._ship_class}. Текущий статус - {self._status}. Координаты корабля - {self._ship_coords}'

    @property
    def ship_coords(self):
        return self._ship_coords

    @property
    def is_destroyed(self):
        return self._destroyed

    def shoted(self):
        self._health -= 1
        if self._health == 0:
            self._destroyed = True
            self._status = 'Destroyed'
        elif self._health < self._max_health and self._health > 0:
            self._status = 'Injured'

class Desk:
    def __init__(self, player_name):
        self._pole = [['O' for y in range(1, 7)] for x in range(1, 7)]
        self._player_name = player_name
        self._ships = []

    def __str__(self):
        str_repr = f'Поле игрока {self._player_name}\n'
        str_repr += '  | 1 | 2 | 3 | 4 | 5 | 6\n'
        for i in range(1, 7):
            str_repr += f'{i} | ' + ' | '.join(self._pole[i - 1]) + '\n'

        return str_repr

    @property
    def get_player_name(self):
        return self._player_name

    def add_ship(self, ship):
        for x, y in ship.ship_coords:
            if x not in range(1, 7) or y not in range(1, 7):
                raise Exception(f'Указана некорректная координата {x}, {y} для корабля.')

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (x + i) not in range(0, 6) or (y + j) not in range(0, 6):
                        continue
                    if self._pole[x + i - 1][y + j - 1] in [chr(8718)]:
                        raise Exception(f'Клетка {x}, {y} уже занята, укажите другие координаты')

        self._ships.append(ship)
        for x, y in ship.ship_coords:
            self._pole[x - 1][y - 1] = chr(8718)

    def ship_search(self, x, y):
        for s in self._ships:
            if (x, y) in s.ship_coords:
                return s
        return None

    def say_current_status(self):
        print('Текущее состояние кораблей')
        for s in self._ships:
            print(s)

    def get_possible_cells(self):
        possible_cells = []
        for x in range(0, 6):
            for y in range(0, 6):
                if self._pole[x][y] in ['O', chr(8718)]:
                    possible_cells.append([x + 1, y + 1])

        return possible_cells

    def get_random_cell(self):
        cells = self.get_possible_cells()
        return cells[random.randint(0, len(cells)-1)]

    def make_shot(self, x, y):
        if x not in range(1, 7) or y not in range(1, 7):
            raise Exception(f'Указаны некорректные координаты {x}, {y} для выстрела.')

        cell = self._pole[x - 1][y - 1]

        if cell == 'O':
            self._pole[x - 1][y - 1] = 'T'
            print(f'Выстрел в клетку {x}, {y}. Мимо!')
        elif cell == chr(8718):
            self._pole[x - 1][y - 1] = 'X'
            self.ship_search(x, y).shoted()
            print(f'Выстрел в клетку {x}, {y}. Попадание!')

    def check_lose(self):
        d = []
        for s in self._ships:
            d.append(s.is_destroyed)
        return all(d)