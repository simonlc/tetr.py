from .gamedata import pieces
from .draw import draw

class Hold:
    def __init__(self):
        self.piece = None

    def draw(self):
        if self.piece == 0 or self.piece == 3:
            draw(
                pieces[self.piece]['tetro'],
                pieces[self.piece]['x'] - 3,
                2 + pieces[self.piece]['y'],
                None,
                None,
                (200 - 12 - 24 * 4, 48),
            )
        else:
            draw(
                pieces[self.piece]['tetro'],
                pieces[self.piece]['x'] - 2.5,
                2 + pieces[self.piece]['y'],
                None,
                None,
                (92, 48),
            )
