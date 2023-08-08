import pygame
import os
pygame.init()

def file_path(filename ):
    folder = os.path.abspath(__file__ + "/..")
    path = os.path.join(folder, filename)
    return path

TILE = 30
WIN_WIDTH = 30 * TILE
WIN_HEIGHT = 14 * TILE
FPS = 40
BLUE_FON = (95, 130, 180)

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(image))
        self.image = pygame.transform.scale(self.image, (width, height))

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0
        self.jumped = False
        self.can_jump = True
        

    def update(self):
        dx, dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx -= 5
        if keys[pygame.K_RIGHT]:
            dx += 5
        if keys[pygame.K_SPACE] and not self.jumped and self.can_jump:
            self.gravity = -15
            self.jumped = True
        if not keys[pygame.K_SPACE]:
            self.jumped = False

        # гравитация
        self.gravity += 1
        if self.gravity > 10:
            self.gravity = 10
        dy += self.gravity


        self.rect.x += dx
        blocks_touched = pygame.sprite.spritecollide(self, objects, False)
        if dx > 0:
            for block in blocks_touched:
                self.rect.right = min(self.rect.right, block.rect.left)
        elif dx < 0:
            for block in blocks_touched:
                self.rect.left = max(self.rect.left, block.rect.right)
        
        self.can_jump = False
        self.rect.y += dy
        blocks_touched = pygame.sprite.spritecollide(self, objects, False)
        for block in blocks_touched:
            if dy >= 0:
                self.rect.bottom = min(self.rect.bottom, block.rect.top)
                self.can_jump = True
            elif dy < 0:
                self.rect.top = max(self.rect.top, block.rect.bottom)
                self.gravity = 0

        self.show()

level = [
    "1                            1",
    "1                            1",
    "12222224                     1",
    "1                            1",
    "1        3224                1",
    "1                3222        1",
    "1                            1",
    "1                      3222221",
    "1                            1",
    "1                   2        1",
    "1                            1",
    "1              3224          1",
    "1                            1",
    "122222222222222222222222222221"
]

objects = pygame.sprite.Group()
for row in range(len(level)):
    for col in range(len(level[row])):
        if level[row][col] == "1":
            obj = GameSprite(col * TILE, row * TILE, TILE, TILE, r"t2.png")
            objects.add(obj)
        elif level[row][col] == "2":
            obj = GameSprite(col * TILE, row * TILE, TILE, TILE, r"t1.png")
            objects.add(obj)
        elif level[row][col] == "3":
            obj = GameSprite(col * TILE, row * TILE, TILE, TILE, r"t1-l.png")
            objects.add(obj)
        elif level[row][col] == "4":
            obj = GameSprite(col * TILE, row * TILE, TILE, TILE, r"t1-r.png")
            objects.add(obj)
        
player = Player(100, 100, 22, 26, r"player.png")

level = 0
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
 
    window.fill(BLUE_FON)
    objects.draw(window)
    player.update()

    clock.tick(FPS)
    pygame.display.update()


