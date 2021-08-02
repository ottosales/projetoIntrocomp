import pygame as pg
import system

model = system.setup()
characterList = system.charSelectionLoop(model)
characterList = system.loadCharacterObjects(characterList)
enemyList = system.pickEnemyEncounter()
system.battleLoop(model, characterList, enemyList)