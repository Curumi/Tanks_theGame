from units import Hook, Missile
import units




_hooks = []
_missiles = []
_canvas = None

def initialize(canvas):
    global _canvas
    _canvas = canvas

def fire(owner):
    missile = Missile(owner._canvas, owner)
    _missiles.append(missile)
    return missile

def update():
    start = len(_missiles)-1
    for i in range(start,-1,-1):
        if _missiles[i].is_destroyed():
            del _missiles[i]
        else:
            _missiles[i].update()

def check_missles_collection(tank):
    for missile in _missiles:
        if missile.get_owner() == tank:
            continue
        if missile.intersect(tank):
            missile.destroy()
            tank.damage(25)
            return


def fire_hook(owner):
    hook = Hook(owner._canvas, owner)
    _hooks.append(hook)
    return hook


def update_hooks(tanks_list=None):  # Добавляем параметр tanks_list
    for hook in _hooks[:]:
        hook.update()

        # Проверяем коллизии только если передан список танков
        if tanks_list is not None and not hook._hooked_target and not hook._returning:
            for tank in tanks_list:
                if tank != hook.get_owner() and hook.intersect(tank):
                    hook._hooked_target = tank
                    break

        if hook.is_destroyed():
            _hooks.remove(hook)


def get_missiles():
    return _missiles

def get_hooks():
    return _hooks