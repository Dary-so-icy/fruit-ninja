import pygame
import sys
import os
import random

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Sprites(pygame.sprite.Sprite):
    def __init__(self, im):
        super().__init__(fruits)
        self.image = load_image(im)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(10, 700)
        self.rect.y = 730


    def update(self, *args):
        self.rect = self.rect.move(0, -1)
        if self.rect.y < 0:
            self.rect.x = random.randrange(10, 700)
            self.rect.y = 730


class AnimatedSprites(pygame.sprite.Sprite):
    pass


def terminate():
    pygame.quit()
    sys.exit()


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
        string_rendered = font.render(line, 1, pygame.Color('white'))
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


def generate_level():
    Tile()


pygame.init()
all_sprites = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
generate_level()
running = True
pygame.init()
clock = pygame.time.Clock()
size = WIDTH, HEIGHT = 1280, 730
screen = pygame.display.set_mode(size)
start_screen()
fruits = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
# определим его вид
data = ['Red_Apple.png', 'Coconut.png','Green_Apple.png', 'Mango.png', 'Pineapple.png']
for im in data:
    Sprites(im)

if __name__ == '__main__':
    cur_image = load_image('arrow.png')
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = cur_image
    cursor.rect = cursor.image.get_rect()
    pygame.mouse.set_visible(False)
    while running:
        screen.fill('white')
        all_sprites.draw(screen)
        fruits.draw(screen)
        fruits.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.x = event.pos[0]
                cursor.rect.y = event.pos[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
        if pygame.mouse.get_focused():
            cursor_group.draw(screen)

        pygame.display.flip()

    pygame.quit()