import pygame
import math


# Função para rotacionar imagem em torno do próprio centro
def blitRotate2(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    # pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)


class Arrow:
    def __init__(self, x, y, projectileAngle, vel):
        self.img = pygame.image.load('img/Items/misc/weapon_arrow.png').convert_alpha()
        self.rectCenter = self.img.get_rect().center

        self.shootAngle = projectileAngle
        self.x = x
        self.y = y
        self.vel = vel

        self.rotated_image = pygame.transform.rotate(self.img, self.shootAngle * 180 / math.pi - 90)
        self.rotated_rect = self.rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x - self.rectCenter[0], self.y - self.rectCenter[1])).center)

        self.mask = pygame.mask.from_surface(self.rotated_image)
        self.maskImg = self.mask.to_surface()

    def draw(self, screen):
        self.rotated_rect = self.rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x - self.rectCenter[0], self.y - self.rectCenter[1])).center)
        # screen.blit(self.maskImg, self.rotated_rect)

        blitRotate2(screen, self.img, (self.x - self.rectCenter[0], self.y - self.rectCenter[1]), self.shootAngle * 180 / math.pi - 90)


class BowArrow:  # (pygame.sprite.Sprite):
    def __init__(self, allyBullets, player, cooldown, vel):
        # pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('img/Items/ranged/weapon_bow_arrow.png').convert_alpha()
        self.imgCooldown = pygame.image.load('img/Items/misc/weapon_bow.png').convert_alpha()
        self.cooldown = cooldown
        self.angle = 90
        self.vel = vel

        self.mask = pygame.mask.from_surface(self.img)

        self.allyBullets = allyBullets
        self.player = player

    def draw(self, screen, player, anguloDegrees):
        if pygame.time.get_ticks() - player.lastShot >= self.cooldown - 150:
            blitRotate2(screen, self.img, (player.pos.x - 32 + 2.2 * player.radius * math.cos(player.anguloRadiano),
                                           player.pos.y - 32 - 2.2 * player.radius * math.sin(player.anguloRadiano)),
                        anguloDegrees - self.angle)
        else:
            blitRotate2(screen, self.imgCooldown, (player.pos.x - 32 + 2.2 * player.radius * math.cos(player.anguloRadiano), player.pos.y - 32 - 2.2 * player.radius * math.sin(player.anguloRadiano)), anguloDegrees - self.angle)

    def fire(self):
        flechatemp = Arrow(self.player.pos.x + 2.5 * self.player.radius * math.cos(self.player.anguloRadiano), self.player.pos.y - 2.5 * self.player.radius * math.sin(self.player.anguloRadiano), self.player.anguloRadiano, self.vel)
        self.allyBullets.append(flechatemp)


class Spear:
    def __init__(self):
        self.img = pygame.image.load('img/Items/melee/weapon_spear.png').convert_alpha()
        self.windup = 200
        self.cooldown = 400
        self.overshootAngle = 100

        self.mask = pygame.mask.from_surface(self.img)

    # def fire(self):
    #     print("Fired")
