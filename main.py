from battlefield import Desk, Ship

d1 = Desk(player_name='Ilya')
d2 = Desk(player_name='AI')

current_desk = d1
current_player = d2.get_player_name

ships = [1, 1, 1, 1, 2, 2, 3]
for s in ships:
    coords = []
    print(f'Добавляем корябль с {s} палубой (палубами)')
    for i in range(0, s):
        c = input(f'Введите координаты для корабля с {s} палубой (палубами) в формате xy: ')
        coords.append((int(c[0]), int(c[1])))
    d1.add_ship(Ship(s, coords))
    print(current_desk)

d2.add_ship(Ship(1, [(1, 1)]))
d2.add_ship(Ship(1, [(6, 6)]))
d2.add_ship(Ship(1, [(1, 6)]))
d2.add_ship(Ship(1, [(6, 1)]))
d2.add_ship(Ship(2, [(3, 3), (3, 4)]))
d2.add_ship(Ship(2, [(6, 3), (6, 4)]))
d2.add_ship(Ship(3, [(3, 1), (4, 1), (5, 1)]))

# TODO Реаизовать ввод и обработку вспомогательных команд и/или правил игры


while True:
    print(f'Ход игрока { current_player }')

    if current_desk.get_player_name == 'AI':
        coords_pl = input('Введите координаты выстрела в формате xy: ')
        if len(coords_pl) != 2:
            raise Exception("Некорректный ввод")
        x, y = int(coords_pl[0]), int(coords_pl[1])
        if [x, y] in current_desk.get_possible_cells():
            current_desk.make_shot(x, y)
        else:
            raise Exception(f'Координаты {x}, {y} недоступны для выстрела')
    else:
        coords_ai = current_desk.get_random_cell()
        current_desk.make_shot(coords_ai[0], coords_ai[1])

    current_desk.say_current_status()
    print(current_desk)
    if current_desk.check_lose():
        print(f'Игрок {current_desk.get_player_name} проиграл!')
        break

    current_desk, current_player = (d1, d2.get_player_name) if current_desk == d2 else (d2, d1.get_player_name)