import random

import pygame
import weapons
import math

enemyBullets = []


# Função para rotacionar imagem em torno do próprio centro
def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    # pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)


class EnemyBowArrow:
    def __init__(self, screen, targetX, targetY, dt):
        self.bodyImg = pygame.image.load('img/Characters/red_character.png').convert_alpha()
        self.handImg = pygame.image.load('img/Characters/red_hand.png').convert_alpha()

        self.screen = screen
        self.dt = dt
        self.targetX = targetX
        self.targetY = targetY

        self.pos = self.randomPosition()
        self.radius = 21

        self.bodyMask = pygame.mask.from_surface(self.bodyImg)
        self.handMask = pygame.mask.from_surface(self.handImg)

        # self.bodyMaskImg = self.bodyMask.to_surface()

        # self.bodyRect = self.bodyImg.get_rect()

        self.weapon = weapons.BowArrow(enemyBullets, self, 3000, 900)
        self.ShotCooldown = self.weapon.cooldown
        self.lastShot = pygame.time.get_ticks() - self.ShotCooldown / 2

        self.anguloRadiano = -math.atan2(targetY - self.pos.y, targetX - self.pos.x)
        self.anguloDegrees = self.anguloRadiano * (180 / math.pi)

    def randomPosition(self):
        x0 = random.randint(-128, self.screen.get_width() + 128)

        y1 = random.randint(-64, -32)
        y2 = random.randint(self.screen.get_height() + 32, self.screen.get_height() + 64)
        y0 = random.choice([y1, y2])

        return pygame.Vector2(x0, y0)

    def acquireTarget(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY

    def walk(self):
        self.pos.x += 150 * math.cos(self.anguloRadiano) * self.dt
        self.pos.y += 150 * -math.sin(self.anguloRadiano) * self.dt

    def draw(self):
        self.anguloRadiano = -math.atan2(self.targetY - self.pos.y, self.targetX - self.pos.x)
        self.anguloDegrees = self.anguloRadiano * (180 / math.pi)

        self.weapon.draw(self.screen, self, self.anguloDegrees)
        blitRotate2(self.screen, self.bodyImg, (self.pos.x - self.radius, self.pos.y - self.radius), self.anguloDegrees)

        # self.screen.blit(self.bodyMaskImg, (self.pos.x - self.radius, self.pos.y - self.radius))

    def attack(self):
        if pygame.time.get_ticks() - self.lastShot >= self.ShotCooldown:
            self.lastShot = pygame.time.get_ticks()
            self.weapon.fire()


class EnemySpear:
    def __init__(self):
        self.bodyImg = pygame.image.load('img/Characters/red_character.png').convert_alpha()
        self.handImg = pygame.image.load('img/Characters/red_hand.png').convert_alpha()
        self.weapon = weapons.Spear()


class EnemyTemplate:
    def __init__(self, screen, targetX, targetY, dt):
        self.bodyImg = pygame.image.load('img/Characters/red_character.png').convert_alpha()
        self.handImg = pygame.image.load('img/Characters/red_hand.png').convert_alpha()

        self.screen = screen
        self.dt = dt
        self.targetX = targetX
        self.targetY = targetY

        self.pos = self.randomPosition()
        self.radius = 21

        self.weapon = weapons.BowArrow(enemyBullets, self, 3000, 900)
        self.ShotCooldown = self.weapon.cooldown
        self.lastShot = pygame.time.get_ticks() - self.ShotCooldown / 2

        self.anguloRadiano = -math.atan2(targetY - self.pos.y, targetX - self.pos.x)
        self.anguloDegrees = self.anguloRadiano * (180 / math.pi)

    def randomPosition(self):
        x0 = random.randint(-128, self.screen.get_width() + 128)

        y1 = random.randint(-128, -64)
        y2 = random.randint(self.screen.get_height() + 64, self.screen.get_height() + 128)
        y0 = random.choice([y1, y2])

        return pygame.Vector2(x0, y0)

    def acquireTarget(self, targetX, targetY):
        self.targetX = targetX
        self.targetY = targetY

    def walk(self):
        self.pos.x += 170 * math.cos(self.anguloRadiano) * self.dt
        self.pos.y += 170 * -math.sin(self.anguloRadiano) * self.dt

    def draw(self):
        self.anguloRadiano = -math.atan2(self.targetY - self.pos.y, self.targetX - self.pos.x)
        self.anguloDegrees = self.anguloRadiano * (180 / math.pi)

        self.weapon.draw(self.screen, self, self.anguloDegrees)
        blitRotate2(self.screen, self.bodyImg, (self.pos.x - self.radius, self.pos.y - self.radius), self.anguloDegrees)

    def attack(self):
        if pygame.time.get_ticks() - self.lastShot >= self.ShotCooldown:
            self.lastShot = pygame.time.get_ticks()
            self.weapon.fire()
