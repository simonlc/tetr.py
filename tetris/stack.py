import pygame
import math
from .screen import screen
from .draw import draw
from .gamedata import finesse

stackCtx = None

cellSize = math.floor(480 / 20)

tl = pygame.image.load('tetris/gfx/tl.png').convert()
bl = pygame.image.load('tetris/gfx/bl.png').convert()
tr = pygame.image.load('tetris/gfx/tr.png').convert()
br = pygame.image.load('tetris/gfx/br.png').convert()

class Stack:
    def __init__(self, game, x = 10, y = 22):
        self.game = game
        self.new(x, y)

    """
    Creates a matrix for the playfield.
    """
    def new(self, x = 10, y = 22):
        cells = x * [0]
        for i in range(x):
            cells[i] = y * [0]
        self.grid = cells;

    """
    Adds tetro to the stack, and clears lines if they fill up.
    """
    def addPiece(self, piece):
        once = False
        column = None

        # Add the piece to the stack.
        pieceRange = [];
        valid = False;
        for x in range(len(piece.tetro)):
            for y in range(len(piece.tetro[x])):
                if piece.tetro[x][y]:
                    self.grid[x + piece.x][y + piece.y] = piece.tetro[x][y]
                    # Get column for finesse
                    if not once or x + piece.x < column:
                        column = x + piece.x
                        once = True

                    # Check which lines get modified
                    if y + piece.y not in pieceRange:
                        pieceRange.append(y + piece.y);
                        # This checks if any cell is in the play field. If there
                        # isn't any this is called a lock out and the game ends.
                        if y + piece.y > 1:
                            valid = True

        # Lock out
        if not valid:
            self.game.state = 'gameoveranim';
            # msg.innerHTML = 'LOCK OUT!';
            return

        # Check modified lines for full lines.
        # TODO non mutable way?
        pieceRange.sort()
        for row in range(pieceRange[0], pieceRange[0] + len(pieceRange)):
            count = 0
            for x in range(10):
                if self.grid[x][row]:
                    count += 1
            # Clear the line. This basically just moves down the stack.
            if count == 10:
                self.game.clearLine(row)
                for y in range(row, -1, -1):
                    for x in range(10):
                        self.grid[x][y] = self.grid[x][y - 1] if y > 0 else 0;

        self.game.finesse += piece.finesse - finesse[piece.index][piece.pos][column];
        self.game.pieces += 1

        self.draw()

    """
    Draws the stack.
    """
    def draw(self):
        draw(self.grid, 0, 0, stackCtx, None, (200, 0));

        s = pygame.Surface((cellSize * 10, cellSize * 20))

        if self.game.settings['Outline']:
            b = math.floor(cellSize / 8)
            c = cellSize
            color = (255,255,255)

            for x in range(len(self.grid)):
                for y in range(len(self.grid[x])):
                    if self.grid[x][y]:
                        if x < 9 and not self.grid[x + 1][y]:
                            pygame.draw.rect(s, color, (x * c + c - b, y * c - 2 * c, b, c))
                        if x > 0 and not self.grid[x - 1][y]:
                            pygame.draw.rect(s, color, (x * c, y * c - 2 * c, b, c))
                        if y < 21 and not self.grid[x][y + 1]:
                            pygame.draw.rect(s, color, (x * c, y * c - 2 * c + c - b, c, b))
                        if not self.grid[x][y - 1]:
                            pygame.draw.rect(s, color, (x * c, y * c - 2 * c, c, b))
                        # Diags
                        if x < 9 and y < 21:
                            if not self.grid[x + 1][y + 1] and self.grid[x + 1][y] and self.grid[x][y + 1]:
                                s.blit(br, (x * c + c - b, y * c - 2 * c + c - b))
                        if x < 9:
                            if not self.grid[x + 1][y - 1] and self.grid[x + 1][y] and self.grid[x][y - 1]:
                                s.blit(tr, (x * c + c - b, y * c - 2 * c))
                        if x > 0 and y < 21:
                            if not self.grid[x - 1][y + 1] and self.grid[x - 1][y] and self.grid[x][y + 1]:
                                s.blit(bl, (x * c, y * c - 2 * c + c - b))
                        if x > 0:
                            if not self.grid[x - 1][y - 1] and self.grid[x - 1][y] and self.grid[x][y - 1]:
                                s.blit(tl, (x * c, y * c - 2 * c))

            s_rect = s.get_rect(center=(640/2, 480/2))
            s.set_alpha(180)
            screen.blit(s, s_rect)
