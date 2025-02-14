# battlepass.py

from tkinter import Frame, Label, Button


class BattlePassMenu:
    def __init__(self, root, player):
        self.root = root
        self.player = player

        # Создаем панель батлпаса
        self.frame = Frame(root, bg="lightblue")
        self.frame.pack(fill="both", expand=True)

        # Заголовок батлпаса
        self.title_label = Label(
            self.frame,
            text="Батлпас",
            font=("Arial", 36),
            bg="lightblue"
        )
        self.title_label.pack(pady=50)

        # Прогресс батлпаса
        self.progress_label = Label(
            self.frame,
            text=self.player.get_progress(),
            font=("Arial", 24),
            bg="lightblue"
        )
        self.progress_label.pack(pady=20)

        # Кнопка "Закрыть"
        self.close_button = Button(
            self.frame,
            text="Закрыть",
            font=("Arial", 24),
            width=20,
            height=2,
            command=self.hide
        )
        self.close_button.pack(pady=20)

    def update(self):
        """Обновить прогресс батлпаса на экране."""
        self.progress_label.config(text=self.player.get_progress())

    def show(self):
        """Показать батлпас."""
        self.frame.pack(fill="both", expand=True)
        self.update()  # Обновить прогресс

    def hide(self):
        """Скрыть батлпас."""
        self.frame.pack_forget()
