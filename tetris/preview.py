from random import randint, random
from math import floor
from .gamedata import pieces
from .draw import draw

previewCtx = 0

def clear(ctx):
    return

# TODO Use seed
def shuffle(bag):
    length = len(bag)
    while length > 1:
        i = int(floor(random() * length))
        length -= 1
        bag[i], bag[length] = bag[length], bag[i]
    return bag

class Preview:
    def __init__(self):
        self.grabBag = self.gen()
        while 1:
            self.grabBag = self.gen()
            if self.grabBag[0] not in [3, 4, 6]:
                break;

        self.grabBag.extend(self.gen())
        self.draw()

    def next(self):
        next = None
        next = self.grabBag.pop(0)
        if len(self.grabBag) == 7:
            self.grabBag.extend(self.gen())
        self.draw()
        return next

    """
    Shuffle new 7-bag
    """
    def gen(self):
        pieceList = [0, 1, 2, 3, 4, 5, 6]
        return shuffle(pieceList)

    def draw(self):
        clear(previewCtx)
        for i in range(6):
            if self.grabBag[i] == 0 or self.grabBag[i] == 3:
                draw(
                    pieces[self.grabBag[i]]['tetro'],
                    pieces[self.grabBag[i]]['x'] - 3,
                    pieces[self.grabBag[i]]['y'] + 2 + i * 3,
                    previewCtx,
                    None,
                    (452, 48)
                )
            else:
                draw(
                    pieces[self.grabBag[i]]['tetro'],
                    pieces[self.grabBag[i]]['x'] - 2.5,
                    pieces[self.grabBag[i]]['y'] + 2 + i * 3,
                    previewCtx,
                    None,
                    (452, 48)
                )
