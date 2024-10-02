import pygame

from colors import beyaz, gri, renkler, siyah
from tetris import Tetris

# pygame'i başlatma
pygame.init()


# Pygame ekran boyutu ve ayarları
boyut = (400, 500)
ekran = pygame.display.set_mode(boyut)
pygame.display.set_caption("Tetris")

# Kullanıcı pencereyi kapatana kadar döngü devam eder
oyun_dongusu_bitti_mi = False  # Oyun döngüsünün bitip bitmediğini kontrol eden bayrak
zamanlayici = (
    pygame.time.Clock()
)  # Oyun içindeki zamanlamayı ve FPS kontrolünü sağlayan nesne
fps = 25  # Saniyedeki kare sayısı
oyun = Tetris(
    20, 10
)  # Tetris oyun nesnesini oluşturur; oyun tahtası 20 yüksekliğinde ve 10 genişliğinde
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
                asagiya_basma = (
                    True  # Aşağı ok tuşuna basıldığında aşağıya hareketi hızlandır
                )
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
            pygame.draw.rect(
                ekran,
                gri,
                [oyun.x + oyun.zoom * j, oyun.y + oyun.zoom * i, oyun.zoom, oyun.zoom],
                1,
            )
            if oyun.field[i][j] > 0:
                pygame.draw.rect(
                    ekran,
                    renkler[oyun.field[i][j]],
                    [
                        oyun.x + oyun.zoom * j + 1,
                        oyun.y + oyun.zoom * i + 1,
                        oyun.zoom - 2,
                        oyun.zoom - 2,
                    ],
                )

    # Mevcut şekli çiz
    if oyun.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in oyun.figure.image():
                    pygame.draw.rect(
                        ekran,
                        renkler[oyun.figure.color],
                        [
                            oyun.x + oyun.zoom * (j + oyun.figure.x) + 1,
                            oyun.y + oyun.zoom * (i + oyun.figure.y) + 1,
                            oyun.zoom - 2,
                            oyun.zoom - 2,
                        ],
                    )

    # Ekranı güncelle
    pygame.display.update()

    # FPS kontrolü
    zamanlayici.tick(fps)

    # Skor ve oyun bitti mesajlarını ekranda güncelle
    font = pygame.font.SysFont("Arial", 25, True, False)
    font1 = pygame.font.SysFont("Arial", 65, True, False)
    text = font.render("Skor: " + str(oyun.score), True, siyah)
    text_game_over = font1.render("Kaybettin", True, (255, 125, 0))
    text_game_over1 = font1.render("ESC bas", True, (255, 215, 0))

    ekran.blit(text, [0, 0])
    if oyun.state == "oyunover":
        ekran.blit(text_game_over, [20, 200])
        ekran.blit(text_game_over1, [25, 265])

pygame.display.update()  # <--- Add this line

pygame.quit()
