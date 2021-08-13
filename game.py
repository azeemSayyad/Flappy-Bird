import random
import sys
import pygame
from pygame import transform
from pygame.locals import *

FPS = 30
SCREENWIDTH = 289
SCREENHEIGHT = 400
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "sprites/bird.png"
BACKGROUND = "sprites/b1.png"
PIPE = "sprites/pipe.png"



def welcome_Screen(highscore):
    playerx = int(SCREENWIDTH / 8)
    playery = int((SCREENHEIGHT - GAME_SPRITES["player"].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES["home"].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    
    basex = 0
    widthx=0
    

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                GAME_SOUNDS["music1"].play()
                SCREEN.blit(GAME_SPRITES["background"], (0, 0))
                # SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES["base"], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES["home"], (messagex, messagey))
                
                mydigits=[int(x) for x in list(str(highscore))]

                for digits in mydigits:
                    widthx+=GAME_SPRITES['numbers'][digits].get_width()
                xoffset=230

                for digit in mydigits:
                    SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,363))
                    xoffset+=GAME_SPRITES['numbers'][digit].get_width()
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def game_over():
    overx=(SCREENWIDTH-GAME_SPRITES['gameover'].get_width())/2
    overy = int(SCREENHEIGHT * 0.13)
    while True:
        SCREEN.blit(GAME_SPRITES['gameover'],(overx,overy))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

def getRandomPipe():
    pipeHeight = GAME_SPRITES["pipe"][0].get_height()
    offset = SCREENHEIGHT / 4
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 2*offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {"x": pipex, "y": -y1},
     {"x": pipex, "y": y2}]
    return pipe

def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def find_high_score(score,highscore):
    highscore=max(highscore,score)
    return highscore

def main_game():
    score=0
    playerx =int( SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()


    upperpipes = [
        {"x": SCREENWIDTH + 200, "y": newpipe1[0]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newpipe2[0]["y"]},
    ]

    lowerpipes = [
        {"x": SCREENWIDTH + 200, "y": newpipe1[1]["y"]},
        {"x": SCREENWIDTH + 200 + (SCREENWIDTH / 2), "y": newpipe2[1]["y"]},
    ]

    pipevelx = -5
    playervely = 0.2
    playermaxvely = 5
    playeraccy = 0.5

    playerflapaccv = -4
    playerflapped = False
    overx=(SCREENWIDTH-GAME_SPRITES['gameover'].get_width())/2
    overy = int(SCREENHEIGHT * 0.13)

    
    while 1:
        GAME_SOUNDS["background"].play()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # GAME_SOUNDS["hit"].play()
                playervely = playerflapaccv
                playerflapped = True

        # is player collide to pipe or not
        crashtest= iscollide(playerx,playery,upperpipes,lowerpipes)
        if crashtest:
            return score

        # for updating the score
        playermidpos = playerx + GAME_SPRITES["player"].get_width()
        for pipe in upperpipes:
            pipemidpos = pipe["x"] + GAME_SPRITES["pipe"][0].get_width()
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                print(f"your score is{score}")
                GAME_SOUNDS["swoosh"].play()

        if playervely < playermaxvely and not playerflapped:
            playervely += playeraccy

        if playerflapped:
            playerflapped = False

        playerheight = GAME_SPRITES["player"].get_height()
        playery = playery + min(playervely, GROUNDY - playery - playerheight)

        # move pipes to left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe["x"] += pipevelx
            lowerpipe["x"] += pipevelx

        # add a new pipes if it is deleted
        if 0 < upperpipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # remove the pipes if it cross the screen
        if upperpipes[0]["x"] < -GAME_SPRITES["pipe"][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # lets blit our stripes
        SCREEN.blit(GAME_SPRITES["background"], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES["pipe"][0], (upperpipe["x"], upperpipe["y"]))
            SCREEN.blit(GAME_SPRITES["pipe"][1], (lowerpipe["x"], lowerpipe["y"]))
        SCREEN.blit(GAME_SPRITES["base2"], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES["player"], (playerx, playery))

        mydigits=[int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.18))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by Azeem")
    GAME_SOUNDS["swoosh"] = pygame.mixer.Sound("sounds/Swoosh.mp3")
    GAME_SPRITES["home"] = pygame.image.load("sprites/home.png").convert_alpha()
    GAME_SPRITES["numbers"] = (
        pygame.image.load("sprites/zero.png").convert_alpha(),
        pygame.image.load("sprites/one.png").convert_alpha(),
        pygame.image.load("sprites/two.png").convert_alpha(),
        pygame.image.load("sprites/three.png").convert_alpha(),
        pygame.image.load("sprites/four.png").convert_alpha(),
        pygame.image.load("sprites/five.png").convert_alpha(),
        pygame.image.load("sprites/six.png").convert_alpha(),
        pygame.image.load("sprites/seven.png").convert_alpha(),
        pygame.image.load("sprites/eight.png").convert_alpha(),
        pygame.image.load("sprites/nine.png").convert_alpha(),
    )

    GAME_SPRITES["gameover"] = pygame.image.load("sprites/gameover.png").convert_alpha()
    GAME_SPRITES["base"] = pygame.image.load("sprites/base.png").convert_alpha()
    GAME_SPRITES["base2"] = pygame.image.load("sprites/base2.jpg").convert_alpha()
    GAME_SPRITES["pipe"] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha(),
    )

    GAME_SOUNDS["hit"] = pygame.mixer.Sound("sounds/hit.mp3")
    GAME_SOUNDS["background"] = pygame.mixer.Sound("sounds/chael-sparks.mp3")
    GAME_SOUNDS["music1"] = pygame.mixer.Sound("sounds/music1.mp3")

    GAME_SPRITES["background"] = pygame.image.load(BACKGROUND)
    GAME_SPRITES["player"] = pygame.image.load(PLAYER)
    overx=(SCREENWIDTH-GAME_SPRITES['gameover'].get_width())/2
    overy = int(SCREENHEIGHT * 0.13)
    highscore=0
    while True:
        welcome_Screen(highscore)
        score=main_game()
        game_over()
        highscore=find_high_score(score,highscore)
