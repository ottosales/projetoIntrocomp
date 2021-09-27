import pygame as pg
from pygame.constants import K_BACKSLASH, K_BACKSPACE
import window
import utils
import player
import random

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
    print(textRect, string)
    model['pgWindow'].blit(textSurf, textRect)

def writeLeftAlign(model, string, color, xPos, yPos, size):
    # todo: move this next line of code to the utils lib
    # possibly, creating a function where we can send the size of the text we want and receive a dict
    # so we can use it like: size40Text['robotoMedium'] or size25Text['joystix']
    text = pg.font.Font('assets/fonts/joystix monospace.ttf', size)
    textSurf, textRect = text_objects(string, text, color)
    textRect.x = xPos
    textRect.y = yPos

    textSurf2, textRect2 = text_objects(string, text, (0, 0, 0))
    textRect2.x = xPos + 2
    textRect2.y = yPos + 2
    model['pgWindow'].blit(textSurf2, textRect2)
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
    background = loadImage('assets/sprites/bgLarge.png', (1024, 768))
    pepe = loadImageKeepingAR('assets/sprites/sadPepe.png', 128)
    redPepe = loadImageKeepingAR('assets/sprites/redSadPepe.png', 128)
    redPepe = pg.transform.flip(redPepe, True, False)
    paladin = loadImageKeepingAR('assets/sprites/paladin.png', 128)
    wizard = pg.transform.flip(loadImageKeepingAR('assets/sprites/wizard.png', 128), True, False)
    rogue = loadImageKeepingAR('assets/sprites/rogue.png', 128)
    necromancer = pg.transform.flip(loadImageKeepingAR('assets/sprites/necro.png', 128), True, False)
    skeleton = pg.transform.flip(loadImageKeepingAR('assets/sprites/skelly.png', 128), True, False)
    hunter = loadImageKeepingAR('assets/sprites/hunter.png', 128)
    priest = loadImageKeepingAR('assets/sprites/priest.png', 128)
    arrow = loadImageKeepingAR('assets/sprites/arrow.png', 26)
    sideArrow = pg.transform.rotate(loadImageKeepingAR('assets/sprites/arrow.png', 26), 90)
    menu = loadImage('assets/sprites/menu.png', (180, 180))
    menuLeft = loadImage('assets/sprites/menuLeft.png', (580, 220))
    # pg.Surface.set_alpha(menuLeft, 210)
    menuRight = loadImage('assets/sprites/menuRight.png', (400, 220))
    # pg.Surface.set_alpha(menuRight, 210)

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
        'background': background,
        'pepe': pepe,
        'redPepe': redPepe,
        'paladin': paladin,
        'wizard' : wizard,
        'rogue' : rogue,
        'necromancer': necromancer,
        'skeleton': skeleton,
        'hunter': hunter,
        'priest': priest,
        'menu': menu,
        'arrow': arrow,
        'sideArrow': sideArrow,
        'menuLeft': menuLeft,
        'menuRight': menuRight
    }

    return model

charList = loadCharList()
characterJsonList = []

def charSelectionLoop(model):
    run = True
    selectedSquare = 0
    # todo: make this a JSON file
    allCharacterSquares = [(132, 220), (422, 220), (712, 220), (277, 510), (567, 510)]

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
                elif event.key == pg.K_DOWN and selectedSquare < 2:
                    selectedSquare += 3
                elif event.key == pg.K_RIGHT and (selectedSquare != 2 and selectedSquare != 5):
                    selectedSquare += 1
                elif event.key == pg.K_LEFT and (selectedSquare != 0 and selectedSquare != 3):
                    selectedSquare -= 1
                elif event.key == pg.K_RETURN:
                    characterJsonList.append(loadCharacter(charList[selectedSquare]))
                
        # model['pgWindow'].fill(model['windowObject'].returnColor())
        model['pgWindow'].blit(model['background'], (0, 0))
        drawRectangle(model['pgWindow'], (320, 40), 5, 384, 80)
        write(model, 'IntroBattle!', (255, 255, 255), None, 80, 45)

        for i in range(0, len(charList)):
            if i == selectedSquare:
                # drawRectangle(model['pgWindow'], allCharacterSquares[i], 9, 180, 180)
                model['pgWindow'].blit(model['arrow'], (allCharacterSquares[i][0] + 77, allCharacterSquares[i][1] - 30))
                model['pgWindow'].blit(model['menu'], allCharacterSquares[i])
                write(model, charList[i].capitalize(), (255, 255, 255), allCharacterSquares[i][0] + 90, allCharacterSquares[i][1] + 210, 40)
            else:
                # drawRectangle(model['pgWindow'], allCharacterSquares[i], 5, 180, 180)
                model['pgWindow'].blit(model['menu'], allCharacterSquares[i])
                write(model, charList[i].capitalize(), (255, 255, 255), allCharacterSquares[i][0] + 90, allCharacterSquares[i][1] + 210, 32)

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
    # drawRectangle(model['pgWindow'], (600, 533), 3, 399, 211)
    model['pgWindow'].blit(model['menuRight'], (600, 533))
    y = (553 + 2 + 5 + 10)
    for char in characterList:
        writeLeftAlign(model, char.getName(), (255, 255, 255), (600 + 3 + 20) , y, 25)
        maxHPStr = str(char.getMaxHP())
        currHPStr = str(char.getCurrentHP())
        if char.getMaxHP() < 100:
            maxHPStr = ' ' + str(char.getMaxHP())
        if char.getCurrentHP() < 100:
            currHPStr = ' ' + str(char.getCurrentHP())
        hpStr = currHPStr + ' / ' + maxHPStr
        writeLeftAlign(model, hpStr , (255, 255, 255), 780 , y, 25)
        y += 60

def showCharactersInBattle(model, players, enemies):
    playerPositions = [(230, 240), (100, 340), (230, 440)]
    enemyPositions = [(830, 230), (760, 400)]

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
    # trianglePositions = [
    #     ((830, 120), (820, 110), (840, 110)),
    #     ((760, 320), (750, 310), (770, 310))
    # ]
    trianglePositions = [
        (815, 120),
        (735, 300)
    ]
    enemySelection = 0

    run = True

    while run:
        # model['pgWindow'].fill(model['windowObject'].returnColor())
        model['pgWindow'].blit(model['background'], (0, 0))
        # drawRectangle(model['pgWindow'], (12, 520), 6, 1000, 236)
        showCharacterStats(model, characterList)
        showTurn(model, currentCharacter)
        showAttackMessage(model, currentCharacter, characterList)
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
                        elif ((event.key == pg.K_DOWN and enemySelection == 0) or (event.key == pg.K_LEFT and enemySelection == 0)) and len(enemyList) != 1:
                            enemySelection = 1
                        elif event.key == pg.K_BACKSPACE:
                            return 0

        # pg.draw.polygon(model['pgWindow'], (230, 230, 230), trianglePositions[enemySelection])
        model['pgWindow'].blit(model['arrow'], trianglePositions[enemySelection])
        pg.display.update()

    return -1

def showTurn(model, currentCharacter):
    # drawRectangle(model['pgWindow'], (23, 533), 3, 600 - (23 + 5), 211)
    model['pgWindow'].blit(model['menuLeft'], (15, 533))
    writeLeftAlign(model, currentCharacter.getName() + '\'s turn!', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (553 + 3 + 5 + 10), 25)

def showDefeated(model, name):
    # drawRectangle(model['pgWindow'], (23, 533), 3, 600 - (23 + 5), 211)
    model['pgWindow'].blit(model['menuLeft'], (15, 533))
    writeLeftAlign(model, name, (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (553 + 3 + 5 + 10), 25)
    writeLeftAlign(model, 'was defeated!', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (553 + 3 + 5 + 10 + 50), 25)

def showAttackMessage(model, currentCharacter, characterList):
    if currentCharacter in characterList:
        writeLeftAlign(model, 'Select your target!', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (553 + 3 + 5 + 10 + 70), 25)
    else:
        writeLeftAlign(model, 'It will attack soon...', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (553 + 3 + 5 + 10 + 70), 25)

# please god forgive me for these warcrimes
def showCurrCharacterMoves(model, selectionTrianglePos):
    writeLeftAlign(model, 'Attack', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (533 + 3 + 5 + 10 + 70), 25)
    writeLeftAlign(model, 'Insight', (255, 255, 255), (23 + 3 + 5+ 10 + 40) , (533 + 3 + 5 + 10 + 70 + 60), 25)
    writeLeftAlign(model, 'Defend', (255, 255, 255), (23 + 3 + 5+ 10 + 40 + 300) , (533 + 3 + 5 + 10 + 70), 25)
    writeLeftAlign(model, 'Skill', (255, 255, 255), (23 + 3 + 5+ 10 + 40 + 300) , (533 + 3 + 5 + 10 + 70 + 60), 25)
    # pg.draw.polygon(model['pgWindow'], (255, 255, 255), selectionTrianglePos)
    model['pgWindow'].blit(model['sideArrow'], selectionTrianglePos)

# lambda x : x.getSpeed() would work as well
def speedCompare(element):
    return element.getSpeed()

def deathCheck(list):
    for element in list:
        if element.getCurrentHP() == 0:
            return element

    return False

def nextIndex(index, list):
    listLength = len(list)
    if index + 1 >= listLength:
        index = 0
    else:
        index += 1

    return index

def battleLoop(model, characterList, enemyList):
    random.seed()
    run = True

    selectionTrianglePos = 0
    #more warcrimes
    # selectionTriangleList = [
    # [((50) , (533 + 3 + 5 + 70 + 10)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 10)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 30))],
    # [((23 + 3 + 5+ 10 + 40 + 300 - 10) , (533 + 3 + 5 + 10 + 70 + 20)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 10)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 30))],
    # [((23 + 3 + 5+ 10 + 40 - 10) , (533 + 3 + 5 + 10 + 70 + 60 + 20)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 10)), ((23 + 3 + 5+ 10 + 40 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 30))],
    # [((23 + 3 + 5+ 10 + 40 + 300 - 10) , (533 + 3 + 5 + 10 + 70 + 60 + 20)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 10)), ((23 + 3 + 5+ 10 + 40 + 300 - 20) , (533 + 3 + 5 + 10 + 70 + 60 + 30))]
    # ]
    selectionTriangleList = [(50, 620), (350, 620), (50, 680), (350, 680)]

    battleList = sorted(characterList + enemyList, key=speedCompare, reverse = True)
    currentIndex = 0
    currentCharacter = battleList[currentIndex]

    while run:
        # model['pgWindow'].fill(model['windowObject'].returnColor())
        model['pgWindow'].blit(model['background'], (0, 0))
        # drawRectangle(model['pgWindow'], (12, 520), 6, 1000, 236)
        showTurn(model, currentCharacter)
        showCharactersInBattle(model, characterList, enemyList)

        if currentCharacter in enemyList:
            showCharacterStats(model, characterList)
            showAttackMessage(model, currentCharacter, characterList)
            target = random.randrange(0, len(characterList))
            calcDamageBasicAttack(currentCharacter, characterList[target])
            pg.display.update()
            pg.time.wait(3000)
            pg.event.clear()
            deathCheckReturn = deathCheck(battleList)
            if deathCheckReturn:
                battleList.remove(deathCheckReturn)
                showDefeated(model, deathCheckReturn.getName())
                pg.display.update()
                pg.time.wait(1800)
                if deathCheckReturn in characterList:
                    characterList.remove(deathCheckReturn)
                else:
                    enemyList.remove(deathCheckReturn)
            currentIndex = nextIndex(currentIndex, battleList)
            currentCharacter = battleList[currentIndex]
        else:
            if currentCharacter.isDefending():
                currentCharacter.stopDefending()
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
                                    deathCheckReturn = deathCheck(battleList)
                                    if deathCheckReturn:
                                        battleList.remove(deathCheckReturn)
                                        showDefeated(model, deathCheckReturn.getName())
                                        pg.display.update()
                                        pg.time.wait(1800)
                                        if deathCheckReturn in characterList:
                                            characterList.remove(deathCheckReturn)
                                        else:
                                            enemyList.remove(deathCheckReturn)
                                    currentIndex = nextIndex(currentIndex, battleList)
                                    currentCharacter = battleList[currentIndex]
                            elif selectionTrianglePos == 1:
                                currentCharacter.defend()
                                currentIndex = nextIndex(currentIndex, battleList)
                                currentCharacter = battleList[currentIndex]
                        elif event.key == pg.K_UP and selectionTrianglePos > 1:
                            selectionTrianglePos -= 2
                        elif event.key == pg.K_DOWN and selectionTrianglePos < 2:
                            selectionTrianglePos += 2
                        elif event.key == pg.K_RIGHT and selectionTrianglePos % 2 == 0:
                            selectionTrianglePos += 1
                        elif event.key == pg.K_LEFT and selectionTrianglePos % 2 == 1:
                            selectionTrianglePos -= 1

            showCharacterStats(model, characterList)

            if len(enemyList) == 0 or len(characterList) == 0:
                run = False

            pg.display.update()

    # model['pgWindow'].fill(model['windowObject'].returnColor())
    model['pgWindow'].blit(model['background'], (0, 0))
    showCharactersInBattle(model, characterList, enemyList)
    model['pgWindow'].blit(model['menuLeft'], (222, 533))
    # drawRectangle(model['pgWindow'], (12, 520), 6, 1000, 236)
    if len(enemyList) == 0:
        writeLeftAlign(model, "You won the battle! :)", (255, 255, 255), 275, 580, 25)

    else:
        writeLeftAlign(model, "You lost the battle! :(", (255, 255, 255), 275, 580, 25)

    pg.display.update()
    pg.time.wait(3000)