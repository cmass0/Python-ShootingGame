import pygame
from pygame.rect import *
import random
import sys

difficulty = 0


def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(recSnowball)):
        recSnowball[i].y = -1
    for i in range(len(recFireball)):
        recFireball[i].y = -1


def showModeSelection():
    global SCREEN_WIDTH, SCREEN_HEIGHT, difficulty

    pygame.init()
    mode_screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('게임 모드 선택')

    font = pygame.font.Font(None, 36)
    modes = ['Easy', 'Normal', 'Hard']
    mode_rects = []

    for i, mode in enumerate(modes):
        rect = pygame.Rect(50, 50 + i * 50, 200, 40)
        pygame.draw.rect(mode_screen, (200, 200, 200), rect)
        pygame.draw.rect(mode_screen, (0, 0, 0), rect, 2)

        text = font.render(mode, True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        mode_screen.blit(text, text_rect)

        mode_rects.append(rect)

    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                x, y = e.pos
                for i, rect in enumerate(mode_rects):
                    if rect.collidepoint(x, y):
                        pygame.quit()
                        if i == 0:
                            difficulty = 1
                            SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
                        elif i == 1:
                            difficulty = 2
                            SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
                        elif i == 2:
                            difficulty = 3
                            SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
                        return
        pygame.time.Clock().tick(30)

# 초기 모드 선택
# selectMode()  # 주석처리: 해당 함수가 정의되지 않아 에러 발생


# 게임 모드 선택 창 표시
showModeSelection()


def restart():
    global isGameOver, score
    isGameOver = False
    score = 0
    for i in range(len(snowball)):
        recSnowball[i].y = -1
    for i in range(len(fireball)):
        recFireball[i].y = -1


def eProcess():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                pygame.quit()

            if e.key == pygame.K_LEFT:
                if difficulty != 3:
                    move.x -= 3
                else:
                    move.x -= 2
            if e.key == pygame.K_RIGHT:
                if difficulty != 3:
                    move.x += 3
                else:
                    move.x = 2
            if e.key == pygame.K_UP:
                if difficulty != 3:
                    move.y -= 3
                else:
                    move.y -= 2
            if e.key == pygame.K_DOWN:
                if difficulty != 3:
                    move.y += 3
                else:
                    move.y = 2
            if e.key == pygame.K_r:
                current_music_key = "bgm1"
                pygame.mixer.music.load(f"{current_music_key}.mp3")
                pygame.mixer.music.play(-1)
                restart()
            if e.key == pygame.K_SPACE:
                makeFireball()
        if e.type == pygame.KEYUP:
            if difficulty != 3:
                if e.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    move.x = 0
                if e.key in [pygame.K_UP, pygame.K_DOWN]:
                    move.y = 0


def movePlayer():
    if not isGameOver:
        recPlayer.x += move.x
        recPlayer.y += move.y

    if recPlayer.x < 0:
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH - recPlayer.width:  # 오타 수정
        recPlayer.x = SCREEN_WIDTH - recPlayer.width

    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT - recPlayer.height:
        recPlayer.y = SCREEN_HEIGHT - recPlayer.height

    SCREEN.blit(player, recPlayer)


def timeDelay500ms():
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True

    time_delay_500ms += 1
    return False


def makeSnowball():
    if isGameOver:
        return
    if timeDelay500ms():
        idex = random.randint(0, len(snowball) - 1)
        if recSnowball[idex].y == -1:
            recSnowball[idex].x = random.randint(0, SCREEN_WIDTH)
            recSnowball[idex].y = 0


def moveSnowball():
    makeSnowball()

    for i in range(len(snowball)):
        if recSnowball[i].y == -1:
            continue

        if not isGameOver:
            if difficulty != 3:
                recSnowball[i].y += 1 + difficulty
            else:
                recSnowball[i].y += 1.5
        if recSnowball[i].y > SCREEN_HEIGHT:
            recSnowball[i].y = 0

        SCREEN.blit(snowball[i], recSnowball[i])


def CheckCollisionFireball():
    global score, isGameOver
    if isGameOver:
        return
    for rec in recSnowball:
        if rec.y == -1:
            continue
        for recF in recFireball:
            if recF.y == -1:
                continue
            if rec.top < recF.bottom \
                    and recF.top < rec.bottom \
                    and rec.left < recF.right \
                    and recF.left < rec.right:
                rec.y = -1
                recF.y = -1
                score += 10
                print(rec, recF)
                break


def makeFireball():
    global isGameOver, last_fireball_time

    if isGameOver:
        return

    current_time = pygame.time.get_ticks()
    if current_time - last_fireball_time >= 500:  # 0.5초 (500ms)마다 발사
        last_fireball_time = current_time

        for i in range(len(fireball)):
            if recFireball[i].y == -1:
                recFireball[i].x = recPlayer.x
                recFireball[i].y = recPlayer.y
                break


def moveFireball():
    for i in range(len(fireball)):
        if recFireball[i].y == -1:
            continue

        if not isGameOver:
            recFireball[i].y -= 3.8
        if recFireball[i].y < 0:
            recFireball[i].y = -1

        SCREEN.blit(fireball[i], recFireball[i])


def CheckCollision():
    global score, isGameOver

    if isGameOver:
        pygame.mixer.music.stop()
        return

    for rec in recSnowball:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
                and recPlayer.top < rec.bottom \
                and rec.left < recPlayer.right \
                and recPlayer.left < rec.right:
            print('충돌')
            isGameOver = True
            break
    # score += 1


def blinking():
    global time_delay_4sec, toggle
    time_delay_4sec += 1
    if time_delay_4sec > 40:
        time_delay_4sec = 0
        toggle = ~toggle

    return toggle


def setText():
    mFont = pygame.font.SysFont("arial", 20, True, False)
    SCREEN.blit(mFont.render(
        f'score : {score}', True, 'green'), (10, 10, 0, 0))

    if isGameOver and blinking():
        SCREEN.blit(mFont.render(
            'Game Over!!', True, 'red'), (150, 300, 0, 0))
        SCREEN.blit(mFont.render(
            'press R - Restart', True, 'red'), (140, 320, 0, 0))


# 1. 변수초기화
isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0)
time_delay_500ms = 0
time_delay_4sec = 0
toggle = False
score = 0
isGameOver = False
last_fireball_time = 0

# 2. 스크린생성
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('눈덩이 피하기 게임')

# 배경 이미지 불러오기
# 'background.jpg'를 사용자가 가진 이미지 파일로 대체
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 3. player 생성
player = pygame.image.load('snowman.png')
player = pygame.transform.scale(player, (30, 30))
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH / 2)
recPlayer.centery = (SCREEN_HEIGHT / 2)

# 4. 눈덩이 생성
snowball = [pygame.image.load('snowball.png') for i in range(40)]
recSnowball = [None for i in range(len(snowball))]
for i in range(len(snowball)):
    snowball[i] = pygame.transform.scale(snowball[i], (20, 20))
    recSnowball[i] = snowball[i].get_rect()
    recSnowball[i].y = -1

# 4. 불덩이 생성
fireball = [pygame.image.load('fireball.png') for i in range(40)]
recFireball = [None for i in range(len(fireball))]
for i in range(len(fireball)):
    fireball[i] = pygame.transform.scale(fireball[i], (20, 20))
    recFireball[i] = fireball[i].get_rect()
    recFireball[i].y = -1

# 5. bgm
clock = pygame.time.Clock()
current_music_key = "bgm1"
pygame.mixer.music.load(f"{current_music_key}.mp3")
pygame.mixer.music.play(-1)

# 6. 기타

##### 반복####

while isActive:

    # 1.화면 지움
    SCREEN.fill((0, 0, 0))
    # 배경 이미지 그리기
    SCREEN.blit(background_image, (0, 0))

    # 2.이벤트처리
    eProcess()
    # 3.플레이어 이동
    movePlayer()
    # 4.눈덩이 생성 및 이동
    moveSnowball()
    # 4.불덩이 생성 및 이동
    moveFireball()
    # 5.충돌 확인
    CheckCollisionFireball()
    CheckCollision()
    # 6.text업데이트
    setText()
    # 7 bgm2로 변경
    if score >= 200 and current_music_key == "bgm1":
        pygame.mixer.music.stop()
        current_music_key = "bgm2"
        pygame.mixer.music.load(f"{current_music_key}.wav")
        pygame.mixer.music.play(-1)
    # 8.화면 갱신
    pygame.display.flip()
    clock.tick(100)
##### 반복####