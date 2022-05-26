import pygame
import random
from tetris.screen import screen
from tetris.stack import Stack
from tetris.hold import Hold
from tetris.piece import Piece
from tetris.preview import Preview
from tetris.settings import load_save
from tetris.fonts import font, fontBig

leftColumnCenter = 200 - 2 * 24 - 12
WHITE = (255, 255, 255)
lineLabel = font.render('LINE', True, WHITE)
finesseLabel = font.render('FINESSE', True, WHITE)

class Game:
    def __init__(self):
        self.frame = 0
        self.grayOut = 21
        self.keysDown = 0
        self.lastKeys = 0
        self.released = 255
        self.finesse = 0
        self.pieces = 0
        self.lines = 0
        self.state = 'inactive'
        self.lockDelay = 50
        self.gravity = 0
        ## TODO make piece and others a field

        self.piece = Piece(self)
        self.stack = Stack(self)
        self.preview = Preview()
        self.hold = Hold()

        save = load_save()
        self.settings = save['settings']
        self.binds = save['controls']

    def clearLine(self, row):
        self.lines += 1

    def checkWin(self):
        return False

    def drawUI(self):
        return True

class GameMaster(Game):
    def __init__(self):
        super().__init__()
        self.lockDelay = 50
        self.gravity = 22
        levelLabel = font.render('Level', True, WHITE)

    def checkWin(self):
        return False

    def drawUI(self):
        lines = str(40 - self.lines)
        lineText = fontBig.render(lines, True, WHITE)
        lineRect = lineText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 11 - 8)
        lineLabelRect = lineLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 8.5)
        screen.blit(lineText, lineRect)
        screen.blit(lineLabel, lineLabelRect)

        finesseText = fontBig.render(str(self.finesse), True, WHITE)
        finesseRect = finesseText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 7.5 - 8)
        finesseLabelRect = finesseLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 5)
        screen.blit(finesseText, finesseRect)
        screen.blit(finesseLabel, finesseLabelRect)

class GameSprint(Game):
    def checkWin(self):
        if 40 - self.lines <= 0:
            return True

    def drawUI(self):
        lines = str(40 - self.lines)
        lineText = fontBig.render(lines, True, WHITE)
        lineRect = lineText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 11 - 8)
        lineLabelRect = lineLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 8.5)
        screen.blit(lineText, lineRect)
        screen.blit(lineLabel, lineLabelRect)

        finesseText = fontBig.render(str(self.finesse), True, WHITE)
        finesseRect = finesseText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 7.5 - 8)
        finesseLabelRect = finesseLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 5)
        screen.blit(finesseText, finesseRect)
        screen.blit(finesseLabel, finesseLabelRect)

class GameDig(Game):
    def __init__(self):
        super().__init__()
        self.digLines = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21];
        holes = []
        i = 0
        while i < 10:
            # hole = math.floor(rng.next() * 10)
            hole = random.randint(0, 9)
            if i == 0 or hole != holes[i - 1]:
                holes.append(hole)
                i += 1

        for y in self.digLines:
            for x in range(10):
                if holes[y - 12] != x:
                    self.stack.grid[x][y] = 8

    def checkWin(self):
        if len(self.digLines) == 0:
            return True

    def drawUI(self):
        # TODO Compute center and draw to centered
        lines = str(len(self.digLines))
        lineText = fontBig.render(lines, True, WHITE)
        lineRect = lineText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 11 - 8)
        lineLabelRect = lineLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 8.5)
        screen.blit(lineText, lineRect)
        screen.blit(lineLabel, lineLabelRect)

    def clearLine(self, row):
        super().clearLine(row)
        try:
            self.digLines.remove(row)
        except ValueError:
            pass

class GameLeaves(Game):
    def __init__(self):
        super().__init__()
        self.stack = Stack(self, 5, 12)

    def checkWin(self):
        # TODO timer
        return False

    def drawUI(self):
        # lines = str(len(self.digLines))
        # lineText = fontBig.render(lines, True, WHITE)
        # lineRect = lineText.get_rect(centerx=leftColumnCenter, top=480 - 24 * 11 - 8)
        # lineLabelRect = lineLabel.get_rect(centerx=leftColumnCenter, top=480 - 24 * 8.5)
        # screen.blit(lineText, lineRect)
        # screen.blit(lineLabel, lineLabelRect)
        pass

    def clearLine(self, row):
        super().clearLine(row)
        # TODO Check if pc

