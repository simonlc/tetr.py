import pygame
from tetris.screen import screen
from tetris.fonts import fontValue
from tetris.logger import logging
from tetris.settings import load_save, write_save, create_save
from tetris.logger import logging

WHITE = (255, 255, 255)

bg1 = pygame.image.load('tetris/bg4.png').convert()
bg2 = pygame.image.load('tetris/bg2.png').convert()
pygame.mixer.init()
try:
    menuChangeSound = pygame.mixer.Sound('tetris/sfx/menu-change.ogg')
except:
    logging.exception('sound error')

class Menu:
    keysDown = 0
    lastKeys = 0
    released = 255
    das = 0
    arr = 0
    flags = {
        'left': 1,
        'right': 2,
        'up': 4,
        'down': 8,
        'accept': 16,
        'cancel': 32,
        'tabLeft': 64,
        'tabRight': 128,
    }
    binds = {
        'left': pygame.K_LEFT,
        'right': pygame.K_RIGHT,
        'up': pygame.K_UP,
        'down': pygame.K_DOWN,
        'accept': pygame.K_RETURN,
        'cancel': pygame.K_ESCAPE,
        'tabLeft': [pygame.K_TAB, pygame.K_e],
        'tabRight': [pygame.K_BACKSPACE, pygame.K_t],
    }

    def __init__(self):
        self.selected = 0
        self.optionGametype = 0
        self.options = [
            ['Play Master', 'Play Sprint', 'Play Dig Race', 'Play Leaves'],
            'Settings',
            'Quit',
        ]

    def changeGametype(self, by):
        if self.das == 0 or self.das >= 13:
            if self.das == 0 or (self.das >= 13 and self.arr >= 3):
                self.optionGametype = (self.optionGametype + by) % len(self.options[0])
                if self.arr == 3:
                    self.arr = 0
                try:
                    menuChangeSound.play()
                except:
                    logging.exception('sound error')
            else:
                self.arr = self.arr + 1
            if self.das == 0:
                self.das = self.das + 1
        else:
            self.das = self.das + 1

    def changeSetting(self, by):
        if self.das == 0 or self.das >= 13:
            if self.das == 0 or (self.das >= 13 and self.arr >= 3):
                self.selected = (self.selected + by) % len(self.options)
                if self.arr == 3:
                    self.arr = 0
                try:
                    menuChangeSound.play()
                except:
                    logging.exception('sound error')
            else:
                self.arr = self.arr + 1
            if self.das == 0:
                self.das = self.das + 1
        else:
            self.das = self.das + 1

    def keyDown(self, key, testKey):
        if type(self.binds[testKey]) is list:
            if key in self.binds[testKey]:
                self.keysDown |= self.flags[testKey]
        else:
            if key == self.binds[testKey]:
                self.keysDown |= self.flags[testKey]

    def keyUp(self, key, testKey):
        if type(self.binds[testKey]) is list:
            if key in self.binds[testKey] and self.keysDown & self.flags[testKey]:
                self.keysDown ^= self.flags[testKey]
        else:
            if key == self.binds[testKey] and self.keysDown & self.flags[testKey]:
                self.keysDown ^= self.flags[testKey]

    def isKeyDown(self, button):
        return self.flags[button] & self.keysDown

    def checkButton(self, button):
        return (self.flags[button] & self.keysDown) and not (self.lastKeys & self.flags[button])

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keyDown(event.key, 'left')
                self.keyDown(event.key, 'right')
                self.keyDown(event.key, 'up')
                self.keyDown(event.key, 'down')
                self.keyDown(event.key, 'accept')
                self.keyDown(event.key, 'cancel')
                self.keyDown(event.key, 'tabLeft')
                self.keyDown(event.key, 'tabRight')

            if event.type == pygame.KEYUP:
                self.keyUp(event.key, 'left')
                self.keyUp(event.key, 'right')
                self.keyUp(event.key, 'up')
                self.keyUp(event.key, 'down')
                self.keyUp(event.key, 'accept')
                self.keyUp(event.key, 'cancel')
                self.keyUp(event.key, 'tabLeft')
                self.keyUp(event.key, 'tabRight')

    def drawOption(self, optionText, top, selected, offsetx=0):
        try:
            color = WHITE if not selected else (29, 161, 242)
            # Text
            value = fontValue.render(optionText, True, color)
            value_rect = value.get_rect(centerx=640/2 + offsetx, top=top)

            # Box
            # TODO Replace with image
            borderRect = pygame.Rect((0, 0, 6 * 24, 24 * 1.5))
            bgRect = pygame.Rect((2, 2, 6 * 24 - 4, 24 * 1.5 - 4))

            s = pygame.Surface(borderRect.size)
            s.set_alpha(128)
            buttonRect = s.get_rect(center=value_rect.center)

            # Compose
            pygame.draw.rect(s, color, borderRect)
            pygame.draw.rect(s, (0,0,0), bgRect)
            screen.blit(s, buttonRect)
            screen.blit(value, value_rect)
        except:
            logging.exception('drawOption error')

    def draw(self):
        offsetTop = 480 - 200
        for x in range(len(self.options)):
            top = (36 + 12) * x + offsetTop
            if type(self.options[x]) is list:
                for y in range(len(self.options[x])):
                    self.drawOption(self.options[x][y], top, self.optionGametype == y and (self.selected % len(self.options)) == x, offsetx = (y - self.optionGametype) * 150 )
            else:
                self.drawOption(self.options[x], top, (self.selected % len(self.options)) == x)

class EndGameMenu(Menu):
    def __init__(self):
        super().__init__()
        self.options = [
            'Retry',
            'Main Menu',
        ]

class SettingsMenu(Menu):
    def __init__(self):
        super().__init__()

        save = load_save()
        self.settings = save['settings']
        self.controls = save['controls']

        self.selectedControl = 0
        self.selectedTab = 0
        self.changingKey = False
        self.options = [
            {
                'title': 'DAS',
                'options': list(range(30)),
                'description': 'How fast before auto repeat kicks in.',
            },
            {
                'title': 'ARR',
                'options': list(range(10)),
                'description': 'Length between auto repeat ticks.',
            },
            # 1/2G, 1G, 22G
            {
                'title': 'Soft Drop',
                'options': ['Slow', 'Fast', 'Instant'],
                'description': 'How fast a piece falls when down is pressed.',
            },
            {
                'title': 'Sound',
                'options': list(range(101)),
                'description': 'Sound effect volume.',
            },
            {
                'title': 'Music',
                'options': list(range(101)),
                'description': 'Music volume.',
            },
            # TODO Load skins from directory
            {
                'title': 'Block Skin',
                'options': ['Shaded', 'Solid', 'World'],
                'description': 'How the minos look in game.',
            },
            {
                'title': 'Ghost',
                'options': ['Gray', 'Transparent', 'Off'],
                'description': 'How the ghost piece looks in game.',
            },
            {
                'title': 'Outline',
                'options': ['Off', 'On'],
                'description': 'Turn the stack outline on or off.',
            },
        ]
        self.controlOptions = [
            {
                'title': 'Move Left',
                'value': 'moveLeft',
            },
            {
                'title': 'Move Right',
                'value': 'moveRight',
            },
            {
                'title': 'Move Down',
                'value': 'moveDown',
            },
            {
                'title': 'Hard Drop',
                'value': 'hardDrop',
            },
            {
                'title': 'Hold',
                'value': 'holdPiece',
            },
            {
                'title': 'Spin Right',
                'value': 'rotRight',
            },
            {
                'title': 'Spin Left',
                'value': 'rotLeft',
            },
            {
                'title': 'Spin 180',
                'value': 'rot180',
            },
            {
                'title': 'Retry',
                'value': 'menu',
            },
            {
                'title': 'Pause',
                'value': 'pause',
            },
        ]

    def setSelectedTab(self, tabIndex):
        if tabIndex != self.selectedTab:
            self.selectedTab = tabIndex
            self.selectedControl = 0
            self.selected = 0
            try:
                menuChangeSound.play()
            except:
                logging.exception('sound error')

    def changeSetting(self, by):
        if self.das == 0 or self.das >= 13:
            if self.das == 0 or (self.das >= 13 and self.arr >= 3):
                if self.selectedTab == 0:
                    self.selected = (self.selected + by) % len(self.options)
                elif self.selectedTab == 1:
                    self.selectedControl = (self.selectedControl + by) % len(self.controlOptions)

                if self.arr == 3:
                    self.arr = 0

                try:
                    menuChangeSound.play()
                except:
                    logging.exception('sound error')

            else:
                self.arr = self.arr + 1
            if self.das == 0:
                self.das = self.das + 1
        else:
            self.das = self.das + 1

    def changeValue(self, by):
        option = self.options[self.selected]['title']
        arrLimit = 1 if option in ['Sound', 'Music'] else 3
        if self.dasValue == 0 or self.dasValue >= 13:
            if self.dasValue == 0 or (self.dasValue >= 13 and self.arr >= arrLimit):
                optionLength = len(self.options[self.selected]['options'])
                self.settings[option] = (self.settings[option] + by) % optionLength
                write_save({
                    'controls': self.controls,
                    'settings': self.settings,
                })
                if self.arr == arrLimit:
                    self.arr = 0
                try:
                    menuChangeSound.play()
                except:
                    logging.exception('sound error')
            else:
                self.arr = self.arr + 1
            if self.dasValue == 0:
                self.dasValue = 1
        else:
            self.dasValue = self.dasValue + 1

    def changeKey(self, key):
        controlValue = self.controlOptions[self.selectedControl]['value']
        self.controls[controlValue] = key
        write_save({
            'controls': self.controls,
            'settings': self.settings,
        })

    def drawOption(self, optionText, pos, selected):
        color = WHITE if not selected else (29, 161, 242)
        # Text
        value = fontValue.render(optionText, True, color)
        value_rect = value.get_rect(top=pos[0], left=20 + pos[1])

        screen.blit(value, value_rect)

    def drawTabs(self):
        selectedColor = (29, 161, 242)

        top = 15
        settings = fontValue.render('Settings', True, selectedColor if self.selectedTab == 0 else WHITE)
        settings_rect = settings.get_rect(top=top, left=15)

        controls = fontValue.render('Controls', True, selectedColor if self.selectedTab == 1 else WHITE)
        controls_rect = controls.get_rect(top=top, left=settings_rect.width + 40)

        screen.blit(settings, settings_rect)
        screen.blit(controls, controls_rect)

    def draw(self):
        screen.blit(bg1 if self.selectedTab == 0 else bg2, (0, 0))
        offsetTop = 65

        tabsS = pygame.Surface((190, 26), pygame.SRCALPHA)
        tabsS.fill((0,0,0,180))
        screen.blit(tabsS, (8, 15))

        settingsS = pygame.Surface((300, 210 if self.selectedTab == 0 else 260), pygame.SRCALPHA)
        settingsS.fill((0,0,0,180))
        screen.blit(settingsS, (8, 60))

        if self.selectedTab == 0:
            for x in range(len(self.options)):
                top = 25 * x + offsetTop
                settingValue = self.settings[self.options[x]['title']]
                self.drawOption(self.options[x]['title'], (top, 0), (self.selected % len(self.options)) == x)
                self.drawOption(str(self.options[x]['options'][settingValue]), (top, 150), (self.selected % len(self.options)) == x)

            value = fontValue.render(self.options[self.selected % len(self.options)]['description'], True, WHITE)
            value_rect = value.get_rect(right=640 - 30, bottom=480 - 30)

            descriptionS = pygame.Surface((value_rect.width + 15, 26), pygame.SRCALPHA)
            descriptionS.fill((0,0,0,180))
            descriptionS_rect = descriptionS.get_rect(center=value_rect.center)
            screen.blit(descriptionS, descriptionS_rect)


            screen.blit(value, value_rect)
        elif self.selectedTab == 1:
            for x in range(len(self.controlOptions)):
                top = 25 * x + offsetTop
                controlValue = self.controlOptions[x]['value']
                self.drawOption(self.controlOptions[x]['title'], (top, 0), self.selectedControl == x)
                self.drawOption(pygame.key.name(self.controls[controlValue]), (top, 150), self.selectedControl == x)

        self.drawTabs()
        if self.changingKey:
            pygame.draw.rect(screen, (210,10,30), (0, 480 / 2 - 30, 640, 60))
            value = fontValue.render('Press any key to use for {} or press {} to cancel'.format(self.controlOptions[self.selectedControl]['title'], pygame.key.name(self.binds['cancel'])), True, WHITE)
            value_rect = value.get_rect(center=screen.get_rect().center)
            screen.blit(value, value_rect)
            pass
