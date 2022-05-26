import pygame, sys, time, math
from datetime import datetime

from tetris.gamedata import flags
from tetris.screen import screen
from tetris.game import GameDig, GameSprint, GameLeaves, GameMaster
from tetris.menu import Menu, EndGameMenu, SettingsMenu
from tetris.easing import easeOutElastic
from tetris.fonts import font, fontMsg, fontValueLabel, fontValue, fontTime
from tetris.logger import logging

pygame.mixer.init()
try:

    pygame.mixer.music.load('tetris/bgm/bgm1.mp3')
    pygame.mixer.music.play(loops=-1, start=1.4)
except:
    logging.exception('sound error')

try:
    acceptSound = pygame.mixer.Sound('tetris/sfx/accept.ogg')
except:
    logging.exception('sound error')

    # hold
    # line clear
    # lock
    # land

clock = pygame.time.Clock()

## Todo align these using better pygame rect props
leftColumnCenter = 200 - 2 * 24 - 12

bg = pygame.image.load('tetris/bg-game.png').convert()
logoMain = pygame.image.load('tetris/logo-main.png').convert_alpha()
logoPygame = pygame.image.load('tetris/logo-pygame.png').convert_alpha()
logoEdition = pygame.image.load('tetris/logo-edition.png').convert_alpha()

backgrounds = [
    pygame.image.load('tetris/bg.png').convert(),
    pygame.image.load('tetris/bg1.png').convert(),
    pygame.image.load('tetris/bg2.png').convert(),
    pygame.image.load('tetris/bg3.png').convert(),
    pygame.image.load('tetris/bg4.png').convert(),
    pygame.image.load('tetris/bg5.png').convert(),
    pygame.image.load('tetris/bg6.png').convert(),
    pygame.image.load('tetris/bg7.png').convert(),
    # pygame.image.load('tetris/bg8.png').convert(),
    # pygame.image.load('tetris/bg9.png').convert(),
]

"""
Texts
"""
# TODO Convert these all to images? (bad for i18n)
WHITE = (255, 255, 255)

nextLabel = font.render('NEXT', True, WHITE)
holdLabel = font.render('HOLD', True, WHITE)

piecesLabel = fontValueLabel.render('PIECES', True, WHITE)
ppsLabel = fontValueLabel.render('PPS', True, WHITE)

timeHeight = fontTime.size('00:00.00')[1]
timeCenter = math.floor(fontTime.size('00:00.00')[0] / 2)
lineLabelCenter = math.floor(font.size('LINE')[0] / 2)
nextLabelCenter = math.floor(font.size('NEXT')[0] / 2)
holdLabelCenter = math.floor(font.size('HOLD')[0] / 2)
finesseLabelCenter = math.floor(font.size('FINESSE')[0] / 2)

# Miyoo Mini inputs
# ➢ 上键:K_UP
# ➢ 下键:K_DOWN
# ➢ 左键:K_LEFT
# ➢ 右键:K_RIGHT
# ➢ A 键:K_SPACE
# ➢ B 键:K_LCTRL
# ➢ X 键:K_LSHIFT
# ➢ Y 键:K_LALT
# ➢ L1 键:K_e
# ➢ L2 键:K_TAB
# ➢ R1 键:K_t
# ➢ R2 键:K_BACKSPACE
# ➢ START 键:K_RETURN
# ➢ SELECT 键:K_RCTRL
# ➢ MENU 键:K_ESCAPE

menu = Menu()
endGameMenu = EndGameMenu()
settingsMenu = SettingsMenu()

def checkEvents(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == game.binds['moveLeft']:
                game.keysDown |= flags['moveLeft']
            elif event.key == game.binds['moveRight']:
                game.keysDown |= flags['moveRight']
            elif event.key == game.binds['moveDown']:
                game.keysDown |= flags['moveDown']
            elif event.key == game.binds['hardDrop']:
                game.keysDown |= flags['hardDrop']
            elif event.key == game.binds['rotRight']:
                game.keysDown |= flags['rotRight']
            elif event.key == game.binds['rotLeft']:
                game.keysDown |= flags['rotLeft']
            elif event.key == game.binds['rot180']:
                game.keysDown |= flags['rot180']
            elif event.key == game.binds['holdPiece']:
                game.keysDown |= flags['holdPiece']
        if event.type == pygame.KEYUP:
            if event.key == game.binds['moveLeft'] and game.keysDown & flags['moveLeft']:
                game.keysDown ^= flags['moveLeft']
            elif event.key == game.binds['moveRight'] and game.keysDown & flags['moveRight']:
                game.keysDown ^= flags['moveRight']
            elif event.key == game.binds['moveDown'] and game.keysDown & flags['moveDown']:
                game.keysDown ^= flags['moveDown']
            elif event.key == game.binds['hardDrop'] and game.keysDown & flags['hardDrop']:
                game.keysDown ^= flags['hardDrop']
            elif event.key == game.binds['rotRight'] and game.keysDown & flags['rotRight']:
                game.keysDown ^= flags['rotRight']
            elif event.key == game.binds['rotLeft'] and game.keysDown & flags['rotLeft']:
                game.keysDown ^= flags['rotLeft']
            elif event.key == game.binds['rot180'] and game.keysDown & flags['rot180']:
                game.keysDown ^= flags['rot180']
            elif event.key == game.binds['holdPiece'] and game.keysDown & flags['holdPiece']:
                game.keysDown ^= flags['holdPiece']

def update(game):
    if (flags['holdPiece'] & game.keysDown) and not (game.lastKeys & flags['holdPiece']):
        game.piece.hold()

    if flags['rotLeft'] & game.keysDown and not (game.lastKeys & flags['rotLeft']):
        game.piece.rotate(-1)
        game.piece.finesse += 1
    elif flags['rotRight'] & game.keysDown and not (game.lastKeys & flags['rotRight']):
        game.piece.rotate(1)
        game.piece.finesse += 1

    if not game.piece.firstFrame:
        game.piece.checkShift()
    else:
        game.piece.firstFrame = False

    if flags['moveDown'] & game.keysDown:
        game.piece.shiftDown();

    if flags['hardDrop'] & game.keysDown and not game.lastKeys & flags['hardDrop']:
        game.piece.hardDrop();

    game.piece.update()

    game.lastKeys = game.keysDown

def drawGame(game):
    screen.blit(bg, (0, 0))

    # TODO Temp drawing
    game.piece.drawGhost()
    game.piece.draw()
    game.preview.draw()
    game.stack.draw()
    if game.hold.piece != None:
        game.hold.draw()

    # UI
    screen.blit(nextLabel, (500 - nextLabelCenter, 12))
    screen.blit(holdLabel, (leftColumnCenter - holdLabelCenter, 12))

    game.drawUI()

    screen.blit(piecesLabel, (200 - 24 * 4.5, 480 - 24 * 3.5))
    piecesValue = fontValue.render(str(game.pieces), True, WHITE)
    piecesValueEnd = fontValue.size(str(game.pieces))[0]
    screen.blit(piecesValue, (200 - piecesValueEnd - 12, 480 - 24 * 3.5))

    # TODO Maxout time 99:99.99
    time = (1 / 60) * game.frame
    secs = time % 60
    seconds = f'{secs:.2f}'
    minutes = math.floor(time / 60)
    timeString = ('0' if minutes < 10 else '') + str(minutes) + (':0' if secs < 10 else ':') + str(seconds)
    timeValue = fontTime.render(timeString, True, WHITE)
    screen.blit(timeValue, (leftColumnCenter - timeCenter, 480 - timeHeight))

    screen.blit(ppsLabel, (200 - 24 * 4.5, 480 - 24 * 2.5))
    pps = f'{(game.pieces / time):.3f}' if game.frame > 0 else '0.000'
    ppsValue = fontValue.render(pps, True, WHITE)
    ppsValueEnd = fontValue.size(pps)[0]
    screen.blit(ppsValue, (200 - ppsValueEnd - 12, 480 - 24 * 2.5))
    # END UI

readyText = fontMsg.render('READY', True, WHITE)
goText = fontMsg.render('GO!', True, WHITE)
# greatText = fontMsg.render('GREAT!', True, WHITE)

def runGame(game):
    readyFrame = 0
    running = True
    pygame.mixer.music.load('tetris/bgm/bgm2.mp3')
    pygame.mixer.music.play(loops=-1, start=14)
    while running:
        checkEvents(game)

        # Count Down
        if readyFrame <= 100:
            drawGame(game)
            if readyFrame < 50:
                text_rect = readyText.get_rect(center=(640/2, 480/2))
                screen.blit(readyText, text_rect)
            elif readyFrame < 100:
                text_rect = goText.get_rect(center=(640/2, 480/2))
                screen.blit(goText, text_rect)
            else:
                game.state = 'playing'
                game.piece.new(game.preview.next())
            # DAS Preload
            if game.keysDown & flags['moveLeft']:
                game.lastKeys = game.keysDown
                game.piece.shiftDelay = game.settings['DAS']
                game.piece.shiftReleased = False
                game.piece.shiftDir = -1
            elif game.keysDown & flags['moveRight']:
                game.lastKeys = game.keysDown
                game.piece.shiftDelay = game.settings['DAS']
                game.piece.shiftReleased = False
                game.piece.shiftDir = 1
            readyFrame += 1
            pygame.display.flip()
            clock.tick(60)
            continue

        if game.state == 'playing' or game.state == 'gameoveranim':
            game.frame += 1

        if game.state == 'playing':
            update(game)
            drawGame(game)

        if game.checkWin() and game.state == 'playing':
            game.state = 'gameoveranim'

        if game.state == 'gameoveranim':
            if game.grayOut >= 2:
                if game.frame % 2 == 0:
                    count = 0
                    for x in range(10):
                        if (game.stack.grid[x][game.grayOut]):
                            game.stack.grid[x][game.grayOut] = 8
                        else:
                            count +=1
                    if count == 10:
                        game.grayOut = 1
                    screen.blit(bg, (200, 0), (200, 0, 240, 480)) 
                    game.stack.draw()
                    pygame.display.flip()
                    game.grayOut -= 1
            else:
                game.state = 'menu'
                running = False

        pygame.display.flip()
        clock.tick(60)

    endMenu()

def endMenu():
    running = True

    endGameMenu.keysDown = 0
    endGameMenu.selected = 0

    # copy image to rerender it
    copy = screen.copy()

    while running:
        screen.blit(copy, (0, 0))
        endGameMenu.checkEvents()

        if endGameMenu.isKeyDown('down'):
            endGameMenu.changeSetting(1)
        elif endGameMenu.isKeyDown('up'):
            endGameMenu.changeSetting(-1)
        elif endGameMenu.checkButton('accept'):
            running = False
            break
        else:
            endGameMenu.das = 0

        endGameMenu.draw()

        # NOTE Do this in every loop
        pygame.display.flip()
        endGameMenu.lastKeys = endGameMenu.keysDown
        clock.tick(60)

def runSettings():
    settingsMenu.keysDown = 0
    settingsMenu.selected = 0
    settingsMenu.selectedControl = 0
    settingsMenu.selectedTab = 0

    while True:

        if settingsMenu.changingKey:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # wait for any key to get pressed
                    if settingsMenu.binds['cancel'] == event.key:
                        settingsMenu.changingKey = False
                        settingsMenu.draw()
                    if settingsMenu.changingKey == True:
                        settingsMenu.changeKey(event.key)
                        settingsMenu.changingKey = False

            settingsMenu.draw()
            pygame.display.flip()
            settingsMenu.lastKeys = settingsMenu.keysDown
            clock.tick(60)
            continue
        else:
            settingsMenu.checkEvents()

        if settingsMenu.selectedTab == 1 and settingsMenu.checkButton('accept'):
            settingsMenu.changingKey = True
            settingsMenu.draw()
            pygame.display.flip()
            settingsMenu.lastKeys = settingsMenu.keysDown
            clock.tick(60)
            continue

        if settingsMenu.isKeyDown('down'):
            settingsMenu.changeSetting(1)
        elif settingsMenu.isKeyDown('up'):
            settingsMenu.changeSetting(-1)
        else:
            settingsMenu.das = 0

        if settingsMenu.isKeyDown('right'):
            settingsMenu.changeValue(1)
        elif settingsMenu.isKeyDown('left'):
            settingsMenu.changeValue(-1)
        else:
            settingsMenu.dasValue = 0

        if settingsMenu.checkButton('tabRight'):
            settingsMenu.setSelectedTab(1)
        elif settingsMenu.checkButton('tabLeft'):
            settingsMenu.setSelectedTab(0)

        if settingsMenu.checkButton('cancel'):
            break

        settingsMenu.draw()

        # NOTE Do this in every loop
        pygame.display.flip()
        settingsMenu.lastKeys = settingsMenu.keysDown
        clock.tick(60)

def mainMenu():
    frame = 0
    retry = False

    while True:
        menu.checkEvents()

        if menu.isKeyDown('down'):
            menu.changeSetting(1)
        elif menu.isKeyDown('up'):
            menu.changeSetting(-1)
        elif menu.isKeyDown('left'):
            menu.changeGametype(-1)
        elif menu.isKeyDown('right'):
            menu.changeGametype(1)
        else:
            menu.das = 0

        if retry or menu.checkButton('accept'):

            try:
                acceptSound.play()
            except:
                logging.exception('sound error')
            if menu.selected % len(menu.options) == 0:
                if menu.optionGametype == 0:
                    game = GameMaster()
                    runGame(game)
                elif menu.optionGametype == 1:
                    game = GameSprint()
                    runGame(game)
                elif menu.optionGametype == 2:
                    game = GameDig()
                    runGame(game)
                elif menu.optionGametype == 3:
                    game = GameLeaves()
                    runGame(game)
            elif menu.selected % len(menu.options) == 1:
                menu.selected = 0
                menu.keysDown = 0
                runSettings()
                continue
            elif menu.selected % len(menu.options) == 2:
                sys.exit()

            if endGameMenu.selected % 2 == 0:
                retry = True
            else:
                retry = False
                menu.selected = 0

            frame = 0
            menu.keysDown = 0
            continue

        try:
            screen.blit(backgrounds[frame // 180 % len(backgrounds)], (0, 0))
            logoMainRect = logoMain.get_rect(centerx=640 / 2, top=30)
            screen.blit(logoMain, logoMainRect)

            logoPygameRect = logoPygame.get_rect(center=(640 / 2, 170))
            pygameSize = (round(logoPygameRect.width * easeOutElastic(frame / 120)), round(logoPygameRect.height * easeOutElastic(frame / 120)))
            pygameOffset = ((logoPygameRect.width - pygameSize[0]) / 2, (logoPygameRect.height - pygameSize[1]) / 2)
            logoPygameScaled = pygame.transform.smoothscale(logoPygame, pygameSize)
            screen.blit(logoPygameScaled, (logoPygameRect.left + pygameOffset[0], math.sin(5 + frame / 13) * 1.6 + logoPygameRect.top + pygameOffset[1]))

            logoEditionRect = logoEdition.get_rect(center=(640 / 2, 215))
            editionSize = (round(logoEditionRect.width * easeOutElastic(max(0, frame - 30) / 120)), round(logoEditionRect.height * easeOutElastic(max(0, frame - 30) / 120)))
            editionOffset = ((logoEditionRect.width - editionSize[0]) / 2, (logoEditionRect.height - editionSize[1]) / 2)
            logoEditionScaled = pygame.transform.smoothscale(logoEdition, editionSize)
            screen.blit(logoEditionScaled, (logoEditionRect.left + editionOffset[0], math.sin(frame / 13) * 1.6 + logoEditionRect.top + editionOffset[1]))
        except:
            logging.exception('Menu render error')


        menu.draw()

        # NOTE Do this in every loop
        pygame.display.flip()
        menu.lastKeys = menu.keysDown
        frame += 1
        clock.tick(60)

mainMenu()
