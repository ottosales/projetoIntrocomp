import pygame as pg
import window
import utils

def loadWindow():
    return utils.loadJSON('../assets/data/window.json')

def write(model, string, color, yPos, size):
    # todo: move this next line of code to the utils lib
    # possibly, creating a function where we can send the size of the text we want and receive a dict
    # so we can use it like: size40Text['robotoMedium'] or size25Text['joystix']
    text = pg.font.Font('../assets/fonts/RobotoMono-Medium.ttf', size)
    textSurf, textRect = text_objects(string, text, color)
    textRect.center = ((model['windowObject'].returnWindowSize()[0]/2), (yPos))

    model['pgWindow'].blit(textSurf, textRect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# todo: add color and square size to this function
def drawSquare(pgWindow, pos, margin):
    outerRect = pg.Rect(pos[0], pos[1], 180, 180) # square size goes here
    innerRect = pg.Rect(pos[0] + margin, pos[1] + margin, 180 - (2 * margin), 180 - (2 * margin)) # square size goes here
    pg.draw.rect(pgWindow, (255, 255, 255), outerRect) # color goes here
    pg.draw.rect(pgWindow, (0, 0, 0), innerRect) # color goes here

def setup():
    windowSettings = loadWindow()
    print(windowSettings)
    windowObject = window.Window(windowSettings['width'], windowSettings['height'])

    pg.init()
    pgWindow = pg.display.set_mode(windowObject.returnWindowSize())
    pg.display.set_caption('The IntroBattle Project')
    pg.key.set_repeat(100)
    clock = pg.time.Clock()
    pg.key.set_repeat(100)

    model = {
        'windowSettings': windowSettings,
        'windowObject': windowObject,
        'pgWindow': pgWindow,
        'clock': clock
    }

    return model


def charSelectionLoop(model):
    run = True
    selectedSquare = 0
    # todo: make this a JSON file
    allCharacterSquares = [(132, 200) , (422, 200), (712, 200), (132, 490) , (422, 490), (712, 490)]

    while run:
        model['clock'].tick(60)
        print(selectedSquare)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_UP and selectedSquare > 2:
                    selectedSquare -= 3
                elif event.key == pg.K_DOWN and selectedSquare < 3:
                    selectedSquare += 3
                elif event.key == pg.K_RIGHT and (selectedSquare != 2 and selectedSquare != 5):
                    selectedSquare += 1
                elif event.key == pg.K_LEFT and (selectedSquare != 0 and selectedSquare != 3):
                    selectedSquare -= 1
                
        
        model['pgWindow'].fill(model['windowObject'].returnColor())
        write(model, 'The IntroBattle Project', (255, 255, 255), 80, 45)

        for i in range(0, len(allCharacterSquares)):
            if i == selectedSquare:
                drawSquare(model['pgWindow'], allCharacterSquares[i], 9)
            else:
                drawSquare(model['pgWindow'], allCharacterSquares[i], 5)
        
        pg.display.update()