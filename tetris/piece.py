import math
from .gamedata import pieces, flags
from .draw import draw

activeCtx = None

gravValues = [0.5, 1, 22]

class Piece:
    def __init__(self, game):
        self.x = 0
        self.y = 0
        self.pos = 0
        self.tetro = 0
        self.index = 0
        self.kickData = 0
        self.lockDelay = 0
        self.shiftDelay = 0
        self.shiftDir = 0
        self.shiftReleased = False
        self.arrDelay = 0
        self.held = False
        self.finesse = 0
        self.dirty = False
        self.landed = False
        self.game = game
        self.firstFrame = True

    def new(self, index):
        # TODO if no arguments, get next grabbag piece
        self.pos = 0
        self.tetro = []
        self.held = False
        self.finesse = 0
        self.dirty = True
        self.landed = False
        self.lockDelay = 0
        self.firstFrame = True

        self.tetro = pieces[index]['tetro'];
        self.kickData = pieces[index]['kickData'];
        self.x = pieces[index]['x'];
        self.y = pieces[index]['y'];
        self.index = index;
        if not self.moveValid(0, 0, self.tetro):
            self.game.state = 'gameoveranim'

    def rotate(self, direction):
        rotated = len(self.tetro) * [0];
        if (direction == -1):
            for i in range(len(self.tetro) - 1, -1, -1):
                rotated[i] = len(self.tetro) * [0]
                for row in range(len(self.tetro)):
                    rotated[i][len(self.tetro) - 1 - row] = self.tetro[row][i]
        else:
            for i in range(len(self.tetro)):
                rotated[i] = len(self.tetro) * [0]
                for row in range(len(self.tetro) - 1, -1, -1):
                    rotated[i][row] = self.tetro[row][len(self.tetro) - 1 - i]

        # Goes thorugh kick data until it finds a valid move.
        curPos = self.pos % 4
        newPos = (self.pos + direction) % 4

        for x in range(len(self.kickData[0])):
            if self.moveValid(
                    self.kickData[curPos][x][0] - self.kickData[newPos][x][0],
                    self.kickData[curPos][x][1] - self.kickData[newPos][x][1],
                    rotated,
                    ):
                self.x += self.kickData[curPos][x][0] - self.kickData[newPos][x][0];
                self.y += self.kickData[curPos][x][1] - self.kickData[newPos][x][1];
                self.tetro = rotated;
                self.pos = newPos;
                break;

    def checkShift(self):
        # Handle key pressed
        if self.game.keysDown & flags['moveLeft'] and not (self.game.lastKeys & flags['moveLeft']):
            self.shiftDelay = 0
            self.arrDelay = 0
            self.shiftReleased = True
            self.shiftDir = -1
            self.finesse += 1
        elif self.game.keysDown & flags['moveRight'] and not (self.game.lastKeys & flags['moveRight']):
            self.shiftDelay = 0
            self.arrDelay = 0
            self.shiftReleased = True
            self.shiftDir = 1
            self.finesse += 1

        # Handle released key
        if self.shiftDir == 1 and not (self.game.keysDown & flags['moveRight']) and self.game.lastKeys & flags['moveRight'] and self.game.keysDown & flags['moveLeft']:
            self.shiftDelay = 0
            self.arrDelay = 0
            self.shiftReleased = True
            self.shiftDir = -1
        elif self.shiftDir == -1 and not (self.game.keysDown & flags['moveLeft']) and self.game.lastKeys & flags['moveLeft'] and self.game.keysDown & flags['moveRight']:
            self.shiftDelay = 0;
            self.arrDelay = 0;
            self.shiftReleased = True;
            self.shiftDir = 1;
        elif not (self.game.keysDown & flags['moveRight']) and self.game.lastKeys & flags['moveRight'] and self.game.keysDown & flags['moveLeft']:
            self.shiftDir = -1;
        elif not (self.game.keysDown & flags['moveLeft']) and self.game.lastKeys & flags['moveLeft'] and self.game.keysDown & flags['moveRight']:
            self.shiftDir = 1;
        elif (not (self.game.keysDown & flags['moveLeft']) and self.game.lastKeys & flags['moveLeft']) or (not (self.game.keysDown & flags['moveRight']) and self.game.lastKeys & flags['moveRight']):
            self.shiftDelay = 0;
            self.arrDelay = 0;
            self.shiftReleased = True;
            self.shiftDir = 0;

        # Handle events
        if self.shiftDir:
            # 1. When key pressed instantly move over once.
            if self.shiftReleased:
                self.shift(self.shiftDir)
                self.shiftDelay += 1
                self.shiftReleased = False
            # 2. Apply DAS delay
            elif self.shiftDelay < self.game.settings['DAS']:
                self.shiftDelay += 1
            # 3. Once the delay is complete, move over once.
            #     Increment delay so self doesn't run again.
            elif self.shiftDelay == self.game.settings['DAS'] and self.game.settings['DAS'] != 0:
                self.shift(self.shiftDir)
                if self.game.settings['ARR'] != 0:
                    self.shiftDelay += 1
            # 4. Apply ARR delay
            elif self.arrDelay < self.game.settings['ARR']:
                self.arrDelay += 1
            # 5. If ARR Delay is full, move piece, and reset delay and repeat.
            elif self.arrDelay == self.game.settings['ARR'] and self.game.settings['ARR'] != 0:
                self.shift(self.shiftDir)

    # TODO update from published game
    def shift(self, direction):
        self.arrDelay = 0
        if self.game.settings['ARR'] == 0 and self.shiftDelay == self.game.settings['DAS']:
            for i in range(1, 10):
                if not self.moveValid(i * direction, 0, self.tetro):
                    self.x += i * direction - direction
                    break
                else:
                    grav = self.game.gravity
                    if grav >= 1:
                        if self.moveValid(i * direction, 1, self.tetro):
                            self.y += self.getDrop(grav, i * direction + self.x)

        elif self.moveValid(direction, 0, self.tetro):
            self.x += direction

    def shiftDown(self):
        if self.moveValid(0, 1, self.tetro):
            grav = gravValues[self.game.settings['Soft Drop']]
            if (grav > 1):
                self.y += self.getDrop(grav)
            else:
                self.y += grav


    def hardDrop(self):
        self.y += self.getDrop(22)
        self.lockDelay = self.game.lockDelay

    def getDrop(self, distance, overridex = None):
        for i in range(distance):
            if not self.moveValid(0, i, self.tetro, overridex):
                # return i - 1
                break
        return i - 1;

    def hold(self):
        temp = self.game.hold.piece
        if not self.held:
            if self.game.hold.piece != None:
                self.game.hold.piece = self.index
                self.new(temp)
            else:
                self.game.hold.piece = self.index
                self.new(self.game.preview.next())

            self.held = True
            self.game.hold.draw()

    """
    Checks if position and orientation passed is valid.
    We call it for every action instead of only once a frame in case one
    of the actions is still valid, we don't want to block it.
    """
    def moveValid(self, cx, cy, tetro, overridex = None):
        if overridex != None:
            cx = cx + overridex
        else:
            cx = cx + self.x
        cy = math.floor(cy + self.y)

        for x in range(len(tetro)):
            for y in range(len(tetro[x])):
                if tetro[x][y] and (cx + x < 0 or cx + x >= 10 or cy + y >= 22 or self.game.stack.grid[cx + x][cy + y]):
                    return False
        self.lockDelay = 0;
        return True

    def update(self):
        if self.moveValid(0, 1, self.tetro):
            self.landed = False
            grav = self.game.gravity
            if grav > 1:
                self.y += self.getDrop(grav)
            else:
                self.y += grav
        else:
            self.landed = True
            self.y = math.floor(self.y)
            if self.lockDelay >= self.game.lockDelay:
                self.game.stack.addPiece(self)
                self.new(self.game.preview.next())
            else:
                a = 1 / self.game.lockDelay
                # Fade out I think
                # TODO activeCtx.globalCompositeOperation = 'source-atop'
                # TODO activeCtx.fillStyle = 'rgba(0,0,0,' + a + ')'
                # TODO activeCtx.fillRect(0, 0, activeCanvas.width, activeCanvas.height)
                # TODO activeCtx.globalCompositeOperation = 'source-over'
                self.lockDelay += 1;

    def draw(self):
        if self.tetro:
            draw(self.tetro, self.x, self.y, activeCtx, None, (200, 0))

    def drawGhost(self):
        if self.tetro:
            if self.game.settings['Ghost'] == 0 and not self.landed:
                draw(self.tetro, self.x, self.y + self.getDrop(22), activeCtx, 0, (200, 0))
            elif self.game.settings['Ghost'] == 1 and not self.landed:
                draw(self.tetro, self.x, self.y + self.getDrop(22), activeCtx, None, (200, 0), 255 * 0.3)
