import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from copy import copy
from random import randint
from sys import exit as close_game

root = tk.Tk()


heart = Image.open('images/heart.png')
heart = ImageTk.PhotoImage(heart)

keys_pressed = {
    37: False, 39: False, 38: False,  # Управление для игрока
    27: False  # Пауза
}

bullets = []  # Список для хранения активных пуль игрока
enemies = [[], []]  # Список для хранения активных врагов
enemy_bullets = []  # Список для хранения активных пуль врагов

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
                     'score': 50}]

Image.open('images/player.png')

player_spaceship = {'id': 0,
                    'image': 'images/player.png',
                    'x': 0,
                    'y': 0,
                    'image_obj': ImageTk.PhotoImage(file='images/player.png')}


Paused = False
Game_is_active = False


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
            enemy = copy(types_of_enemies[0])
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
            background_game.move(enemy['id'], (((-1)**row)*x_move)/default_n, 4/default_n)
            enemy['y'] += 4/default_n
            enemy['x'] += (((-1)**row)*x_move)/default_n
            root.after(round(round(1600/default_n)*1.5), enemies_movement, enemy, row, x_move, n-1, default_n)
        elif Paused:
            root.after(5, enemies_movement, enemy, row, x_move, n, default_n)
        if enemy['y'] >= 825:
            Game_is_active = False
            Paused = False
            switch_frames(game, main_menu)


def start_shooting():
    for row in range(2):
        for i in range(len(enemies[row])):
            enemy = enemies[row][i]
            enemy['rate'] = round((enemy['rate'] + randint(-1000, 2000)))
            root.after(round(max(randint(500*i, 6000+1000*i), 0))*2, create_enemy_bullet, enemy)


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
            background_game.move(bullet['id'], 0, (5*bullet['speed']))
            if background_game.coords(bullet['id'])[3] > 900:  # Если пуля вышла за верхнюю границу
                background_game.delete(bullet['id'])
                enemy_bullets.remove(bullet)
    root.after(30, move_enemy_bullets)


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
    global pause_button_canvas, player_spaceship, Paused, Game_is_active, enemies
    Game_is_active = True
    Paused = False
    background_game.delete('all')
    enemies = [[], []]
    background_game.create_image(1600, 900, image=background_image, anchor="se")
    pause_button_canvas = background_game.create_window(1550, 60, window=pause_button)
    player_spaceship['id'] = background_game.create_image(800, 794, image=player_spaceship['image_obj'])
    player_spaceship['x'] = 800
    player_spaceship['y'] = 794
    enemy_bullets.clear()
    bullets.clear()
    placing_enemies()


def moving_ship():
    if not Paused and Game_is_active:
        if keys_pressed[37] and player_spaceship['x'] >= 90:
            player_spaceship['x'] -= 8
            background_game.move(player_spaceship['id'], -8, 0)
        if keys_pressed[39] and player_spaceship['x'] <= 1510:
            player_spaceship['x'] += 8
            background_game.move(player_spaceship['id'], 8, 0)
    root.after(5, moving_ship)


def create_bullet():
    if keys_pressed[38] and not Paused and Game_is_active:
        x, y = background_game.coords(player_spaceship['id'])
        bullet = background_game.create_rectangle(x-4.5, y-75, x+4.5, y-66, fill="#ffffff", outline="#ffffff")
        bullets.append(bullet)
        # Ограничение частоты выстрелов
        root.after(1000, create_bullet)
    else:
        root.after(5, create_bullet)


def move_bullets():
    if not Paused and Game_is_active:
        for bullet in bullets[:]:  # Используем копию списка для безопасного удаления
            background_game.move(bullet, 0, -8)
            coords = background_game.coords(bullet)
            if coords[3] < 0:  # Если пуля вышла за верхнюю границу
                background_game.delete(bullet)
                bullets.remove(bullet)
    root.after(30, move_bullets)


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


root.bind("<KeyPress>", key_pressed)
root.bind("<KeyRelease>", key_released)

moving_ship()
create_bullet()
move_bullets()
move_enemy_bullets()

root.mainloop()
