# Coisas para fazer:
# - Sistema para criar mapas proceduralmente
# - Sistema de game over
# - Aumentar dificuldade conforme o tempo

import pygame
import math
import time
import random

import weapons
# import waveFunctionCollapse
import enemies

# Iniciação do jogo
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("PyClashers")
screenWidth, screenHeight = pygame.display.get_surface().get_size()
screenWidthBy64, screenHeightBy64 = math.ceil(screenWidth/64), math.ceil(screenHeight/64)

logoPy = pygame.image.load('img/logoPy.png').convert_alpha()
logoClashers = pygame.image.load('img/logoClashers.png').convert_alpha()

imgIniciar = pygame.image.load('img/iniciar.png').convert_alpha()

imgGanhou = pygame.image.load('img/ganhou.png').convert_alpha()
imgPerdeu = pygame.image.load('img/perdeu.png').convert_alpha()

# Custom mouse
cursor_img = pygame.image.load('img/aim.png').convert_alpha()
cursor_img_rect = cursor_img.get_rect()

# Criar mapa
IDMap = []
floor1 = pygame.image.load('img/floor/grass.png').convert_alpha()
floor2 = pygame.image.load('img/floor/floor_plants.png').convert_alpha()


def createMap():
    for xIndex in range(0, screenWidthBy64):
        IDMap.append([])
        for yIndex in range(0, screenHeightBy64):
            x = random.randint(1, 6)
            IDMap[xIndex].append(x)


def drawMap():
    for xIndex in range(0, screenWidthBy64):
        for yIndex in range(0, screenHeightBy64):
            x = IDMap[xIndex][yIndex]
            match x:
                case 1:
                    screen.blit(floor1, (xIndex*64, yIndex*64))
                case 2:
                    screen.blit(floor1, (xIndex * 64, yIndex * 64))
                case 3:
                    screen.blit(floor1, (xIndex * 64, yIndex * 64))
                case 4:
                    screen.blit(floor1, (xIndex * 64, yIndex * 64))
                case 5:
                    screen.blit(floor2, (xIndex * 64, yIndex * 64))
                case 6:
                    screen.blit(floor2, (xIndex * 64, yIndex * 64))


# Posição do mouse
MousePosX, MousePosY = pygame.mouse.get_pos()

# Lista de inimigos
enemiesList = []

# Table para armazenar todos os disparos de cada personagem
allyBullets = []

# Coisas vitais para o jogo, o clock, se o jogo está rodando, etc
clock = pygame.time.Clock()
running = True
playing = False
gameover = False
dt = clock.tick(60) / 1000

winCountdown = 30000
roundStart = 0

gameoverCountdown = 2000
timeOfDeath = 0

firstSummonTime = -3000
lastEnemySummon = firstSummonTime

quantiaDeInimigos = 3

FONT = pygame.font.SysFont("arialblack", 80)


def draw_text(text, font, text_col, x, y):
    img = font.render(f"{text}", True, text_col)
    screen.blit(img, (x - img.get_width()/2, y))


# Função para rotacionar imagem em torno do próprio centro
def blitRotate2(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
    # pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)


class Player:
    def __init__(self):
        self.bodyImg = pygame.image.load('img/Characters/green_character.png').convert_alpha()
        # self.playerHand = pygame.image.load('img/Characters/green_hand.png').convert_alpha()

        self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.radius = 21

        self.bodyMask = pygame.mask.from_surface(self.bodyImg)
        # self.handMask = pygame.mask.from_surface(self.handImg)

        # self.maskImg = self.bodyMask.to_surface()

        self.weapon = weapons.BowArrow(allyBullets, self, 700, 900)
        self.ShotCooldown = self.weapon.cooldown
        self.lastShot = pygame.time.get_ticks() + 100

        self.anguloRadiano = -math.atan2(MousePosY - self.pos.y, MousePosX - self.pos.x)
        self.anguloDegrees = self.anguloRadiano * (180 / math.pi)

    def draw(self):
        self.anguloDegrees = -math.atan2(MousePosY - self.pos.y, MousePosX - self.pos.x) * (180 / math.pi)
        self.anguloRadiano = math.radians(self.anguloDegrees)

        # screen.blit(self.maskImg, (self.pos.x, self.pos.y))
        # blitRotate2(screen, self.maskImg, (self.pos.x - self.radius, self.pos.y - self.radius), self.anguloDegrees)

        # Jogador
        blitRotate2(screen, self.bodyImg, (self.pos.x - self.radius, self.pos.y - self.radius), self.anguloDegrees)
        # pygame.draw.circle(screen, "green", self.pos, 3)

        # Arma
        self.weapon.draw(screen, player, self.anguloDegrees)

    def attack(self):
        if pygame.time.get_ticks() - player.lastShot >= player.ShotCooldown:
            self.lastShot = pygame.time.get_ticks()
            self.weapon.fire()


player = Player()


# Quando acionado, gera outro mapa
def resetMap():
    global player
    time.sleep(dt)
    IDMap.clear()
    allyBullets.clear()
    enemies.enemyBullets.clear()
    enemiesList.clear()
    pygame.mouse.set_visible(True)
    createMap()
    # waveFunctionCollapse.wfc(screenWidthBy64, screenHeightBy64)


createMap()

while running:
    MousePosX, MousePosY = pygame.mouse.get_pos()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mousePressed = pygame.mouse.get_pressed()

    # Finalizar o jogo
    if keys[pygame.K_ESCAPE]:
        running = False

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Desenhar tela
    screen.fill("gray")

    if not playing and gameover:
        if timeOfDeath + gameoverCountdown >= pygame.time.get_ticks():
            screen.blit(imgPerdeu, pygame.Vector2((screenWidth - imgPerdeu.get_width())/2, screenHeight/3))
        else:
            gameover = False

    if not playing and not gameover:
        drawMap()

        screen.blit(logoPy, pygame.Vector2((screenWidth - logoPy.get_width() - logoClashers.get_width())/2, screenHeight/3))
        screen.blit(logoClashers, pygame.Vector2((screenWidth + logoPy.get_width() - logoClashers.get_width()) / 2, screenHeight/3 + (logoPy.get_height() - logoClashers.get_height())))

        padding = 30

        buttonPosition = pygame.Vector2((screenWidth - imgIniciar.get_width())/2 - padding/2, screenHeight/2 + 70 - padding/2)
        buttonSize = pygame.Vector2(imgIniciar.get_width() + padding, imgIniciar.get_height() + padding)

        # Ilustrar botão para jogar
        pygame.draw.rect(screen, (0, 255, 0), (buttonPosition, buttonSize), 0, 300)
        screen.blit(imgIniciar, pygame.Vector2((screenWidth - imgIniciar.get_width())/2, screenHeight/2 + 70))

        if mousePressed[0]:
            if (screenWidth - imgIniciar.get_width())/2 - padding/2 <= MousePosX <= (screenWidth + imgIniciar.get_width())/2 + padding/2 and screenHeight/2 + 70 - padding/2 <= MousePosY <= screenHeight/2 + 70 + padding/2 + imgIniciar.get_height():
                playing = True
                pygame.mouse.set_visible(False)
                roundStart = pygame.time.get_ticks()
                lastEnemySummon = firstSummonTime
                quantiaDeInimigos = 3

                player = Player()

    if playing and not gameover:
        elapsedTime = pygame.time.get_ticks() - roundStart

        drawMap()
        if pygame.time.get_ticks() - roundStart >= winCountdown:
            if len(enemiesList) > 0:
                draw_text("Elimine todos os inimigos para vencer", FONT, (0, 0, 0), screen.get_width()/2, 200)
            else:
                draw_text("Você ganhou!", FONT, (0, 0, 0), screen.get_width()/2, 200)
                enemies.enemyBullets.clear()
        else:
            elapsedTime = pygame.time.get_ticks() - roundStart
            timeRemaining = winCountdown - elapsedTime
            draw_text(math.ceil(timeRemaining/1000), FONT, (0, 0, 0), screen.get_width()/2, 200)

            if elapsedTime - lastEnemySummon >= 7000:
                lastEnemySummon = elapsedTime

                for i in range(0, quantiaDeInimigos):
                    enemiesList.append(enemies.EnemyBowArrow(screen, player.pos.x, player.pos.y, dt))

                quantiaDeInimigos += 1

        player.draw()

        for enemy in enemiesList:
            enemy.dt = dt
            enemy.acquireTarget(player.pos.x, player.pos.y)
            enemy.draw()
            enemy.walk()
            enemy.attack()

        # Custom mouse
        cursor_img_rect.center = MousePosX, MousePosY
        screen.blit(cursor_img, cursor_img_rect)

        # Colisão
        for allyBullet in allyBullets:
            if -64 < allyBullet.x < screenWidth + 64 and -64 < allyBullet.y < screenHeight + 64:
                for enemy in enemiesList:
                    if allyBullet.mask.overlap(enemy.bodyMask, ((enemy.pos.x - enemy.radius) - allyBullet.rotated_rect[0], (enemy.pos.y - enemy.radius) - allyBullet.rotated_rect[1])):
                        allyBullets.pop(allyBullets.index(allyBullet))
                        enemiesList.pop(enemiesList.index(enemy))
                        # enemy.bodyImg = pygame.image.load('img/Characters/yellow_character.png').convert_alpha()
                        break
                    # else:
                        # enemy.bodyImg = pygame.image.load('img/Characters/red_character.png').convert_alpha()

                allyBullet.x += dt * allyBullet.vel * math.cos(allyBullet.shootAngle)
                allyBullet.y += dt * allyBullet.vel * -math.sin(allyBullet.shootAngle)
            else:
                allyBullets.pop(allyBullets.index(allyBullet))

            allyBullet.draw(screen)

        for enemyBullet in enemies.enemyBullets:
            if -64 < enemyBullet.x < screenWidth + 64 and -64 < enemyBullet.y < screenHeight + 64:
                if enemyBullet.mask.overlap(player.bodyMask, ((player.pos.x - player.radius) - enemyBullet.rotated_rect[0], (player.pos.y - player.radius) - enemyBullet.rotated_rect[1])):
                    playing = False
                    gameover = True
                    resetMap()
                    timeOfDeath = pygame.time.get_ticks()

                enemyBullet.x += dt * enemyBullet.vel * math.cos(enemyBullet.shootAngle)
                enemyBullet.y += dt * enemyBullet.vel * -math.sin(enemyBullet.shootAngle)
            else:
                enemies.enemyBullets.pop(enemies.enemyBullets.index(enemyBullet))

            enemyBullet.draw(screen)

        if keys[pygame.K_SPACE] or mousePressed[0]:
            player.attack()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player.pos.y > player.radius:
                player.pos.y -= 170 * dt

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player.pos.y < screenHeight - player.radius:
                player.pos.y += 170 * dt

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player.pos.x > player.radius:
                player.pos.x -= 170 * dt

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player.pos.x < screenWidth - player.radius:
                player.pos.x += 170 * dt

        if keys[pygame.K_QUOTE]:
            playing = False
            gameover = True
            resetMap()

    # Atualizar tela do jogo
    pygame.display.flip()

    # Definir FPS do jogo para 60 FPS
    dt = clock.tick(60) / 1000

pygame.quit()
