import random
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

fps = 40
screenwidth = 289
screenheight = 511
screen = pygame.display.set_mode((screenwidth, screenheight))  # initialize the screen for game
ground = screenheight
game_sprites = {}
game_sound = {}
player = 'bird2.png'
background = 'background.jpg'
pipe = 'pipe2.png'

def welcomescreen():
    playerx = int(screenwidth / 5)
    playery = int((screenheight - game_sprites['player'].get_height()) / 2)
    messagex = int((screenwidth - game_sprites['message'].get_width()) / 2)
    messagey = int(screenheight * 0.13)
    while True:
        for event in pygame.event.get():
            # if user clicks on the cross button close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_sprites['background'], (0, 0))
                screen.blit(game_sprites['player'], (playerx + 30, playery))
                screen.blit(game_sprites['message'], (messagex, messagey + 70))
                pygame.display.update()
                fpsclock.tick(fps)

def isCollide(playery, playerx, upperPipes, lowerPipes):
    if playery > ground - 120 or playery < 0:
        game_sound['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = game_sprites['pipe'][0].get_height() - 50
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width() -50):
            game_sound['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playery + game_sprites['player'].get_height() -20 > pipe['y']  and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width() - 50):
            game_sound['hit'].play()
            return True
    return False


def mainGame():
    score = 0
    playerx = int(screenwidth / 5)
    playery = int(screenheight / 2)
    # create 2 pipes for blitting on the screen
    newpipe1 = getrandompipe()
    newpipe2 = getrandompipe()

    upperpipe = [
        {"x": screenwidth + 150, 'y': newpipe1[0]['y']},
        {"x": screenwidth + 150 + (screenwidth / 1.2), 'y': newpipe2[0]['y']}
    ]
    lowerpipe = [
        {"x": screenwidth + 150, 'y': newpipe1[1]['y']},
        {"x": screenwidth + 150 + (screenwidth / 1.2), 'y': newpipe2[1]['y']}
    ]

    pipevelx = -4

    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playeraccy = 1

    playerflap = -8  # velocity while flapping
    playerflapped = False  # It is true only when the bird is flapping

    bgx = 0
    bgvelx = -2
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely = playerflap
                    playerflapped = True
                    game_sound['wing'].play()

        crashtest = isCollide(playery, playerx, upperpipe, lowerpipe)

        if crashtest:
            return
        playerMidPos = playerx + game_sprites['player'].get_width() / 2
        for pipe in upperpipe:
            pipeMidPos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f'Your score is {score}')
                game_sound['point'].play()

        if playervely < playermaxvely and not playerflapped:
            playervely += playeraccy

        if playerflapped:
            playerflapped = False
        playerHeight = game_sprites['player'].get_height()
        playery = playery + min(playervely, ground - playery - playerHeight)

        for upperpipes, lowerpipes in zip(upperpipe, lowerpipe):
            upperpipes['x'] += pipevelx
            lowerpipes['x'] += pipevelx

        if 0 < upperpipe[0]['x'] < 5:
            newpipe = getrandompipe()
            upperpipe.append(newpipe[0])
            lowerpipe.append(newpipe[1])
        # if the pipe is out of the screen remove it
        if upperpipe[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperpipe.pop(0)
            lowerpipe.pop(0)
        bgx += bgvelx
        if bgx <= -game_sprites['background'].get_width() + screenwidth:
            bgx = 0
        screen.blit(game_sprites['background'], (bgx, 0))
        for upperpipes, lowerpipes in zip(upperpipe, lowerpipe):
            screen.blit(game_sprites['pipe'][0], (upperpipes['x'], upperpipes['y']))
            screen.blit(game_sprites['pipe'][1], (lowerpipes['x'], lowerpipes['y']))

        screen.blit(game_sprites['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_sprites['numbers'][digit].get_width()
        Xoffset = (screenwidth - width) / 2

        for digit in myDigits:
            screen.blit(game_sprites['numbers'][digit], (Xoffset, screenheight * 0.12))
            Xoffset += game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        fpsclock.tick(fps)

def getrandompipe():
    pipeheight = game_sprites['pipe'][0].get_height()
    offset = screenheight / 5
    y2 = offset + random.randint(0, int(screenheight - 1.2 * offset)) - 50
    pipex = screenwidth + 200
    y1 = pipeheight - y2 + offset + 50
    return [
        {'x': pipex, 'y': -y2},  # upper pipe
        {'x': pipex, 'y': y1}   # lower pipe
    ]

if __name__ == "__main__":
    pygame.init()  # Initialize all pygame module
    fpsclock = pygame.time.Clock()  # for fps
    pygame.display.set_caption("Flappy Bird by Saurav Subedi")
    game_sprites['numbers'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('/5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha(),
    )

    game_sprites['message'] = pygame.image.load('message.png').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )

    game_sound['die'] = pygame.mixer.Sound('losing.wav')
    game_sound['hit'] = pygame.mixer.Sound('boxer.wav')
    game_sound['point'] = pygame.mixer.Sound('point.wav')
    game_sound['swoosh'] = pygame.mixer.Sound('swoosh.mp3')
    game_sound['wing'] = pygame.mixer.Sound('wings.mp3')
    game_sound['intro'] = pygame.mixer.Sound('intro.wav')

    game_sprites['background'] = pygame.image.load(background).convert_alpha()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sound['intro'].play()

    while True:
        welcomescreen()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function
