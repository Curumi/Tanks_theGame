import missiles_collection
from tank import Tank
from tkinter import *

from player import Player  # Импортируем класс игрока
from battlepass import BattlePassMenu  # Импортируем класс батлпаса

import world
import tanks_collection
import texture

KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN = 37, 39, 38, 40
KEY_SPACE = 32
KEY_W = 87
KEY_S = 83
KEY_A = 65
KEY_D = 68
FPS = 60


def update():
    tanks_collection.update()
    missiles_collection.update()
    player = tanks_collection.get_player()



    world.set_camera_xy(player.get_x() - world.SCREEN_WIDTH // 2 + player.get_size() // 2,
                        player.get_y() - world.SCREEN_HEIGHT // 2 + player.get_size() // 2)
    world.update_map()
    w.after(1000 // FPS, update)


def key_press(event):
    player = tanks_collection.get_player()
    if player.is_destroyed():
        return
    if event.keycode == KEY_W:
        player.forward()
    elif event.keycode == KEY_S:
        player.backward()
    elif event.keycode == KEY_A:
        player.left()
    elif event.keycode == KEY_D:
        player.right()
    elif event.keycode == KEY_UP:
        world.move_camera(0, -5)
    elif event.keycode == KEY_DOWN:
        world.move_camera(0, 5)
    elif event.keycode == KEY_LEFT:
        world.move_camera(-5, 0)
    elif event.keycode == KEY_RIGHT:
        world.move_camera(5, 0)
    elif event.keycode == 32:
        print('Fire')
        player.fire()


def load_textures():
    texture.load('tank_up',
                  '../img/tank_up.png')
    texture.load('tank_down',
                  '../img/tank_down.png')
    texture.load('tank_left',
                  '../img/tank_left.png')
    texture.load('tank_right',
                  '../img/tank_right.png')

    texture.load('tank_forward_player',
                  '../img/tank_forward_player.png')
    texture.load('tank_backward_player',
                  '../img/tank_backward_player.png')
    texture.load('tank_left_player',
                  '../img/tank_left_player.png')
    texture.load('tank_right_player',
                  '../img/tank_right_player.png')

    texture.load(world.BRICK, '../img/brick.png')
    texture.load(world.WATER, '../img/water.png')
    texture.load(world.CONCRETE, '../img/wall.png')

    texture.load(world.MISSLE, '../img/bonus.png')
    texture.load('missile_up','../img/missile_up.png')
    texture.load('missile_down','../img/missile_down.png')
    texture.load('missile_left','../img/missile_left.png')
    texture.load('missile_right','../img/missile_right.png')

    texture.load('100','../img/100.png')
    texture.load('75','../img/75.png')
    texture.load('50','../img/50.png')
    texture.load('25','../img/25.png')
    texture.load('0', '../img/0.png')

    texture.load('tank_destroy', '../img/tank_destroy.png')





class Menu:
    def __init__(self, root, start_game_callback, exit_game_callback):
        self.root = root
        self.frame = Frame(root, bg="darkblue")
        self.frame.pack(fill="both", expand=True)

        # Заголовок меню
        self.title_label = Label(
            self.frame,
            text="Танки на минималках 2.0",
            font=("Arial", 48, 'bold'),
            fg="white",
            bg="darkblue"
        )
        self.title_label.pack(pady=100)

        # Кнопка "Начать игру"
        self.start_button = Button(
            self.frame,
            text="Начать игру",
            font=("Arial", 24, 'bold'),
            width=20,
            height=2,
            fg="white",
            bg="#5a9e6f",  # Зеленый цвет, похожий на стиль Brawl Stars
            activebackground="#4c7c58",  # Цвет кнопки при нажатии
            relief=FLAT,
            bd=5,
            command=start_game_callback
        )
        self.start_button.pack(pady=30)
        self.start_button.bind("<Enter>", self.on_enter_button)
        self.start_button.bind("<Leave>", self.on_leave_button)

        # Кнопка "Выход"
        self.exit_button = Button(
            self.frame,
            text="Выход",
            font=("Arial", 24, 'bold'),
            width=20,
            height=2,
            fg="white",
            bg="#c70039",  # Красный цвет кнопки
            activebackground="#a6002f",  # Цвет кнопки при нажатии
            relief=FLAT,
            bd=5,
            command=exit_game_callback
        )
        self.exit_button.pack(pady=30)
        self.exit_button.bind("<Enter>", self.on_enter_button)
        self.exit_button.bind("<Leave>", self.on_leave_button)

    def on_enter_button(self, event):
        event.widget.config(bg="#f1f1f1", fg="black")  # При наведении цвет кнопки меняется
        event.widget.config(font=("Arial", 26, 'bold'))  # Увеличиваем размер шрифта

    def on_leave_button(self, event):
        event.widget.config(bg="#5a9e6f", fg="white")  # Возвращаем оригинальный цвет кнопки
        event.widget.config(font=("Arial", 24, 'bold'))  # Возвращаем исходный размер шрифта

    def hide(self):
        """Скрыть меню."""
        self.frame.pack_forget()

    def show(self):
        """Показать меню."""
        self.frame.pack(fill="both", expand=True)


def start_game():

    menu.hide()
    canv.pack()
    world.initialize(canv)
    tanks_collection.initialize(canv)
    missiles_collection.initialize(canv)
    w.bind('<KeyPress>', key_press)
    update()


def exit_game():

    w.destroy()


w = Tk()
w.title('Танки на минималках 2.0')
w.geometry(f"{world.SCREEN_WIDTH}x{world.SCREEN_HEIGHT}")


load_textures()


canv = Canvas(w, width=world.SCREEN_WIDTH, height=world.SCREEN_HEIGHT, bg='light green')


menu = Menu(w, start_game, exit_game)


menu.show()


w.mainloop()