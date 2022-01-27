import pygame
import sys
import os
import random
import time
import datetime
import schedule

FPS = 50
PRICE = {'Red_Apple.png': 1, 'Coconut.png': 1, 'melon.png': 1, 'Mango.png': 1, 'Pineapple.png': 1,
         'Watermelon.png': 1, 'Banana.png': 1, 'Kiwi.png': 1, 'Lemon.png': 1,
         'Orange.png': 1, 'Pear.png': 1}
NAME_CHANGE = {'Red_Apple.png': ['apple12.png', 'apple2.png'], 'Coconut.png': ['coco1.png', 'coc2.png'],
               'melon.png': ['melon1.png', 'melon2.png'], 'Mango.png': ['mango1.png', 'mango2.png'],
               'Pineapple.png': ['pn1.png', 'pn2.png'],
               'Watermelon.png': ['watermelon1.png', 'watermelon2.png'], 'Banana.png': ['banana1.png', 'banana2.png'],
               'Kiwi.png': ['kiwi1.png', 'kiwi2.png'], 'Lemon.png': ['lemon1.png', 'lemon2.png'],
               'Orange.png': ['or1.png', 'or2.png'], 'Pear.png': ['pear1.png', 'pear2.png']}
global score
score = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def write_text(sc, text, size, x, y):  # функции для вывода текста
    font = pygame.font.Font(None, size)
    rendered = font.render(text, True, (255, 255, 255))
    rect = rendered.get_rect()
    rect.midtop = (x, y)
    screen.blit(rendered, rect)


class Sprites(pygame.sprite.Sprite):
    def __init__(self, im, cut=False, *args):
        super().__init__(all_sprites)
        self.name = im
        self.price = 2
        self.image = load_image(im)
        self.cut = cut
        self.flag = False
        if self.cut:
            self.rect = self.image.get_rect()
            self.rect.y = args[0][1]
            self.rect.x = args[0][0]
        else:
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(10, 1001)
            self.top = random.randrange(20, 150)
            self.rect.y = 730

    def update(self, *args):
        global score
        draw_score(20, 20, score)
        draw_time(600, 20)
        if not self.cut:
            if self.rect.y <= self.top:
                self.flag = True
            if self.flag:
                self.rect = self.rect.move(0, 5)
            else:
                self.rect = self.rect.move(0, -5)
        else:
            self.rect = self.rect.move(0, 8)

    def check(self, pos):
        global extra_time, score
        if int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                  self.rect.y +
                                                                                                  self.rect[
                                                                                                      3]) and self.name == 'Bomb.png':
            extra_time += 10
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                  self.rect.y +
                                                                                                  self.rect[
                                                                                                      3]) and self.name == 'Score_2x_Banana.png':
            score *= 2
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                  self.rect.y +
                                                                                                  self.rect[
                                                                                                      3]) and self.name == '5seconds_Banana.png':
            extra_time -= 5
            all_sprites.remove(self)
            return False
        elif int(pos[0]) in range(self.rect.x, self.rect.x + self.rect[2]) and int(pos[1]) in range(self.rect.y,
                                                                                                    self.rect.y +
                                                                                                    self.rect[3]):
            return True
        else:
            return False

    def change(self):
        global score
        score += 1
        im = NAME_CHANGE[self.name]
        for el in im:
            Sprites(el, True, [self.rect[0], self.rect[1], self.rect[2], self.rect[3]])
        all_sprites.remove(self)

    def sliced(self):
        return self.cut


def get_click(pos):
    for e in all_sprites:
        if not e.sliced():
            a = e.check(pos)
            if a:
                e.change()


def terminate():
    pygame.quit()
    sys.exit()


def draw_score(x, y, score):  # рисует счет
    write_text(screen, str(score), 30, x, y)


def draw_time(x, y):
    write_text(screen, f'Осталось {str(60 - round(end_time - start_time + extra_time))} секунд', 30, x, y)


def game_over():  # завершение игры, вывод счета
    global score
    game_over_text = [f'Вы набрали {score} очков',
                      'Кликните чтобы продолжить']
    fon = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 546
    for line in game_over_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 550
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 546
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 550
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = load_image('background.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = tile_images
        self.rect = self.image.get_rect()

    def sliced(self):
        return True

    def check(self, pos):
        return False

    def change(self):
        pass


def generate_level():
    Tile()


pygame.init()
all_sprites = pygame.sprite.Group()
generate_level()
running = True
pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 1280, 730
screen = pygame.display.set_mode(size)
start_screen()
start_time = time.time()
extra_time = 0
fruits = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
data = ['Red_Apple.png', 'Coconut.png', 'Mango.png', 'Pineapple.png', 'Bomb.png', 'Score_2x_Banana.png',
        '5seconds_Banana.png',
        'Watermelon.png', 'Banana.png', 'Kiwi.png', 'Lemon.png', 'Orange.png', 'Pear.png', 'melon.png']
# Score_2x_Banana удваивает счет, 10seconds_Banana добавляет 10 секунд времени, Bomb отнимает 5 секунд


def job():
    k = random.randrange(2, 5)
    for i in range(k):
        Sprites(data[random.randrange(0, 10)])


schedule.every(1).seconds.do(job)

if __name__ == '__main__':
    while running:
        end_time = time.time()
        schedule.run_pending()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                get_click(event.pos)
        for e in all_sprites:
            if e.rect.x < 0 or e.rect.x > WIDTH or e.rect.y < 0 or e.rect.y > HEIGHT:
                all_sprites.remove(e)
        if round(end_time - start_time + extra_time) >= 60:
            game_over()
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
