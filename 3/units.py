import missiles_collection
import world
from hitbox import Hitbox
import texture as skin
from tkinter import NW
from random import randint
import time




class Unit:
    def __init__(self, canvas, x, y, speed, padding, bot, default_image):
        self._destroyed = False
        self._speed = speed
        self._x = x
        self._y = y
        self._vx = 0
        self._vy = 0
        self._canvas = canvas
        self._hp = 100
        self._dx = 0
        self._dy = 0
        self._bot = bot
        self._bot = bot
        self._hitbox = Hitbox(x, y, world.BLOCK_SIZE, world.BLOCK_SIZE, padding=padding)
        self._default_image = default_image
        self._forward_image = default_image
        self._backward_image = default_image
        self._left_image = default_image
        self._right_image = default_image
        self._create()



        if isinstance(self, Tank):
            self._create_hp_bar()

    def damage(self, value):
        self._hp -= value
        if self._hp <= 0:
            self.destroy()
        else:
            if isinstance(self, Tank):
                self._update_hp_bar()  # Обновляем ХП-бар при получении урона

    def _create_hp_bar(self):
        # Создаем прямоугольник для ХП-бара
        self._hp_bar = self._canvas.create_image(self._x, self._y - 10, image=skin.get('100'), anchor=NW)

    def _update_hp_bar(self):
        # Обновляем ХП-бар в зависимости от текущего здоровья
        if self._hp > 75:
            self._canvas.itemconfig(self._hp_bar, image=skin.get('100'))
        elif self._hp > 50:
            self._canvas.itemconfig(self._hp_bar, image=skin.get('75'))
        elif self._hp > 25:
            self._canvas.itemconfig(self._hp_bar, image=skin.get('50'))
        elif self._hp > 0:
            self._canvas.itemconfig(self._hp_bar, image=skin.get('25'))
        elif self._hp == 0:
            self._canvas.itemconfig(self._hp_bar, image=skin.get('0'))

    def is_destroyed(self):
        return self._destroyed

    def destroy(self):
        # Удаление хп-бара после уничтожения
        if hasattr(self, '_hp_bar'):
            self._canvas.delete(self._hp_bar)  # Удаляем хп-бар
        self._destroyed = True
        self.stop()
        self._speed = 0



    def update(self):
        if self._bot:
            self._AI()
        self._dx = self._vx * self._speed
        self._dy = self._vy * self._speed
        self._x += self._dx
        self._y += self._dy
        self._update_hitbox()
        self._check_map_collision()
        self._repaint()


        if isinstance(self, Tank):  # Обновляем хп-бар только для танков
            self._repaint_hp_bar()

    def _repaint_hp_bar(self):
        screen_x = world.get_screen_x(self._x)
        screen_y = world.get_screen_y(self._y)
        self._canvas.moveto(self._hp_bar, x=screen_x, y=screen_y - 10)  # ХП-бар будет чуть выше танка

    def _create(self):
        self._id = self._canvas.create_image(self._x, self._y,
                                             image=skin.get(self._default_image),
                                             anchor=NW)

    def __del__(self):
        try:
            self._canvas.delete(self._id)
        except Exception:
            pass

    def forward(self):
        self._vx = 0
        self._vy = -1
        self._canvas.itemconfig(self._id,
                                image=skin.get(self._forward_image))

    def backward(self):
        self._vx = 0
        self._vy = 1
        self._canvas.itemconfig(self._id,
                                image=skin.get(self._backward_image))

    def left(self):
        self._vx = -1
        self._vy = 0
        self._canvas.itemconfig(self._id,
                                image=skin.get(self._left_image))

    def right(self):
        self._vx = 1
        self._vy = 0
        self._canvas.itemconfig(self._id,
                                image=skin.get(self._right_image))

    def stop(self):
        self._vx = 0
        self._vy = 0


    def _repaint(self):
        screen_x = world.get_screen_x(self._x)
        screen_y = world.get_screen_y(self._y)
        self._canvas.moveto(self._id, x=screen_x, y=screen_y)

    def _AI(self):
        pass

    def _update_hitbox(self):
        self._hitbox.moveto(self._x, self._y)

    def _check_map_collision(self):
        details = {}
        result = self._hitbox.check_map_collision(details)
        if result:
            self._on_map_collision(details)
        else:
            self._no_map_collision()

    def _no_map_collision(self):
        pass

    def _on_map_collision(self, details):
        pass

    def _undo_move(self):
        if self._dx == 0 and self._dy == 0:
            return
        self._x -= self._dx
        self._y -= self._dy
        self._update_hitbox()
        self._repaint()
        self._dx = 0
        self._dy = 0

    def intersect(self, other_unit):
        value = self._hitbox.intersects(other_unit._hitbox)
        if value:
            self._on_intersect(other_unit)
        return value

    def _on_intersect(self, other_unit):
        self._undo_move()

    def _change_orientation(self):
        rand = randint(0, 3)
        if rand == 0:
            self.left()
        if rand == 1:
            self.forward()
        if rand == 2:
            self.right()
        if rand == 3:
            self.backward()

    def get_hp(self):
        return self._hp

    def get_speed(self):
        return self._speed

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_vx(self):
        return self._vx

    def get_vy(self):
        return self._vy

    def get_size(self):
        return world.BLOCK_SIZE

    def is_bot(self):
        return self._bot


class Tank(Unit):
    def __init__(self, canvas, row, col, bot=True):
        super().__init__(canvas, col * world.BLOCK_SIZE, row * world.BLOCK_SIZE, 2, 8,
                         bot, 'tank_up')
        self._last_shot_time = 0  # Время последнего выстрела
        self._shot_delay = 1  # Задержка между выстрелами в секундах (например, 1 секунда)

        self._last_hook_time = 0
        self._hook_cooldown = 5  # 5 секунд перезарядки хука



        if bot:
            self._forward_image = 'tank_up'
            self._backward_image = 'tank_down'
            self._left_image = 'tank_left'
            self._right_image = 'tank_right'
            self._tank_destroy = 'tank_destroy'
        else:
            self._forward_image = 'tank_backward_player'
            self._backward_image = 'tank_forward_player'
            self._left_image = 'tank_left_player'
            self._right_image = 'tank_right_player'
            self._tank_destroy = 'tank_destroy'

        self.forward()
        self._ammo = 80
        self._usual_speed = self._speed
        self._water_speed = self._speed // 2
        self._target = None

    def fire_hook(self):
        current_time = time.time()
        if current_time - getattr(self, '_last_hook_time', 0) >= 5:
            from missiles_collection import fire_hook
            fire_hook(self)  # self передается как владелец хука
            self._last_hook_time = current_time
            return True
        return False


    def destroy(self):
        # Удаление хп-бара после уничтожения
        if hasattr(self, '_hp_bar'):
            self._canvas.delete(self._hp_bar)  # Удаляем хп-бар

        self._destroyed = True
        self.stop()
        self._speed = 0

        # Изменяем текстуру только если это игрок
        if not self._bot:  # Если это игрок
            self._canvas.itemconfig(self._id, image=skin.get(self._tank_destroy))

    def set_target(self, target):
        self._target = target

    def _AI_goto_target(self):
        if randint(1, 2) == 1:
            if self._target.get_x() < self.get_x():
                self.left()
            else:
                self.right()
        else:
            if self._target.get_y() < self.get_y():
                self.forward()
            else:
                self.backward()

    def get_ammo(self):
        return self._ammo

    def _take_ammo(self):
        self._ammo += 10
        if self._ammo > 100:
            self._ammo1 = 100

    def fire(self):
        current_time = time.time()  # Получаем текущее время

        # Проверяем, прошло ли достаточно времени с последнего выстрела
        if current_time - self._last_shot_time >= self._shot_delay:
            if self._ammo > 0:
                self._ammo -= 1
                missiles_collection.fire(self)
                self._last_shot_time = current_time  # Обновляем время последнего выстрела


    def _set_usual_speed(self):
        self._speed = self._usual_speed

    def _set_water_speed(self):
        self._speed = self._water_speed

    def _on_map_collision(self, details):
        if world.WATER in details and len(details) == 1:
            self._set_water_speed()
        elif world.MISSLE in details:
            pos = details[world.MISSLE]
            if world.take(pos['row'], pos['col']) != world.AIR:
                self._take_ammo()
        else:
            self._undo_move()
            if self._bot:
                self._change_orientation()

    def _no_map_collision(self):
        self._set_usual_speed()

    def _on_intersect(self, other_unit):
        super()._on_intersect(other_unit)
        if self._bot:
            self._change_orientation()

    def _AI(self):
        if randint(1, 30) == 1:
            if randint(1, 10) < 9 and self._target is not None:
                self._AI_goto_target()
            else:
                self._change_orientation()
        elif randint(1,30) == 1:
            self._AI_fire()
        elif randint(1,100) == 1:
            self.fire()
    def _AI_fire(self):
        if self._target is None:
            return
        center_x = self.get_x() + self.get_size()//2
        center_y = self.get_y() + self.get_size()//2
        target_center_x = self._target.get_x() + self._target.get_size()//2
        target_center_y = self._target.get_y() + self._target.get_size()//2
        row = world.get_row(center_y)
        col = world.get_col(center_x)
        row_target = world.get_row(target_center_y)
        col_target = world.get_col(target_center_x)
        if row == row_target:
            if col_target < col:
                self.left()
                self.fire()
            else:
                self.right()
                self.fire()
        elif col == col_target:
            if row_target < row:
                self.forward()
                self.fire()
            else:
                self.backward()
                self.fire()

    def is_stunned(self):
        return hasattr(self, '_stun_end_time') and time.time() < self._stun_end_time

    def update(self):
        if self.is_stunned():
            return  # Не обновляем позицию если танк оглушен

        super().update()


class Missile(Unit):
    def __init__(self, canvas, owner):
        super().__init__(canvas, owner.get_x(), owner.get_y(),
                         6, 20, False, 'missile_up')
        self._owner = owner
        self._forward_image = 'missile_up'
        self._backward_image = 'missile_down'
        self._left_image = 'missile_left'
        self._right_image = 'missile_right'
        if owner.get_vx() == 1 and owner.get_vy() == 0:
            self.right()
        elif owner.get_vx() == -1 and owner.get_vy() == 0:
            self.left()
        elif owner.get_vx() == 0 and owner.get_vy() == -1:
            self.forward()
        elif owner.get_vx() == 0 and owner.get_vy() == 1:
            self.backward()
        self._x += owner.get_vx() * self.get_size() // 2
        self._y += owner.get_vy() * self.get_size() // 2
        self._hitbox.set_blacklist([world.CONCRETE, world.BRICK])

    def get_owner(self):
        return self._owner

    def _on_map_collision(self, details):
        if world.BRICK in details:
            row = details[world.BRICK]['row']
            col = details[world.BRICK]['col']
            world.destroy(row, col)
            self.destroy()
        if world.CONCRETE in details:
            self.destroy()


class Hook(Unit):
    def __init__(self, canvas, owner):
        super().__init__(canvas, owner.get_x(), owner.get_y(),
                         8, 20, False, 'hook_up')
        self._owner = owner
        self._forward_image = 'hook_up'
        self._backward_image = 'hook_down'
        self._left_image = 'hook_left'
        self._right_image = 'hook_right'
        self._hooked_target = None
        self._returning = False
        self._max_distance = 500
        self._distance_traveled = 0
        self._hook_speed = 8
        self._chain_id = None
        self._hitbox.set_blacklist([world.BRICK, world.CONCRETE])

        # Направление хука
        if owner.get_vx() == 1 and owner.get_vy() == 0:
            self.right()
        elif owner.get_vx() == -1 and owner.get_vy() == 0:
            self.left()
        elif owner.get_vx() == 0 and owner.get_vy() == -1:
            self.forward()
        elif owner.get_vx() == 0 and owner.get_vy() == 1:
            self.backward()

        # Начальная позиция хука
        self._x += owner.get_vx() * self.get_size() // 2
        self._y += owner.get_vy() * self.get_size() // 2

    def update(self):
        if self._hooked_target:
            self._pull_target()
        elif not self._returning:
            # Перед движением проверяем столкновения
            if not self._check_collisions():
                super().update()
                self._distance_traveled += self._speed
                if self._distance_traveled >= self._max_distance:
                    self._start_returning()
        else:
            self._return_to_owner()

    def _pull_target(self):
        if self._hooked_target is None or self._hooked_target.is_destroyed():
            self._start_returning()
            return

        owner = self._owner
        target = self._hooked_target

        # Упрощенная проверка препятствий (можно закомментировать, если вызывает проблемы)
        # if self._has_obstacles_between(owner, target):
        #     self._start_returning()
        #     return

        dx = owner.get_x() - target.get_x()
        dy = owner.get_y() - target.get_y()
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 20:
            target.destroy()
            self.destroy()
            return

        dx = dx / distance * self._hook_speed
        dy = dy / distance * self._hook_speed

        target._x += dx
        target._y += dy
        target._update_hitbox()

        self._x = target.get_x()
        self._y = target.get_y()
        self._update_hitbox()

        target._repaint()
        self._repaint()

    def _has_obstacles_between(self, unit1, unit2):
        """Проверяет наличие препятствий между двумя юнитами"""
        x1 = unit1.get_x() + unit1.get_size() // 2
        y1 = unit1.get_y() + unit1.get_size() // 2
        x2 = unit2.get_x() + unit2.get_size() // 2
        y2 = unit2.get_y() + unit2.get_size() // 2

        # Проверяем несколько точек вдоль линии между юнитами
        steps = 10
        for i in range(1, steps):
            x = x1 + (x2 - x1) * i / steps
            y = y1 + (y2 - y1) * i / steps
            col = world.get_col(x)
            row = world.get_row(y)
            cell_type = world._map[row][col] if 0 <= row < len(world._map) and 0 <= col < len(world._map[0]) else None
            if cell_type in [world.BRICK, world.CONCRETE]:
                return True
        return False

    def _start_returning(self):
        self._returning = True
        if self._hooked_target:
            self._hooked_target = None  # Отпускаем цель при возвращении
        self.stop()

    def _return_to_owner(self):
        owner_x = self._owner.get_x() + self._owner.get_size() // 2
        owner_y = self._owner.get_y() + self._owner.get_size() // 2
        hook_x = self._x + self.get_size() // 2
        hook_y = self._y + self.get_size() // 2

        dx = owner_x - hook_x
        dy = owner_y - hook_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 10:
            self.destroy()
            return

        speed = self._speed
        if distance > 0:
            dx = dx / distance * speed
            dy = dy / distance * speed

        self._x += dx
        self._y += dy
        self._update_hitbox()
        self._repaint()

    def destroy(self):
        if self._chain_id:
            self._canvas.delete(self._chain_id)
            self._chain_id = None
        super().destroy()

    def get_owner(self):
        return self._owner

    def _check_collisions(self):
        details = {}
        if self._hitbox.check_map_collision(details):
            # Если столкнулись с блоком - возвращаем хук
            if world.BRICK in details or world.CONCRETE in details:
                self._start_returning()
                return True
        return False

    def _on_map_collision(self, details):
        # При столкновении с кирпичом или бетоном - возвращаем хук
        if world.BRICK in details or world.CONCRETE in details:
            self._start_returning()
            # Можно добавить эффект "удара" о стену
            self._canvas.create_rectangle(
                self._x, self._y,
                self._x + self.get_size(), self._y + self.get_size(),
                outline="red", width=2
            )