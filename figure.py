import random

from colors import renkler


# Figür sınıfı oyun içindeki şekilleri temsil eder
class Figür:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(renkler) - 1)
        self.rotation = 0

    # Şu anki şeklin görüntüsünü döndürür
    def image(self):
        return self.figures[self.type][self.rotation]

    # Şekli döndürür
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I şekli
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # O şekli
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # T şekli
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # S şekli
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # Z şekli
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # J şekli
        [[1, 2, 5, 6]],  # L şekli
    ]
