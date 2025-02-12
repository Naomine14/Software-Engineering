#Выполнено: Чеканиной Варварой и Ракашевой Альбиной ИТ32

from tkinter import *
from random import randint

class SnakeGame:
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_game()

    def start_game(self):
        self.snake_coords = [[14, 14]]
        self.apple_coords = self.set_apple()
        self.vector = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
        self.direction = self.vector["Right"]
        self.score = 0
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.set_direction)
        self.run_game()

    def set_apple(self):
        while True:
            apple_coords = [randint(0, 29), randint(0, 29)]
            if apple_coords not in self.snake_coords:
                return apple_coords

    def set_direction(self, event):
        if event.keysym in self.vector:
            new_direction = self.vector[event.keysym]
            # Запрет изменения направления на противоположное
            if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
                self.direction = new_direction
        elif event.keysym == 'c':  # Перезапуск при нажатии 'C'
            self.start_game()
        elif event.keysym == 'q':  # Закрытие при нажатии 'Q'
            self.close_game()

    def draw(self):
        self.canvas.delete(ALL)
        x_apple, y_apple = self.apple_coords
        self.canvas.create_oval(x_apple * 10, y_apple * 10,
                                (x_apple + 1) * 10, (y_apple + 1) * 10,
                                fill="red", outline="")

        for x, y in self.snake_coords:
            self.canvas.create_rectangle(x * 10, y * 10,
                                         (x + 1) * 10, (y + 1) * 10,
                                         fill="#228B22", outline="")

        # Отображение счёта
        score_text = f"Счёт: {self.score}"
        self.canvas.create_text(150, 10, text=score_text, fill="white", font=("Arial", 12))

    @staticmethod
    def coord_check(coord):
        return max(0, min(29, coord))

    def run_game(self):
        self.draw()
        x, y = self.snake_coords[0]
        x += self.direction[0]
        y += self.direction[1]

        # Окончание игры при столкновении
        if x < 0 or x >= 30 or y < 0 or y >= 30:
            self.end_game()
            return

        x = self.coord_check(x)
        y = self.coord_check(y)

        if [x, y] == self.apple_coords:
            self.apple_coords = self.set_apple()
            self.score += 1
        elif [x, y] in self.snake_coords:
            self.end_game()
            return
        else:
            self.snake_coords.pop()

        self.snake_coords.insert(0, [x, y])
        if self.snake_coords:  # Проверка на наличие змейки
            self.canvas.after(100, self.run_game)

    def end_game(self):
        game_over_text = "Игра окончена\n 'C' - Перезапустить\n 'Q' - Закрыть игру"
        self.canvas.create_text(150, 150, text=game_over_text, fill="red", font=("Arial", 18), justify='center')
        print(f"Счёт: {self.score}")

    def close_game(self):
        self.canvas.master.destroy() 

root = Tk()
canvas = Canvas(root, width=300, height=300, bg="black")
canvas.pack()
game = SnakeGame(canvas)
root.mainloop()
