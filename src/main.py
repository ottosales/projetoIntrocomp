import pygame as pg
import system

model = system.setup()
characterList = system.charSelectionLoop(model)
characterList = system.loadCharacterObjects(characterList)
system.battleLoop(model, characterList)