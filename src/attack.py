class Attack:
    __name = 'missing attack name'
    __damage = 0
    __damageType = 'missing damage type'
    __damageSubType = 'missing damage subtype'
    
    def __init__(self, name, damage, damageType, damageSubType):
        self.__name = name
        self.__damage = damage
        self.__damageType = damageType # physical or magical 
        self.__damageSubType = damageSubType # slashing, piercing, bludgeoning, fire, dark, electric...
    
    def getAttackName(self):
        return self.__name
    
    def getAttackDamage(self):
        return self.__damage

    def getAttackDamageType(self):
        return self.__damageType

    def getAttackDamageSubType(self):
        return self.__damageSubType