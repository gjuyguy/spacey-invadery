# Create your own shooter

from pygame import *
from random import randint

WIDTH = 700
HEIGHT = 500

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("SPACE INVADERS")

background = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, image_path, x, y, speed, width, height, hp):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x <= WIDTH - 85:
            self.rect.x += self.speed

    def fire(self):
        fire_sound.play()
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 8, 10, 1)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed

        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0
            missed += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.x = randint(80, WIDTH - 80)
            self.rect.y = 0

score = 0
missed = 0

game_running = True
game_finished = False

player = Player("rocket.png", 350, HEIGHT - 100, 6, 80, 100, 1)

enemies = sprite.Group()
debris = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(80, WIDTH - 80), -40, randint(1, 5), 100, 50, 1)
    enemies.add(enemy)
for i in range(3):
    rocks = Asteroid("asteroid.png",randint(80, WIDTH - 80), -40, randint(1, 5), 50, 50,3)
    debris.add(rocks)

bullets = sprite.Group()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

font.init()
game_font = font.SysFont('Arial', 36)
end_font = font.SysFont('Arial', 72)

clock = time.Clock()


while game_running:


    for e in event.get():
        if e.type == QUIT:
            game_running = False

        # One bullet per key press
        if e.type == KEYDOWN:
            if e.key == K_UP:
                player.fire()

    if not game_finished:

        # Background
        window.blit(background, (0, 0))

        # Player
        player.update()
        player.reset()

        # Bullets
        bullets.update()

        # Enemies
        enemies.update()
        debris.update()

        # Draw enemies & bullets + collisions
        enemies.draw(window)
        debris.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(enemies,bullets,True,True)
        rockhits = sprite.groupcollide(debris,bullets,False,True)
        for asteroid in rockhits:
            asteroid.hp -= 1
            if asteroid.hp <= 0:
                asteroid.kill()
                newrocks = Asteroid("asteroid.png",randint(80, WIDTH - 80), -40, randint(1, 5), 50, 50,3)
                debris.add(newrocks)
        for c in collides:
            score += 1
            enemy = Enemy("ufo.png", randint(80, WIDTH - 80), -40, randint(1, 5), 100, 50,1)
            enemies.add(enemy)

        # Score + Win
        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(score_text, (10, 20))
        if score >= 100:
            fin_text = end_font.render("you WIN!", True, (255, 215, 0))
            window.blit(fin_text, (WIDTH/3, HEIGHT/2.5))
            game_finished = True

        # Missed + Lose
        missed_text = game_font.render(f"Missed: {missed}", True, (255, 255, 255))
        window.blit(missed_text, (10, 50))
        if missed >= 10 or sprite.spritecollide(player,debris,False):
            fin_text = end_font.render("you LOSE!", True, (220,20,60))
            window.blit(fin_text, (WIDTH/3, HEIGHT/2.5))
            game_finished = True


    display.update()
    clock.tick(60)