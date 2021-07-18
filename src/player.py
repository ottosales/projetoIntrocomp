class Player:
    __name = None
    __attack = 0
    __defense = 0
    __maxHP = 0
    __currentHP = 0
    __speed = 0
    __attackList = 0
    __canBePicked = True
    __imageSrc = None
    __position = None
    __resistances = None
    __mainColor = None

    def __init__(self, name, attack, defense, maxHP, speed, attackList, imageSrc, position, resistances, color):
        self.__name = name
        self.__attack = attack
        self.__defense = defense
        self.__maxHP = self.__currentHP = maxHP
        self.__speed = speed
        self.__attackList = attackList
        self.__imageSrc = imageSrc
        self.__position = position
        self.__resistances = resistances
        self.__mainColor = color

    def getName(self):
        return self.__name
    
    def getAttack(self):
        return self.__attack
    
    def getDefense(self):
        return self.__defense
    
    def getMaxHP(self):
        return self.__maxHP
    
    def getCurrentHP(self):
        return self.__currentHP

    def getSpeed(self):
        return self.__speed
    
    def getAttackList(self):
        return self.__attackList
    
    def getImage(self):
        return self.__imageSrc
    
    def getPosition(self):
        return self.__position
    
    def getResistances(self):
        return self.__resistances

    def getMainColor(self):
        return self.__mainColor

    def canBePicked(self):
        return self.__canBePicked

    def pick(self):
        self.__canBePicked = False
    
    def updateLife(self, damage):
        if damage > 0 and self.__currentHP + damage > self.__maxHP:
            self.__currentHP = self.__maxHP
        elif damage < 0 and self.__currentHP + damage <= 0:
            self.__currentHP = 0
            return 0 #code understands this as "died"
        else:
            self.__currentHP += damage
            return 1