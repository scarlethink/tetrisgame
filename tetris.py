from figure import Figür
from game_state import State


# Tetris oyun sınıfı
class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = State.INGAME
        self.field = []  # Oyun alanının 2 boyutlu matrisi
        self.height = height
        self.width = width
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None

        # Oyun alanını sıfırlarla doldur
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = Figür(3, 0)

    def sinir_kontrolu(
        self,
    ):  # Oyun alanındaki sınırları veya diğer şekillerle çakışıp çakışmadığını kontrol eder
        sinir_kontrolu = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (
                        i + self.figure.y > self.height - 1
                        or j + self.figure.x > self.width - 1
                        or j + self.figure.x < 0
                        or self.field[i + self.figure.y][j + self.figure.x] > 0
                    ):
                        sinir_kontrolu = True
        return sinir_kontrolu

    def satirlari_temizle(self):  # Tamamlanan satırları tespit eder ve temizler
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines**2

    def sekil_dusurme(self):
        while not self.sinir_kontrolu():
            self.figure.y += 1
        self.figure.y -= 1
        self.dondurma()

    def asagi(self):
        self.figure.y += 1
        if self.sinir_kontrolu():
            self.figure.y -= 1
            self.dondurma()

    def dondurma(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.satirlari_temizle()
        self.new_figure()
        if self.sinir_kontrolu():
            self.state = State.GAME_OVER

    def yatay(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.sinir_kontrolu():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.sinir_kontrolu():
            self.figure.rotation = old_rotation
