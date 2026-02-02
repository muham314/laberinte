import pygame
import random
import time
import math
TILE_SIZE = 40

maze = [
    "###############",
    "#.....#.......#",
    "#.###.#.##..#.#",
    "#.#...#.#...#.#",
    "#.#.###.#.###.#",
    "#.#.....#.....#",
    "#.#######.#####",
    "#.............#",
    "###.###########",
    "#...#.....#...#",
    "#.#.#.###.#.#.#",
    "#.#.#...#.#.#.#",
    "#.#.###.#.#.#.#",
    "#.#.....#.....#",
    "#.#######.#####",
    "#.............#",
    "###.###########",
    "#.....#.....#.#",
    "#.###.#.##..#.#",
    "#.#...#.#...#.#",
    "#.#.###.#.###.#",
    "#.#.....#.....#",
    "#.#######.#####",
    "#.............#",
    "###############"
]

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5

    def move(self, dx, dy, walls):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x -= dx

        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.y -= dy

    def draw(self, screen):
        pygame.draw.rect(screen, (173, 255, 47), self.rect)

class Wall:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 127, 80), self.rect)

class Coin:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x+10,y+10,20,20)

    def draw(self,screen):
        pygame.draw.ellipse(screen, (255,255,0), self.rect)
        
class Door:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,40,40)

    def draw(self,screen):
        pygame.draw.rect(screen, (0,0,0),self.rect)

class Ghost:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,30,30)
        self.speed = 1
        self.spawn__time = time.time()
        self.life_time = random.randint(5,7)

    def update(self,player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx,dy)
        if distance !=0:
            dx /= distance
            dy /= distance

        self.rect.x +=dx * self.speed
        self.rect.y +=dy * self.speed

    def draw(self,screen):
        pygame.draw.ellipse(screen, (78,87,84),self.rect)

    def is_alive(self):
        return time.time() - self.spawn__time < self.life_time
    

class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(None,36)

        self.rows = len(maze)
        self.cols = max(len(row) for row in maze)
        self.maze = [row.ljust(self.cols, ' ') for row in maze]

        self.width = 600#
        self.height = 1000#
        self.screen = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Laberint")
        self.clock = pygame.time.Clock()
        self.running = True
        self.coin_count = 0
        self.walls = []
        self.free_cells = []
        self.coins = []
        self.door = None
        self.win = False 
        self.ghosts = []
        self.game_over = False
        self.last_ghost_time = time.time()
        self.ghost_delay = 8

        for row_index, row in enumerate(self.maze):#
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == "#":
                    self.walls.append(Wall(x, y, TILE_SIZE))
                else:
                    self.free_cells.append((x, y))

        if not self.free_cells:
            spawn_x, spawn_y = TILE_SIZE, TILE_SIZE
        else:
            spawn_x, spawn_y = random.choice(self.free_cells)

        self.player = Player(spawn_x, spawn_y)

        for _ in range(7):
            x,y = random.choice(self.free_cells)
            self.coins.append(Coin(x,y))


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        if self.win:
            print("Sie GEWONNEN!, das Spiel ist beenden")
        time.sleep(4)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        currect_time = time.time()

        if currect_time - self.last_ghost_time > self.ghost_delay:
            self.last_ghost_time = currect_time

            for _ in range(random.randint(1,2)):
                x,y = random.choice(self.free_cells)
                self.ghosts.append(Ghost(x,y))
        
        for ghost in self.ghosts[:]:
            ghost.update(self.player)

            if ghost.rect.colliderect(self.player.rect):
                self.game_over = True
                self.running = False

            if not ghost.is_alive():
                self.ghosts.remove(ghost)
                
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.coin_count +=1

        if self.coin_count >=6 and self.door is None:
            x,y = random.choice(self.free_cells)
            self.door = Door(x,y)

        if self.door and self.player.rect.colliderect(self.door.rect):
            self.win = True 
            self.running =False

                
        keys = pygame.key.get_pressed()

        dx = 0#
        dy = 0

        if keys[pygame.K_LEFT]:
            dx = -self.player.speed
        elif keys[pygame.K_RIGHT]:
            dx = self.player.speed
        if keys[pygame.K_UP]:
            dy = -self.player.speed
        elif keys[pygame.K_DOWN]:
            dy = self.player.speed

        self.player.move(dx, dy, self.walls)

    def draw(self):
        self.screen.fill((30, 30, 60))

        for ghost in self.ghosts: 
            ghost.draw(self.screen)

        for wall in self.walls:
            wall.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)
        
        if self.door:
            self.door.draw(self.screen)

        text = self.font.render(
            f"Coins: {self.coin_count}",True, (255,255,255)
        )
        self.screen.blit(text,(10,10))

        if self.win:
            text = self.font.render("GEWONEN!", True, (127,255,212))
            self.screen.blit(text, (300,250))

        if self.game_over:
            text = self.font.render("Sie haben ferloren", True, (255,0,0))
            self.screen.blit(text,(280,260))

        self.player.draw(self.screen)
        pygame.display.flip()

game = Game()
game.run()
