import pygame
import sys
import os

FPS = 50

class Sprites():
    print('Hello')

class AnimatedSprites():
    pass


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images
        self.rect = self.image.get_rect()


def generate_level():
    Tile()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
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
data = ['Red_Apple.jpg', 'Coconut.jpg','Green_Apple.png', 'Mango.png', 'Pineapple.png']
for im in data:
    sprite.image = load_image(im)
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)

if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
        screen.fill('white')
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
