import pygame
import random

# pygame'i başlatma
pygame.init()

# Renk tanımları
renkler = [
    (0, 0, 0),  # Siyah (arka plan rengi)
    (120, 37, 179),  # Mor
    (100, 179, 179),  # Açık mavi
    (80, 34, 22),  # Koyu kahverengi
    (80, 134, 22),  # Yeşil
    (180, 34, 22),  # Kırmızı
    (180, 34, 122),  # Pembe
]

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

# Tetris oyun sınıfı
class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "başla"
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

    def sinir_kontrolu(self):  # Oyun alanındaki sınırları veya diğer şekillerle çakışıp çakışmadığını kontrol eder
        sinir_kontrolu = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
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
        self.score += lines ** 2

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
            self.state = "oyunover"

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

# Ekstra renkler
siyah = (0, 0, 0)
beyaz = (255, 255, 255)
gri = (128, 128, 128)

# Pygame ekran boyutu ve ayarları
boyut = (400, 500)
ekran = pygame.display.set_mode(boyut)
pygame.display.set_caption("Tetris")

# Kullanıcı pencereyi kapatana kadar döngü devam eder
oyun_dongusu_bitti_mi = False  # Oyun döngüsünün bitip bitmediğini kontrol eden bayrak
zamanlayici = pygame.time.Clock()  # Oyun içindeki zamanlamayı ve FPS kontrolünü sağlayan nesne
fps = 25  # Saniyedeki kare sayısı
oyun = Tetris(20, 10)  # Tetris oyun nesnesini oluşturur; oyun tahtası 20 yüksekliğinde ve 10 genişliğinde
sayac = 0  # Sayaç değişkeni; oyun döngüsünde süre veya koşul kontrolü için kullanılır

asagiya_basma = False

while not oyun_dongusu_bitti_mi:
    
    # Eğer mevcut bir şekil yoksa yeni bir şekil oluştur
    if oyun.figure is None:
        oyun.new_figure()
    
    # Sayaç değerini artır
    sayac += 1
    
    # Sayaç çok büyükse sıfırla
    if sayac > 100000:
        sayac = 0

    # FPS ve oyun seviyesine göre aşağı hareket etmeyi kontrol et veya aşağı ok tuşuna basılıp basılmadığını kontrol et
    if sayac % (fps // oyun.level // 2) == 0 or asagiya_basma:
        if oyun.state == "başla":
            oyun.asagi()

    # pygame olaylarını kontrol et
    for event in pygame.event.get():
        # Pencere kapatıldığında döngüyü bitir
        if event.type == pygame.QUIT:
            oyun_dongusu_bitti_mi = True
        # Klavye tuşlarına basıldığında çeşitli işlemleri yap
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                oyun.rotate()  # Yukarı ok tuşuna basıldığında şekli döndür
            if event.key == pygame.K_DOWN:
                asagiya_basma = True  # Aşağı ok tuşuna basıldığında aşağıya hareketi hızlandır
            if event.key == pygame.K_LEFT:
                oyun.yatay(-1)  # Sol ok tuşuna basıldığında şekli sola hareket ettir
            if event.key == pygame.K_RIGHT:
                oyun.yatay(1)  # Sağ ok tuşuna basıldığında şekli sağa hareket ettir
            if event.key == pygame.K_SPACE:
                oyun.sekil_dusurme()  # Boşluk tuşuna basıldığında şekli hızlıca aşağıya hareket ettir
            if event.key == pygame.K_ESCAPE:
                oyun_dongusu_bitti_mi = True  # ESC tuşuna basıldığında oyunu kapat 

        # Tuş bırakıldığında aşağı hareketi hızlandırmayı durdur
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                asagiya_basma = False

    # Ekranı beyaz ile doldur
    ekran.fill(beyaz)

    # Oyun tahtasını çiz
    for i in range(oyun.height):
        for j in range(oyun.width):
            pygame.draw.rect(ekran, gri, [oyun.x + oyun.zoom * j, oyun.y + oyun.zoom * i, oyun.zoom, oyun.zoom], 1)
            if oyun.field[i][j] > 0:
                pygame.draw.rect(ekran, renkler[oyun.field[i][j]],
                                 [oyun.x + oyun.zoom * j + 1, oyun.y + oyun.zoom * i + 1, oyun.zoom - 2, oyun.zoom - 2])

    # Mevcut şekli çiz
    if oyun.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in oyun.figure.image():
                    pygame.draw.rect(ekran, renkler[oyun.figure.color],
                                     [oyun.x + oyun.zoom * (j + oyun.figure.x) + 1,
                                      oyun.y + oyun.zoom * (i + oyun.figure.y) + 1,
                                      oyun.zoom - 2, oyun.zoom - 2])

    # Ekranı güncelle
    pygame.display.update()

    # FPS kontrolü
    zamanlayici.tick(fps)

    # Skor ve oyun bitti mesajlarını ekranda güncelle
    font = pygame.font.SysFont('Arial', 25, True, False)
    font1 = pygame.font.SysFont('Arial', 65, True, False)
    text = font.render("Skor: " + str(oyun.score), True, siyah)
    text_game_over = font1.render("Kaybettin", True, (255, 125, 0))
    text_game_over1 = font1.render("ESC bas", True, (255, 215, 0))

    ekran.blit(text, [0, 0])
    if oyun.state == "oyunover":
        ekran.blit(text_game_over, [20, 200])
        ekran.blit(text_game_over1, [25, 265])

pygame.display.update()  # <--- Add this line
    
pygame.quit()
