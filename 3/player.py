# player.py

class Player:
    def __init__(self):
        self.xp = 0  # Опыт игрока
        self.level = 1  # Уровень игрока
        self.battlepass_rewards = {1: 'tank_skin_1', 2: 'tank_skin_2', 3: 'missile_upgrade'}  # Пример наград
        self.current_reward = None  # Текущая награда
        self._update_rewards()

    def _update_rewards(self):
        """Обновление награды на основе текущего уровня."""
        if self.level in self.battlepass_rewards:
            self.current_reward = self.battlepass_rewards[self.level]

    def add_xp(self, xp):
        """Добавить опыт и обновить уровень."""
        self.xp += xp
        if self.xp >= self.level * 100:  # 100 XP для повышения уровня
            self.level += 1
            self._update_rewards()  # Обновляем награды при повышении уровня
            print(f"Поздравляем! Вы достигли уровня {self.level} и получили {self.current_reward}.")

    def get_progress(self):
        """Возвращаем прогресс для отображения."""
        return f"Уровень: {self.level} | Опыт: {self.xp} | Награда: {self.current_reward or 'Нет награды'}"
