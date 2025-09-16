import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from copy import copy
from random import randint, choices
from sys import exit as close_game

root = tk.Tk()


heart = Image.open('images/heart.png')
heart = ImageTk.PhotoImage(heart)

keys_pressed = {
    37: False, 39: False, 38: False,  # Управление для игрока
    27: False  # Пауза
}

bullets = []  # Список для хранения активных пуль игрока

enemy_bullets = []  # Список для хранения активных пуль врагов

enemies = [[], []]  # Список для хранения активных врагов

dead_enemies = []  # Список для хранения мёртвых врагов

types_of_enemies = [{'id': 0,
                     'name': 'corvette',
                     'image': 'images/enemies/corvette.png',
                     'x': 0,
                     'y': 0,
                     'fill': "#ffffff",
                     'outline': "#ffffff",
                     'size_x': 72,
                     'size_y': 93,
                     'hp': 1,
                     'bullet_damage': 1,
                     'rate': 8000,
                     'bullet_speed': 1,
                     'score': 50},
                    {'id': 0,
                     'name': 'destroyer',
                     'image': 'images/enemies/frigate.png',
                     'x': 0,
                     'y': 0,
                     'fill': "#ffb841",
                     'outline': "#ff4f00",
                     'size_x': 108,
                     'size_y': 80,
                     'hp': 1,
                     'bullet_damage': 1,
                     'rate': 4000,
                     'bullet_speed': 2.5,
                     'score': 100},
                    {'id': 0,
                     'name': 'battleship',
                     'image': 'images/enemies/destroyer.png',
                     'x': 0,
                     'y': 0,
                     'fill': "#57b0ff",
                     'outline': "#8533ff",
                     'size_x': 80,
                     'size_y': 147,
                     'hp': 2,
                     'bullet_damage': 2,
                     'rate': 11000,
                     'bullet_speed': 0.5,
                     'score': 125},
                    {'id': 0,
                     'name': 'cruiser',
                     'image': 'images/enemies/cruiser.png',
                     'x': 0,
                     'y': 0,
                     'fill': "#cc0000",
                     'outline': "#4d0000",
                     'size_x': 95,
                     'size_y': 118,
                     'hp': 3,
                     'bullet_damage': 2,
                     'rate': 6500,
                     'bullet_speed': 1.5,
                     'score': 250}]

Image.open('images/player.png')

player_spaceship = {'id': 0,
                    'image': 'images/player.png',
                    'x': 0,
                    'y': 0,
                    'hp': 4,
                    'image_obj': ImageTk.PhotoImage(file='images/player.png'),
                    'invincible': False,
                    'visible': True}


Paused = False
Game_is_active = False
score = 0
hp_sprites = []
pace_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.2, 1.4, 1.6, 1.8, 2]
hp_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
hp_slider_value = tk.IntVar()
pace_slider_value = tk.IntVar()
set_hp = 6
set_pace = 1
score_label_id = None
hp_value_label = None
pace_value_label = None


def health():
    global player_spaceship
    if not Paused and Game_is_active:
        for sprite in hp_sprites:
            background_game.delete(sprite)
        hp_sprites.clear()
        for i in range(player_spaceship['hp']):
            sprite = background_game.create_image(i * 40 + 40, 890, image=heart, anchor="se")
            hp_sprites.append(sprite)


def scales_values():
    global hp_value_label, pace_value_label
    if settings.winfo_ismapped():
        if hp_value_label and pace_value_label:
            background_settings.delete(pace_value_label)
            background_settings.delete(hp_value_label)
        hp_text = tk.Label(background_settings, text=f"{hp_values[hp_slider_value.get()]}",
                           font=("Cascadia Code", 30), fg="white", bg="black")
        hp_value_label = background_settings.create_window(1100, 565, window=hp_text, anchor="nw")
        pace_text = tk.Label(background_settings, text=f"{pace_values[pace_slider_value.get()]}",
                             font=("Cascadia Code", 30), fg="white", bg="black")
        pace_value_label = background_settings.create_window(1100, 365, window=pace_text, anchor="nw")
    root.after(50, scales_values)


def by_default_settings():
    pace_scale.set(5)
    hp_scale.set(5)


def exit_settings():
    global set_hp, set_pace
    switch_frames(settings, main_menu)
    set_hp = hp_values[hp_slider_value.get()]
    set_pace = pace_values[pace_slider_value.get()]


def new_round():
    global number_of_wave, spawn_chance_values
    if not Paused and Game_is_active and dead_enemies == [] and enemies == [[], []]:
        if number_of_wave <= 3:
            spawn_chance_values[number_of_wave % 3 + 1] += 20
            spawn_chance_values[0] -= 20
        elif (number_of_wave > 3) and (number_of_wave <= 5):
            spawn_chance_values[number_of_wave % 3 + 1] += 10
            spawn_chance_values[0] -= 10
        number_of_wave += 1
        placing_enemies()
    root.after(5, new_round)


def start_invincibility():
    player_spaceship['invincible'] = True
    blink_ship(0)

def end_invincibility():
    player_spaceship['invincible'] = False
    background_game.itemconfig(player_spaceship['id'], state='normal')
    player_spaceship['visible'] = True


def blink_ship(count):
    if count < 501 and player_spaceship['invincible'] and not Paused and Game_is_active:
        if player_spaceship['visible']:
            background_game.itemconfig(player_spaceship['id'], state='hidden')
        else:
            background_game.itemconfig(player_spaceship['id'], state='normal')
        if count % 50 == 0 and count != 0:
            player_spaceship['visible'] = not player_spaceship['visible']
        root.after(round(5/(set_pace**2)), lambda: blink_ship(count + 1))
    elif count == 501:
        end_invincibility()
    else:
        root.after(5, lambda: blink_ship(count))



chosen_section = [{'name': 'base_info', 'chosen': True, 'text': '* "Space Invaders" — это игра, суть которой заключается в отра-' + chr(10) + '  жении нападения врагов. ' + chr(10) + '* Игрок, управляя космическим кораблём, способен передвигать ' + chr(10) + '  его по игровому полю и совершать выстрел вертикально вверх.' + chr(10) + '* Вражеские корабли в свою очередь двигаются "зиг-загом" к ниж-' + chr(10) + '  ней границе игрового поля и совершают выстрелы вертикально ' + chr(10) + '  вниз с временным интервалом, заданный игрой.'},
                  {'name': 'damage', 'chosen': False, 'text': '* В данной игре получение определённого количества урона умень-' + chr(10) + '  шает единицы здоровья объекта на значение, равное полученному ' + chr(10) + '  урону. ' + chr(10) + '* Урон выстрела игрока всегда равен единице.' + chr(10) + '* Урон выстрела вражеского корабля зависит от его типа (см. раз-' + chr(10) + '  дел "Типы кораблей"). Урон падающего вражеского корабля при ' + chr(10) + '  его попадании по игроку всегда равен 1.'},
                  {'name': 'hp', 'chosen': True, 'text': '* Игрок имеет количество единиц здоровья, заданное в настрой-' + chr(10) + '  ках. Стандартное значение — 6 единиц (см. раздел "Настрой-' + chr(10) + '  ки"). ' + chr(10) + '* Вражеские корабли имеют количество единиц здоровья, зависящих ' + chr(10) + '  от их типа (см. раздел "Типы кораблей"). ' + chr(10) + '* После уменьшения здоровья до 0 объект считается уничтоженным. ' + chr(10) + '  После уничтожения корабля игрока наступает конец игры (см. ' + chr(10) + '  раздел "Конец игры"). После уничтожения вражеского корабля он ' + chr(10) + '  начинает падать вертикально вниз.'},
                  {'name': 'end_of_game', 'chosen': False, 'text': '* Игра заверщается в случае падение здоровья игрока до 0. ' + chr(10) + '* Также конец игры наступает при достижении хотя бы одного вра-' + chr(10) + '  жеского корабля нижней границы экрана.' + chr(10) + '* После конца игры игровое поле закрывается, открывается экран, ' + chr(10) + '  на котором отображено количество полученных за эту игру оч-' + chr(10) + '  ков. На этом же экране есть возможность выйти в главное меню ' + chr(10) + '  или начать игру заново.'},
                  {'name': 'waves_of_enemies', 'chosen': False, 'text': '* Атаки врагов делятся на волны. В каждой волне 20 вражеских ко-' + chr(10) + '  раблей. После уничтожения врагов одной волны, начинается сле-' + chr(10) + '  дующая волна и располагаются новые вражеские корабли. ' + chr(10) + '* С увеличением количества пройденных волн скорость движения ' + chr(10) + '  вражеского выстрела и скорость падение уничтоженного корабля ' + chr(10) + '  увеличиваются. ' + chr(10) + '* Также увеличивается скорость движения вражеских кораблей и ' + chr(10) + '  увеличивается шанс появления определённых типов врагов, умень-' + chr(10) + '  шается временной интервал между выстрелами.'},
                  {'name': 'types_of_enemies', 'chosen': False, 'text': ' Вражеские корабли делятся на несколько типов (кликните на ин-' + chr(10) + ' тересующий вас тип, чтобы узнать поподробнее. Базовые показа-' + chr(10) + ' тели интервалов равны показателям на первой волне при базовых' + chr(10) + ' настройках темпа игры (см. раздел "Настройки")): '},
                  {'name': 'score', 'chosen': False, 'text': '* При уничтожения вражеского корабля количество очков увеличи-' + chr(10) + '  вается. ' + chr(10) + '* Количество полученных очков зависит от типа вражеского кораб-' + chr(10) + '  ля. Уничтожение кораблей разных типов даёт разное количество ' + chr(10) + '  очков  (см. раздел "Типы кораблей").' + chr(10) + '* Количество очков, получаемых за уничтожение вражеского кораб-' + chr(10) + '  ля, умножается на номер волны, на котором игрок находится.' + chr(10) + '* Также значение очков умножается на множители, зависящих от ' + chr(10) + '  значений темпа игры и здоровья игрока, заданных в настройках.'},
                  {'name': 'settings', 'chosen': False, 'text': '* Кнопка настроек находится на главном меню и обозначается сим-' + chr(10) + '  волом шестерни.' + chr(10) + '* В настройках предоставлена возможность изменить темп игры и ' + chr(10) + '  количество единиц здоровья, дающихся при старте игры.' + chr(10) + '* Изначальное значение темпа игры равно 1. Максимальное значе-' + chr(10) + '  ние равно 2 (игра будет в 2 раза быстрее). Минимальное зна-' + chr(10) + '  чение — 0,5 (игра будет в 2 раза медленее).' + chr(10) + '* Изначальное значение количества единиц здоровья равно 6. Мак-' + chr(10) + '  симальное значение равно 12. Минимальное значение — 1.' + chr(10) + '* Кнопка "По умолчанию" в настрйоках возвращает изначальные ' + chr(10) + '  значение обоих ползунков.'},
                  {'name': 'upravlenie', 'chosen': False, 'text': 'Управление на игровом поле: ' + chr(10) + '* Кнопки "Влево" и "Вправо" — передвижение корабля' + chr(10) + '* Кнопка "Вверх" — стрельба' + chr(10) + '* Кнопка Esc — пауза/снятие с паузы'},
                  {'name': 'corvette', 'chosen': False, 'text': '* Корвет — базовый тип вражеских кораблей.' + chr(10) + '* Урон выстрела: 1 единица. ' + chr(10) + '* Количество единиц здоровья: 1 единица.' + chr(10) + '* Базовая скорость движения выстрела: 5 единиц.' + chr(10) + '* Базовые интервалы между выстрелами: от 7 с до 10 с.' + chr(10) + '* Базовое количество очков за уничтожение: 50 очков.'},
                  {'name': 'destroyer', 'chosen': False, 'text': '* Эсминец — тип вражеских кораблей, обладающий наименьшими ба-' + chr(10) + '  зовыми показателями временных интервалов между выстрелами и ' + chr(10) + '  наибольшими показателями скорости движения выстрела. ' + chr(10) + '* Урон выстрела: 1 единица. ' + chr(10) + '* Количество единиц здоровья: 1 единица.' + chr(10) + '* Базовая скорость движения выстрела: 12,5 единиц.' + chr(10) + '* Базовые интервалы между выстрелами: от 3 с до 6 с.' + chr(10) + '* Базовое количество очков за уничтожение: 100 очков.'},
                  {'name': 'battleship', 'chosen': False, 'text': '* Линкор — тип вражеских кораблей, обладающий увеличенными уро-' + chr(10) + '  ном, количеством единиц здоровья и временными интервалами меж-' + chr(10) + '  ду выстрелами и уменьшенной скоростью движения выстрела по ' + chr(10) + '  сравнению с корветом.' + chr(10) + '* Урон выстрела: 2 единицы. ' + chr(10) + '* Количество единиц здоровья: 2 единицы.' + chr(10) + '* Базовая скорость движения выстрела: 2,5 единиц.' + chr(10) + '* Базовые интервалы между выстрелами: от 10 с до 13 с.' + chr(10) + '* Базовое количество очков за уничтожение: 125 очков.'},
                  {'name': 'cruiser', 'chosen': False, 'text': '* Крейсер — тип вражеских кораблей, обладающий по сравнению с ' + chr(10) + '  корветом увеличенными показателями урона, количества единиц ' + chr(10) + '  здоровья, скоростью движения выстрела и уменьшенными интер-' + chr(10) + '  валами между выстрелами.' + chr(10) + '* Урон выстрела: 2 единицы. ' + chr(10) + '* Количество единиц здоровья: 3 единицы.' + chr(10) + '* Базовая скорость движения выстрела: 7,5 единиц.' + chr(10) + '* Базовые интервалы между выстрелами: от 5,5 с до 8,5 с.' + chr(10) + '* Базовое количество очков за уничтожение: 250 очков.'}]

image_ship = ''


def guide_open():
    guide_button(0)
    switch_frames(main_menu, guide)


def guide_button(num):
    global text_page, image_ship
    chosen_section[num]['chosen'] = True
    for i in range(len(chosen_section)):
        if i != num:
            chosen_section[i]['chosen'] = False
    s = ''
    text_page.delete('all')
    return_to_list = tk.Label(text_page, text='Вернуться к списку', font=("Cascadia Code", 25), fg="white", bg="black", wraplength=1090, justify='center')

    if chosen_section[0]['chosen']:
        base_info_section.config(bg="white", fg="black")
        s = chosen_section[0]['text']
    else:
        base_info_section.config(bg="black", fg="white")

    if chosen_section[1]['chosen']:
        damage_section.config(bg="white", fg="black")
        s = chosen_section[1]['text']
    else:
        damage_section.config(bg="black", fg="white")

    if chosen_section[2]['chosen']:
        hp_section.config(bg="white", fg="black")
        s = chosen_section[2]['text']
    else:
        hp_section.config(bg="black", fg="white")

    if chosen_section[3]['chosen']:
        end_of_game_section.config(bg="white", fg="black")
        s = chosen_section[3]['text']
    else:
        end_of_game_section.config(bg="black", fg="white")

    if chosen_section[4]['chosen']:
        waves_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[4]['text']
    else:
        waves_of_enemies_section.config(bg="black", fg="white")

    if chosen_section[5]['chosen']:
        types_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[5]['text']
        corvette_label = tk.Label(text_page, text=' 1. Корвет', font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, justify='left')
        corvette_label.bind("<Enter>", on_enter)
        corvette_label.bind("<Leave>", on_leave)
        corvette_label.bind("<Button-1>", lambda event: guide_button(len(chosen_section)-4))
        text_page.create_window(6, 175, window=corvette_label, anchor="nw")

        destroyer_label = tk.Label(text_page, text=' 2. Эсминец', font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, justify='left')
        destroyer_label.bind("<Enter>", on_enter)
        destroyer_label.bind("<Leave>", on_leave)
        destroyer_label.bind("<Button-1>", lambda event: guide_button(len(chosen_section)-3))
        text_page.create_window(6, 225, window=destroyer_label, anchor="nw")

        battleship_label = tk.Label(text_page, text=' 3. Линкор', font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, justify='left')
        battleship_label.bind("<Enter>", on_enter)
        battleship_label.bind("<Leave>", on_leave)
        battleship_label.bind("<Button-1>", lambda event: guide_button(len(chosen_section)-2))
        text_page.create_window(6, 275, window=battleship_label, anchor="nw")

        cruiser_label = tk.Label(text_page, text=' 4. Крейсер', font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, justify='left')
        cruiser_label.bind("<Enter>", on_enter)
        cruiser_label.bind("<Leave>", on_leave)
        cruiser_label.bind("<Button-1>", lambda event: guide_button(len(chosen_section)-1))
        text_page.create_window(6, 325, window=cruiser_label, anchor="nw")
    else:
        types_of_enemies_section.config(bg="black", fg="white")

    if chosen_section[6]['chosen']:
        score_section.config(bg="white", fg="black")
        s = chosen_section[6]['text']
    else:
        score_section.config(bg="black", fg="white")

    if chosen_section[7]['chosen']:
        settings_section.config(bg="white", fg="black")
        s = chosen_section[7]['text']
    else:
        settings_section.config(bg="black", fg="white")

    if chosen_section[8]['chosen']:
        upravlenie_section.config(bg="white", fg="black")
        s = chosen_section[8]['text']
    else:
        upravlenie_section.config(bg="black", fg="white")

    if chosen_section[len(chosen_section)-4]['chosen']:
        types_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[len(chosen_section)-4]['text']
        return_to_list.bind("<Enter>", on_enter)
        return_to_list.bind("<Leave>", on_leave)
        return_to_list.bind("<Button-1>", lambda event: guide_button(5))
        text_page.create_window(545, 520, window=return_to_list, anchor="center")

    if chosen_section[len(chosen_section)-3]['chosen']:
        types_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[len(chosen_section)-3]['text']
        return_to_list.bind("<Enter>", on_enter)
        return_to_list.bind("<Leave>", on_leave)
        return_to_list.bind("<Button-1>", lambda event: guide_button(5))
        text_page.create_window(545, 520, window=return_to_list, anchor="center")

    if chosen_section[len(chosen_section)-2]['chosen']:
        types_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[len(chosen_section)-2]['text']
        return_to_list.bind("<Enter>", on_enter)
        return_to_list.bind("<Leave>", on_leave)
        return_to_list.bind("<Button-1>", lambda event: guide_button(5))
        text_page.create_window(545, 520, window=return_to_list, anchor="center")

    if chosen_section[len(chosen_section)-1]['chosen']:
        types_of_enemies_section.config(bg="white", fg="black")
        s = chosen_section[len(chosen_section)-1]['text']
        return_to_list.bind("<Enter>", on_enter)
        return_to_list.bind("<Leave>", on_leave)
        return_to_list.bind("<Button-1>", lambda event: guide_button(5))
        text_page.create_window(545, 520, window=return_to_list, anchor="center")

    if (num >= (len(chosen_section)-4)) and (num <= (len(chosen_section)-1)):
        image_ship = tk.PhotoImage(file=types_of_enemies[num-(len(chosen_section)-4)]['image'])
        text_section = tk.Label(text_page, text=s, font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, image=image_ship, compound="bottom", justify='left')
    else:
        text_section = tk.Label(text_page, text=s, font=("Cascadia Code", 22), fg="white", bg="black", wraplength=1090, justify='left')
    text_page.create_window(6, 4, window=text_section, anchor="nw")


def key_pressed(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = True
    if event.keycode == 27 and (not Paused and Game_is_active):
        pause_game()
    elif event.keycode == 27 and (Paused and Game_is_active):
        continue_game()


def key_released(event):
    if event.keycode in keys_pressed:
        keys_pressed[event.keycode] = False


def placing_enemies():
    global enemies, First_Movement
    First_Movement = True
    for row in range(2):
        for col in range(10):
            enemy = copy(types_of_enemies[choices(range(len(types_of_enemies)), weights=spawn_chance_values, k=1)[0]])
            Image.open(enemy['image'])
            enemy_image = ImageTk.PhotoImage(file=enemy['image'])
            enemy['image_obj'] = enemy_image
            enemy['x'] = col * 130 + 200
            enemy['y'] = row * 200 + 200
            enemy['id'] = background_game.create_image(enemy['x'], enemy['y'], image=enemy['image_obj'])
            enemies[row].append(enemy)
    start_shooting()
    activate_enemies_movement()


def activate_enemies_movement():
    x_move = 50
    for row in range(2):
        for i in range(len(enemies[row])):
            enemy = enemies[row][i]
            enemies_movement(enemy, row, x_move, 16, 16)


def enemies_movement(enemy, row, x_move, n, default_n):
    global First_Movement, Paused, Game_is_active
    if enemy['hp'] > 0:
        if not Paused and Game_is_active:
            if n == 0:
                n = default_n
                x_move *= -1
                if First_Movement:
                    First_Movement = False
                    x_move += 30
            background_game.move(enemy['id'], (((-1)**row)*(x_move+number_of_wave*0.1))/default_n, (4+number_of_wave*0.1)/default_n)
            enemy['y'] += (4+number_of_wave*0.1)/default_n
            enemy['x'] += (((-1)**row)*(x_move+number_of_wave*0.1))/default_n
            root.after(round((round(1600/default_n) - number_of_wave * 5)*1.5/set_pace), enemies_movement, enemy, row, x_move, n-1, default_n)
        elif Paused:
            root.after(5, enemies_movement, enemy, row, x_move, n, default_n)
        if enemy['y'] >= 825:
            Game_is_active = False
            Paused = False
            switch_frames(game, defeat)


def enemy_death():
    global score
    if not Paused and Game_is_active:
        for row in range(2):
            for enemy in enemies[row][:]:
                if enemy['hp'] == 0:
                    enemies[row].remove(enemy)
                    dead_enemies.append(enemy)
                    # Увеличиваем счет
                    score += round(enemy['score'] * min((number_of_wave + 1), 15) * (7 - set_hp if set_hp <= 6 else 1 / (set_hp - 5)) * (set_pace ** 3))
        root.after(30, enemy_death)
    else:
        root.after(5, enemy_death)


def enemy_falling():
    if not Paused and Game_is_active and dead_enemies != []:
        for enemy in dead_enemies[:]:
            background_game.move(enemy['id'], 0, (5+number_of_wave*0.3)*set_pace)
            enemy['y'] += (5+number_of_wave*0.3)*set_pace
            if enemy['y'] >= 900+enemy['size_y']:
                background_game.delete(enemy['id'])
                dead_enemies.remove(enemy)
        root.after(30, enemy_falling)
    else:
        root.after(5, enemy_falling)


def start_shooting():
    for row in range(2):
        for i in range(len(enemies[row])):
            enemy = enemies[row][i]
            enemy['rate'] = round((enemy['rate'] + randint(-1000 - max(100*number_of_wave, 1500), 2000 - max(100*number_of_wave, 1500)))*1/set_pace)
            root.after(round((1/set_pace)*max(randint(500*i, 6000+1000*i)-max(150*number_of_wave, 2250), 0))*2, create_enemy_bullet, enemy)


def create_enemy_bullet(enemy):
    try:
        if not Paused and Game_is_active and enemy['hp'] > 0:
            x, y = background_game.coords(enemy['id'])
            bullet = {'id': 0, 'speed': 0, 'damage': 0}
            bullet['id'] = background_game.create_rectangle(x - 4.5, y + enemy['size_y'] // 2 - 36, x + 4.5, y + enemy['size_y'] // 2 - 27, fill=enemy['fill'], outline=enemy['outline'])
            bullet['speed'] = enemy['bullet_speed']
            bullet['damage'] = enemy['bullet_damage']
            enemy_bullets.append(bullet)
            # Ограничение частоты выстрелов
            root.after(enemy['rate'], create_enemy_bullet, enemy)
        else:
            root.after(5, create_enemy_bullet, enemy)
    except:
        return


def move_enemy_bullets():
    if not Paused and Game_is_active:
        for bullet in enemy_bullets[:]:  # Используем копию списка для безопасного удаления
            background_game.move(bullet['id'], 0, (5*bullet['speed']+number_of_wave*0.3)*set_pace)
            if background_game.coords(bullet['id'])[3] > 900:  # Если пуля вышла за верхнюю границу
                background_game.delete(bullet['id'])
                enemy_bullets.remove(bullet)
    root.after(30, move_enemy_bullets)


def enemy_collisions():
    global enemies, bullets

    if not Paused and Game_is_active:
        for bullet in bullets[:]:  # Копия списка для безопасного удаления
            bullet_coords = background_game.coords(bullet)

            for row in range(2):
                for enemy in enemies[row][:]:
                    enemy_coords = background_game.coords(enemy['id'])

                    # Проверяем пересечение координат пули и врага
                    if (bullet_coords and enemy_coords and
                            bullet_coords[0] >= enemy_coords[0] - (enemy['size_x']//2) and
                            bullet_coords[0] <= enemy_coords[0] + (enemy['size_x']//2) and
                            bullet_coords[1] >= enemy_coords[1] - (enemy['size_y']//2) and
                            bullet_coords[1] <= enemy_coords[1] + (enemy['size_y']//2)):
                        # Удаляем пулю и уменьшаем здоровье врага
                        enemy['hp'] -= 1
                        background_game.delete(bullet)
                        bullets.remove(bullet)


                        break  # Выходим из цикла по врагам после попадания


def player_bullet_collisions():
    global bullets, player_spaceship

    if not Paused and Game_is_active:
        for bullet in enemy_bullets[:]:  # Копия списка для безопасного удаления
            bullet_coords = background_game.coords(bullet['id'])

            player_coords = background_game.coords(player_spaceship['id'])

            # Проверяем пересечение координат пули и игрока
            if (bullet_coords and player_coords and
                    bullet_coords[0] >= player_coords[0] - 40 and
                    bullet_coords[0] <= player_coords[0] + 40 and
                    bullet_coords[1] >= player_coords[1] - 75 and
                    bullet_coords[1] <= player_coords[1] + 75):
                # Удаляем пулю и уменьшаем здоровье игрока
                if not player_spaceship['invincible']:
                    player_spaceship['hp'] -= bullet['damage']
                    start_invincibility()
                background_game.delete(bullet['id'])
                enemy_bullets.remove(bullet)
                health()


def player_enemy_collisions():
    global dead_enemies, player_spaceship

    if not Paused and Game_is_active:
        for enemy in dead_enemies[:]:  # Копия списка для безопасного удаления
            enemy_coords = background_game.coords(enemy['id'])

            player_coords = background_game.coords(player_spaceship['id'])

            # Проверяем пересечение координат пули и игрока
            if (enemy_coords and player_coords and enemy_coords[0] >= player_coords[0] - 30 and
                    enemy_coords[0] <= player_coords[0] + 30 and
                    enemy_coords[1] >= player_coords[1] - 66 and
                    enemy_coords[1] <= player_coords[1] + 66):
                # Удаляем пулю и уменьшаем здоровье игрока
                if not player_spaceship['invincible']:
                    player_spaceship['hp'] -= 1
                    start_invincibility()
                background_game.delete(enemy['id'])
                dead_enemies.remove(enemy)
                health()


def check_collisions():
    player_enemy_collisions()
    player_bullet_collisions()
    enemy_collisions()
    root.after(30, check_collisions)


def player_death():
    global Paused, Game_is_active, pause_button_canvas, defeat_score_label, background_defeat
    if not Paused and Game_is_active:
        if player_spaceship['hp'] <= 0:
            Game_is_active = False
            Paused = False
            switch_frames(game, defeat)
            background_defeat.delete(defeat_score_label)
            defeat_score_label = tk.Label(background_defeat, text= f"Счёт: {chr(10)} {chr(10)} {score} очков", font=("Minecraft Rus", 50), fg="red", bg="black")
            defeat_score_label = background_defeat.create_window(800, 570, window=defeat_score_label)
    root.after(30, player_death)


def switch_frames(from_frame, to_frame):
    from_frame.pack_forget()
    to_frame.pack(fill='both', expand=True)


def start_game():
    restart_game()
    switch_frames(main_menu, game)


def pause_game():
    global Paused, pause_menu_canvas
    Paused = True
    pause_menu_canvas = background_game.create_window(800, 450, window=pause_menu)
    background_game.delete(pause_button_canvas)


def continue_game():
    global Paused, pause_button_canvas
    Paused = False
    background_game.delete(pause_menu_canvas)
    pause_button_canvas = background_game.create_window(1550, 60, window=pause_button)


def stop_game():
    global Game_is_active, Paused, pause_button_canvas
    Game_is_active = False
    Paused = False
    background_game.delete(pause_menu_canvas)
    pause_button_canvas = background_game.create_window(1550, 60, window=pause_button)
    switch_frames(game, main_menu)


def restart_game():
    global pause_button_canvas, player_spaceship, Paused, Game_is_active, score, score_label_id, enemies, number_of_wave, spawn_chance_values
    Game_is_active = True
    Paused = False
    score = 0
    number_of_wave = 0
    player_spaceship['hp'] = set_hp
    player_spaceship['invincible'] = False
    background_game.delete('all')
    enemies = [[], []]
    spawn_chance_values = [100, 0, 0, 0]
    background_game.create_image(1600, 900, image=background_image, anchor="se")
    pause_button_canvas = background_game.create_window(1550, 60, window=pause_button)
    player_spaceship['id'] = background_game.create_image(800, 794, image=player_spaceship['image_obj'])
    player_spaceship['x'] = 800
    player_spaceship['y'] = 794
    health()
    dead_enemies.clear()
    bullets.clear()
    enemy_bullets.clear()
    placing_enemies()


def restart_after_defeat():
    restart_game()
    switch_frames(defeat, game)


def moving_ship():
    if not Paused and Game_is_active:
        if keys_pressed[37] and player_spaceship['x'] >= 90:
            player_spaceship['x'] -= 8*set_pace
            background_game.move(player_spaceship['id'], -8*set_pace, 0)
        if keys_pressed[39] and player_spaceship['x'] <= 1510:
            player_spaceship['x'] += 8*set_pace
            background_game.move(player_spaceship['id'], 8*set_pace, 0)
    root.after(5, moving_ship)


def create_bullet():
    if keys_pressed[38] and not Paused and Game_is_active and not player_spaceship['invincible']:
        x, y = background_game.coords(player_spaceship['id'])
        bullet = background_game.create_rectangle(x-4.5, y-75, x+4.5, y-66, fill="#ffffff", outline="#ffffff")
        bullets.append(bullet)
        # Ограничение частоты выстрелов
        root.after(round(1000*1/set_pace), create_bullet)
    else:
        root.after(5, create_bullet)


def move_bullets():
    if not Paused and Game_is_active:
        for bullet in bullets[:]:  # Используем копию списка для безопасного удаления
            background_game.move(bullet, 0, -8*set_pace)
            coords = background_game.coords(bullet)
            if coords[3] < 0:  # Если пуля вышла за верхнюю границу
                background_game.delete(bullet)
                bullets.remove(bullet)
    root.after(30, move_bullets)


def score_count():
    global score_label_id
    if score_label_id:
        background_game.delete(score_label_id)
    score_text = tk.Label(background_game, text=f"Счёт: {score}",
                          font=("Cascadia Code", 30), fg="white", bg="black")
    score_label_id = background_game.create_window(20, 10, window=score_text, anchor="nw")
    root.after(100, score_count)


def on_enter(event):
    current_font = font.Font(font=event.widget["font"]).cget("family")
    current_size = font.Font(font=event.widget["font"]).cget("size")
    event.widget.config(font=(current_font, current_size+2, "bold"))


def on_leave(event):
    current_font = font.Font(font=event.widget["font"]).cget("family")
    current_size = font.Font(font=event.widget["font"]).cget("size")
    event.widget.config(font=(current_font, current_size-2))


# Фоновое изображение
path = 'images/Background.png'
background_image = Image.open(path)
background_image = ImageTk.PhotoImage(background_image)

# Основные данные окна
root.title("Space Invaders")
root.geometry('1600x900+160-90')
root.resizable(False, False)
root.iconbitmap(default="images/icon.ico")

# Главное меню
main_menu = tk.Frame(root, width=1600, height=900)

# Главное меню, задний фон
background_main_menu = tk.Canvas(main_menu, width=1600, height=900)
background_main_menu.pack(fill="both", expand=True)
background_main_menu.create_image(1600, 900, image=background_image, anchor="se")

# Главное меню, заголовок
title_label = tk.PhotoImage(file="images/Title.png")
background_main_menu.create_image(800, 250, image=title_label)

# Главное меню, кнопка "Начать игру"
start_button = tk.Label(background_main_menu, text="Начать игру", font=("Cascadia Code", 60), fg="white", bg="black")
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)
start_button.bind("<Button-1>", lambda event: start_game())
background_main_menu.create_window(800, 450, window=start_button)

# Главное меню, кнопка "Помощь"
helping = tk.Label(background_main_menu, text="Помощь", font=("Cascadia Code", 60), fg="white", bg="black")
helping.bind("<Enter>", on_enter)
helping.bind("<Leave>", on_leave)
helping.bind("<Button-1>", lambda event: guide_open())
background_main_menu.create_window(800, 550, window=helping)

# Главное меню, кнопка "Выход"
exit_button = tk.Label(background_main_menu, text="Выход", font=("Cascadia Code", 60), fg="white", bg="black")
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)
exit_button.bind("<Button-1>", lambda event: close_game())
background_main_menu.create_window(800, 650, window=exit_button)

# Главное меню, кнопка "Настроек"
settings_button = tk.PhotoImage(file='images/settings.png')
settings_button_label = tk.Label(image=settings_button, bg="black")
settings_button_label.bind("<Button-1>", lambda event: switch_frames(main_menu, settings))
background_main_menu.create_window(1585, 15, window=settings_button_label, anchor="ne")

main_menu.pack()

# Основной экран игры
game = tk.Frame(root, width=1600, height=900)

# Основной экран игры, задний фон
background_game = tk.Canvas(game, width=1600, height=900)
background_game.pack(fill="both", expand=True)
background_game.create_image(1600, 900, image=background_image, anchor="se")

# Основной экран игры, кнопка паузы
pause_button = tk.Label(background_game, text="☰", font=("Cascadia Code", 60), fg="white", bg="black")
pause_button.bind("<Enter>", on_enter)
pause_button.bind("<Leave>", on_leave)
pause_button.bind("<Button-1>", lambda event: pause_game())
pause_button_canvas = background_game.create_window(1550, 60, window=pause_button)

# Основной экран игры, меню паузы
pause_menu = tk.Canvas(background_game, width=350, height=400, bd=1, bg='black', highlightthickness=4, highlightbackground='white')
continue_button = tk.Label(pause_menu, text="Продолжить", font=("Cascadia Code", 35), fg="white", bg="black")
continue_button.bind("<Button-1>", lambda event: continue_game())
pause_menu.create_window(176, 15, window=continue_button, anchor="n")
restart_button = tk.Label(pause_menu, text="Заново", font=("Cascadia Code", 35), fg="white", bg="black")
restart_button.bind("<Button-1>", lambda event: restart_game())
pause_menu.create_window(176, 85, window=restart_button, anchor="n")
back_to_main_menu_button = tk.Label(pause_menu, text="Выход", font=("Cascadia Code", 35), fg="white", bg="black")
back_to_main_menu_button.bind("<Button-1>", lambda event: stop_game())
pause_menu.create_window(176, 155, window=back_to_main_menu_button, anchor="n")


# Экран поражения
defeat = tk.Frame(root, width=1600, height=900)

# Экран поражения, задний фон
background_defeat = tk.Canvas(defeat, width=1600, height=900)
background_defeat.pack(fill="both", expand=True)
background_defeat.create_image(1600, 900, image=background_image, anchor="se")

# Экран поражения, кнопка "Выйти"
defeat_back_to_main_menu = tk.Label(background_defeat, text="Выйти", font=("Minecraft Rus", 50), fg="red", bg="black")
defeat_back_to_main_menu.bind("<Enter>", on_enter)
defeat_back_to_main_menu.bind("<Leave>", on_leave)
defeat_back_to_main_menu.bind("<Button-1>", lambda event: switch_frames(defeat, main_menu))
background_defeat.create_window(1000, 820, window=defeat_back_to_main_menu)

# Экран поражения, кнопка "Заново"
defeat_restart = tk.Label(background_defeat, text="Заново", font=("Minecraft Rus", 50), fg="red", bg="black")
defeat_restart.bind("<Enter>", on_enter)
defeat_restart.bind("<Leave>", on_leave)
defeat_restart.bind("<Button-1>", lambda event: restart_after_defeat())
background_defeat.create_window(600, 820, window=defeat_restart)

# Экран поражения, надпись поражение
defeat_label = tk.PhotoImage(file="images/Defeat.png")
background_defeat.create_image(800, 250, image=defeat_label)

# Экран поражения, отображение количества очков
defeat_score_label = tk.Label(background_defeat, text="Счёт:", font=("Minecraft Rus", 50), fg="red", bg="black")
defeat_score_label = background_defeat.create_window(800, 570, window=defeat_score_label)

# Экран помощи
guide = tk.Frame(root, width=1600, height=900)

# Экран помощи, задний фон
background_guide = tk.Canvas(guide, width=1600, height=900)
background_guide.pack(fill="both", expand=True)
background_guide.create_image(1600, 900, image=background_image, anchor="se")

# Экран помощи, кнопка "Выйти"
guide_back_to_main_menu = tk.Label(background_guide, text="Выйти", font=("Cascadia Code", 60), fg="white", bg="black")
guide_back_to_main_menu.bind("<Enter>", on_enter)
guide_back_to_main_menu.bind("<Leave>", on_leave)
guide_back_to_main_menu.bind("<Button-1>", lambda event: switch_frames(guide, main_menu))
background_guide.create_window(800, 820, window=guide_back_to_main_menu)

# Экран помощи, заголовок "Помощь"
help_label = tk.Label(background_guide, text="Помощь", font=("Cascadia Code", 80), fg="white", bg="black")
background_guide.create_window(800, 80, window=help_label)

# Экран помощи, список разделов
section_menu = tk.Canvas(background_guide, width=350, height=550, bd=1, bg='black', highlightthickness=4, highlightbackground='white')
background_guide.create_window(250, 450, window=section_menu, anchor="center")

# Экран помощи, кнопки списка разделов
base_info_section = tk.Label(section_menu, text="Общая информация", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
base_info_section.bind("<Button-1>", lambda event: guide_button(0))
section_menu.create_window(180, 5, window=base_info_section, anchor="n")

damage_section = tk.Label(section_menu, text="Урон", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
damage_section.bind("<Button-1>", lambda event: guide_button(1))
section_menu.create_window(180, 60, window=damage_section, anchor="n")

hp_section = tk.Label(section_menu, text="Здоровье", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
hp_section.bind("<Button-1>", lambda event: guide_button(2))
section_menu.create_window(180, 115, window=hp_section, anchor="n")

end_of_game_section = tk.Label(section_menu, text="Конец игры", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
end_of_game_section.bind("<Button-1>", lambda event: guide_button(3))
section_menu.create_window(180, 170, window=end_of_game_section, anchor="n")

waves_of_enemies_section = tk.Label(section_menu, text="Волны врагов", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
waves_of_enemies_section.bind("<Button-1>", lambda event: guide_button(4))
section_menu.create_window(180, 225, window=waves_of_enemies_section, anchor="n")

types_of_enemies_section = tk.Label(section_menu, text="Типы врагов", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
types_of_enemies_section.bind("<Button-1>", lambda event: guide_button(5))
section_menu.create_window(180, 280, window=types_of_enemies_section, anchor="n")

score_section = tk.Label(section_menu, text="Получение очков", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
score_section.bind("<Button-1>", lambda event: guide_button(6))
section_menu.create_window(180, 335, window=score_section, anchor="n")

settings_section = tk.Label(section_menu, text="Настройки", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
settings_section.bind("<Button-1>", lambda event: guide_button(7))
section_menu.create_window(180, 390, window=settings_section, anchor="n")

upravlenie_section = tk.Label(section_menu, text="Управление", font=("Cascadia Code", 25), width=18, fg="white", bg="black")
upravlenie_section.bind("<Button-1>", lambda event: guide_button(8))
section_menu.create_window(180, 445, window=upravlenie_section, anchor="n")

# Экран помощи, текст раздела
text_page = tk.Canvas(background_guide, width=1090, height=550, bd=2, bg='black', highlightthickness=4, highlightbackground='white')
background_guide.create_window(1010, 450, window=text_page, anchor="center")

guide_button(0)

# Экран настроек
settings = tk.Frame(root, width=1600, height=900)

# Экран настроек, задний фон
background_settings = tk.Canvas(settings, width=1600, height=900)
background_settings.pack(fill="both", expand=True)
background_settings.create_image(1600, 900, image=background_image, anchor="se")

# Экран настроек, кнопка "Выйти"
settings_back_to_main_menu = tk.Label(background_settings, text="Выйти", font=("Cascadia Code", 60), fg="white", bg="black")
settings_back_to_main_menu.bind("<Enter>", on_enter)
settings_back_to_main_menu.bind("<Leave>", on_leave)
settings_back_to_main_menu.bind("<Button-1>", lambda event: exit_settings())
background_settings.create_window(800, 820, window=settings_back_to_main_menu)

# Экран настроек, кнопка "По умолчанию"
by_default_back_to_main_menu = tk.Label(background_settings, text="По умолчанию", font=("Cascadia Code", 30), fg="white", bg="black")
by_default_back_to_main_menu.bind("<Enter>", on_enter)
by_default_back_to_main_menu.bind("<Leave>", on_leave)
by_default_back_to_main_menu.bind("<Button-1>", lambda event: by_default_settings())
background_settings.create_window(1400, 840, window=by_default_back_to_main_menu)

# Экран настроек, заголовок "Настройки"
settings_label = tk.Label(background_settings, text="Настройки", font=("Cascadia Code", 80), fg="white", bg="black")
background_settings.create_window(800, 80, window=settings_label)

# Экран настроек, ползунок темпа игры
pace_scale = tk.Scale(background_settings, orient="horizontal", from_=0, to=10, length=560, width=30, digits=0, bg="white", troughcolor='black', showvalue=False, variable=pace_slider_value)
pace_scale.set(5)
background_settings.create_window(800, 400, window=pace_scale)

# Экран настроек, ползунок здоровья
hp_scale = tk.Scale(background_settings, orient="horizontal", from_=0, to=11, length=560, width=30, digits=0, bg="white", troughcolor='black', showvalue=False, variable=hp_slider_value)
hp_scale.set(5)
background_settings.create_window(800, 600, window=hp_scale)

scales_values()

# Экран настроек, надпись "Темп игры"
pace_label = tk.Label(background_settings, text="Темп игры", font=("Cascadia Code", 60), fg="white", bg="black")
background_settings.create_window(800, 300, window=pace_label)

# Экран настроек, надпись "Здоровье игрока"
hp_label = tk.Label(background_settings, text="Здоровье игрока", font=("Cascadia Code", 60), fg="white", bg="black")
background_settings.create_window(800, 500, window=hp_label)

root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

moving_ship()
create_bullet()
move_bullets()
score_count()
check_collisions()
enemy_death()
enemy_falling()
move_enemy_bullets()
player_death()
new_round()

root.mainloop()
