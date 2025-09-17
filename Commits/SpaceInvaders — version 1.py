import tkinter as tk
from tkinter import font
from PIL import ImageTk, Image
from sys import exit as close_game

root = tk.Tk()


def switch_frames(from_frame, to_frame):
    from_frame.pack_forget()
    to_frame.pack(fill='both', expand=True)


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


root.mainloop()
