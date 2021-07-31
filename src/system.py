import pygame as pg
from pygame.constants import K_BACKSLASH, K_BACKSPACE
import window
import utils
import player
import itertools

def loadImageKeepingAR(path, height):
    image = pg.image.load(path)
    imgHeight = pg.Surface.get_height(image)
    imgWidth = pg.Surface.get_width(image)
    aspectRatio = imgWidth / imgHeight
    size = (int(aspectRatio * float(height)), height)
    
    return pg.transform.scale(image, size)

def loadImage(path, size):
    return pg.transform.scale(pg.image.load(path), size)
 
def loadWindow():
    return utils.loadJSON('assets/data/window.json')

def loadCharList():
    return utils.loadTxt('assets/data/charList.txt')

def loadCharacter(character):
    return utils.loadJSON('assets/data/' + character + '.json')

def write(model, string, color, xPos, yPos, size):
    # todo: move this next line of code to the utils lib
    # possibly, creating a function where we can send the size of the text we want and receive a dict
    # so we can use it like: size40Text['robotoMedium'] or size25Text['joystix']
    text = pg.font.Font('assets/fonts/RobotoMono-Medium.ttf', size)
    textSurf, textRect = text_objects(string, text, color)
    if not xPos:
        textRect.center = ((model['windowObject'].returnWindowSize()[0]/2), (yPos))
    else:
        textRect.center = (xPos, yPos)

    model['pgWindow'].blit(textSurf, textRect)

def writeLeftAlign(model, string, color, xPos, yPos, size):
    # todo: move this next line of code to the utils lib
    # possibly, creating a function where we can send the size of the text we want and receive a dict
    # so we can use it like: size40Text['robotoMedium'] or size25Text['joystix']
    text = pg.font.Font('assets/fonts/RobotoMono-Medium.ttf', size)
    textSurf, textRect = text_objects(string, text, color)
    textRect.x = xPos
    textRect.y = yPos

    model['pgWindow'].blit(textSurf, textRect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# todo: add color and square size to this function
def drawRectangle(pgWindow, pos, margin, width, height):
    outerRect = pg.Rect(pos[0], pos[1], width, height) # square size goes here
    innerRect = pg.Rect(pos[0] + margin, pos[1] + margin, width - (2 * margin), height - (2 * margin)) # square size goes here
    pg.draw.rect(pgWindow, (255, 255, 255), outerRect) # color goes here
    pg.draw.rect(pgWindow, (0, 0, 0), innerRect) # color goes here

def drawCharacter(pgWindow, charImage, pos, centerMargin):
    rect = charImage.get_rect()
    if centerMargin:
        rect.center = (pos[0] + 90, pos[1] + 90)
    else:
        rect.center = (pos[0], pos[1])
    pgWindow.blit(charImage, rect)

def setup():
    windowSettings = loadWindow()
    windowObject = window.Window(windowSettings['width'], windowSettings['height'])
    pepe = loadImageKeepingAR('assets/sprites/sadPepe.png', 128)
    redPepe = loadImageKeepingAR('assets/sprites/redSadPepe.png', 128)
    redPepe = pg.transform.flip(redPepe, True, False)
    paladin = loadImageKeepingAR('assets/sprites/terrariaPaladin.png', 128)
    wizard = loadImageKeepingAR('assets/sprites/terrariaWizard.png', 128)
    rogue = loadImageKeepingAR('assets/sprites/terrariaRogue.png', 128)
    necromancer = loadImageKeepingAR('assets/sprites/terrariaNecromancer.png', 128)
    skeleton = loadImageKeepingAR('assets/sprites/terrariaSkeleton.png', 128)

    pg.init()
    pgWindow = pg.display.set_mode(windowObject.returnWindowSize())
    pg.display.set_caption('The IntroBattle Project')
    clock = pg.time.Clock()
    pg.key.set_repeat(200)

    model = {
        'windowSettings': windowSettings,
        'windowObject': windowObject,
        'pgWindow': pgWindow,
        'clock': clock,
        'pepe': pepe,
        'redPepe': redPepe,
        'paladin': paladin,
        'wizard' : wizard,
        'rogue' : rogue,
        'necromancer': necromancer,
        'skeleton': skeleton
    }

    return model

charList = loadCharList()
characterJsonList = []

def charSelectionLoop(model):
    run = True
    selectedSquare = 0
    # todo: make this a JSON file
    allCharacterSquares = [(132, 200), (422, 200), (712, 200), (132, 490), (422, 490), (712, 490)]

    while run:
        model['clock'].tick(60)
        if len(characterJsonList) == 3:
            return characterJsonList
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYUP:
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
                elif event.key == pg.K_RETURN:
                    characterJsonList.append(loadCharacter(charList[selectedSquare]))
                
        model['pgWindow'].fill(model['windowObject'].returnColor())
        write(model, 'IntroBattle!', (255, 255, 255), None, 80, 45)

        for i in range(0, len(allCharacterSquares)):
            if i == selectedSquare:
                drawRectangle(model['pgWindow'], allCharacterSquares[i], 9, 180, 180)
                write(model, charList[i].capitalize(), (255, 255, 255), allCharacterSquares[i][0] + 90, allCharacterSquares[i][1] + 210, 38)
            else:
                drawRectangle(model['pgWindow'], allCharacterSquares[i], 5, 180, 180)
                write(model, charList[i].capitalize(), (255, 255, 255), allCharacterSquares[i][0] + 90, allCharacterSquares[i][1] + 210, 35)

            if charList[i] in model:
                drawCharacter(model['pgWindow'], model[charList[i]], (allCharacterSquares[i][0], allCharacterSquares[i][1]), True)
            else:
                drawCharacter(model['pgWindow'], model['pepe'], (allCharacterSquares[i][0], allCharacterSquares[i][1]), True)
            
        pg.display.update()

def loadCharacterObjects(characterList):
    returnList = []
    for character in characterList:
        currentCharacter = player.Player(character['displayName'], character['attack'], character['defense'], character['maxHP'], character['speed'], [], character['imageSrc'], (30, 30), character['resistances'], character['color'])
        returnList.append(currentCharacter)

    return returnList

def pickEnemyEncounter():
    #hardcoded for now
    returnList = []
    character = loadCharacter('necromancer')
    returnList.append(player.Player(character['displayName'], character['attack'], character['defense'], character['maxHP'], character['speed'], [], character['imageSrc'], (30, 30), character['resistances'], character['color']))
    character = loadCharacter('skeleton')
    returnList.append(player.Player(character['displayName'], character['attack'], character['defense'], character['maxHP'], character['speed'], [], character['imageSrc'], (30, 30), character['resistances'], character['color']))
    
    return returnList

def showCharacterStats(model, characterList):
    drawRectangle(model['pgWindow'], (600, 533), 3, 399, 211)
    y = (533 + 2 + 5 + 10)
    for char in characterList:
        writeLeftAlign(model, char.getName(), (255, 255, 255), (600 + 3 + 20) , y, 30)
        maxHPStr = str(char.getMaxHP())
        currHPStr = str(char.getCurrentHP())
        if char.getMaxHP() < 100:
            maxHPStr = ' ' + str(char.getMaxHP())
        if char.getCurrentHP() < 100:
            currHPStr = ' ' + str(char.getCurrentHP())
        hpStr = currHPStr + ' / ' + maxHPStr
        writeLeftAlign(model, hpStr , (255, 255, 255), 780 , y, 30)
        y += 70

def showCharactersInBattle(model, players, enemies):
    playerPositions = [(230, 120), (100, 280), (230, 430)]
    enemyPositions = [(830, 200), (760, 400)]

    for i in range(0, len(players)):
        drawCharacter(model['pgWindow'], model[players[i].getName().lower()], playerPositions[i], False)

    for i in range(0, len(enemies)):
        drawCharacter(model['pgWindow'], model[enemies[i].getName().lower()], enemyPositions[i], False)


def calcDamageBasicAttack(attacker, defender):
    # damage = attack - defence, plain and simple
    damage = 0
    if attacker.getAttack() - defender.getDefense() > 5:
        damage = attacker.getAttack() - defender.getDefense()
    else:
        damage = 5

    defender.updateLife(-1 * damage)

def attack(model, currentCharacter, characterList, enemyList):
    trianglePositions = [
        ((830, 120), (820, 110), (840, 110)),
        ((760, 320), (750, 310), (770, 310))
    ]
    enemySelection = 0

    run = True

    while run:
        model['pgWindow'].fill(model['windowObject'].returnColor())
        drawRectangle(model['pgWindow'], (12, 520), 6, 1000, 236)
        showTurn(model, currentCharacter)
        showCharactersInBattle(model, characterList, enemyList)

        for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                    elif event.type == pg.KEYUP:
                        if event.key == pg.K_ESCAPE:
                            run = False
                        elif event.key == pg.K_RETURN:
                            if enemySelection == 0:
                                calcDamageBasicAttack(currentCharacter, enemyList[0])
                                return 1
                            else:
                                calcDamageBasicAttack(currentCharacter, enemyList[1])
                                return 1
                            
                        elif (event.key == pg.K_UP and enemySelection == 1) or (event.key == pg.K_RIGHT and enemySelection == 1):
                            enemySelection = 0
                        elif (event.key == pg.K_DOWN and enemySelection == 0) or (event.key == pg.K_LEFT and enemySelection == 0):
                            enemySelection = 1
                        elif event.key == pg.K_BACKSPACE:
                            return 0

        pg.draw.polygon(model['pgWindow'], (230, 230, 230), trianglePositions[enemySelection])
        pg.display.update()

    return -1

def showTurn(model, currentCharacter):
    drawRectangle(model['pgWindow'], (23, 533), 3, 600 - (23 + 5), 211)
    writeLeftAlign(model, currentCharacter.getName() + '\'s turn!', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (533 + 3 + 5 + 10), 30)

# please god forgive me for these warcrimes
def showCurrCharacterMoves(model, selectionTrianglePos):
    writeLeftAlign(model, 'Attack', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (533 + 3 + 5 + 10 + 70), 30)
    writeLeftAlign(model, 'Insight', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (533 + 3 + 5 + 10 + 70 + 60), 30)
    writeLeftAlign(model, 'Defend', (255, 255, 255), (23 + 3 + 5+ 10 + 40 + 300) , (533 + 3 + 5 + 10 + 70), 30)
    writeLeftAlign(model, 'Skill', (255, 255, 255), (23 + 3 + 5+ 10 + 40 + 300) , (533 + 3 + 5 + 10 + 70 + 60), 30)
    pg.draw.polygon(model['pgWindow'], (255, 255, 255), selectionTrianglePos)

# lambda x : x.getSpeed() would work as well
def speedCompare(element):
    return element.getSpeed()

def battleLoop(model, characterList, enemyList):
    for i in characterList:
        print(i.getName())
    
    run = True

    selectionTrianglePos = 0
    #more warcrimes
    selectionTriangleList = [
    [((23 + 3 + 5+ 10 + 40 - 10) , (533 + 3 + 5 + 10 + 70 + 20)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 10)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 30))],
    [((23 + 3 + 5+ 10 + 40 + 300 - 10) , (533 + 3 + 5 + 10 + 70 + 20)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 10)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 30))],
    [((23 + 3 + 5+ 10 + 40 - 10) , (533 + 3 + 5 + 10 + 70 + 60 + 20)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 10)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 30))],
    [((23 + 3 + 5+ 10 + 40 + 300 - 10) , (533 + 3 + 5 + 10 + 70 + 60 + 20)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 10)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 30))]
    ]

    battleList = sorted(characterList + enemyList, key=speedCompare, reverse = True)
    battleList = itertools.cycle(battleList)
    currentCharacter = next(battleList)

    model['pgWindow'].fill(model['windowObject'].returnColor())
    while run:
        drawRectangle(model['pgWindow'], (12, 520), 6, 1000, 236)
        showTurn(model, currentCharacter)
        showCharactersInBattle(model, characterList, enemyList)
        
        print(enemyList[1].getName())
        print(enemyList[1].getCurrentHP())

        if currentCharacter in enemyList:
            showCharacterStats(model, characterList)
            # calcDamageBasicAttack(currentCharacter, characterList[0])
            pg.display.update()
            pg.time.wait(2800)
            currentCharacter = next(battleList)
        else:
            showCurrCharacterMoves(model, selectionTriangleList[selectionTrianglePos])
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                    elif event.type == pg.KEYUP:
                        if event.key == pg.K_ESCAPE:
                            run = False
                        elif event.key == pg.K_RETURN:
                            if selectionTrianglePos == 0:
                                attkResult = attack(model, currentCharacter, characterList, enemyList)
                                if attkResult == -1:
                                    run = False
                                elif attkResult == 1:
                                    currentCharacter = next(battleList)
                        elif event.key == pg.K_UP and selectionTrianglePos > 1:
                            selectionTrianglePos -= 2
                        elif event.key == pg.K_DOWN and selectionTrianglePos < 2:
                            selectionTrianglePos += 2
                        elif event.key == pg.K_RIGHT and selectionTrianglePos % 2 == 0:
                            selectionTrianglePos += 1
                        elif event.key == pg.K_LEFT and selectionTrianglePos % 2 == 1:
                            selectionTrianglePos -= 1
                    elif event.type == pg.MOUSEBUTTONUP:
                        if event.button == 1:
                           print(pg.mouse.get_pos())

            showCharacterStats(model, characterList)
            pg.display.update()
            