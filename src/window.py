class Window:
    __width = 0
    __height = 0
    __color = (0, 0, 0)

    def __init__(self):
        self.__width = 800
        self.__height = 600

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def returnWindowSize(self):
        return (self.__width, self.__height)

    def returnColor(self):
        return self.__color