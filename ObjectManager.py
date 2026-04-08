from enum import Enum, auto
from inspect import signature
from GameManager import gameManager
from Vectors import Vector3

class ObjectTypes(Enum):
    SQUARE = auto()
    CIRCLE = auto()



class Square:
    def __init__(self, topLeftVec, topRightVec, BottomLeftVec, BottomRightVec, color):

        self.topLeftVec = topLeftVec
        self.topRightVec = topRightVec
        self.BottomLeftVec = BottomLeftVec
        self.BottomRightVec = BottomRightVec
        self.color = color
        

class ObjectManager:
    def __init__(self):
        self.currentObjects = []
        return

    def createObject(self,objectType, *objectdata):
        if objectType == ObjectTypes.SQUARE:
            sig = signature(Square.__init__)
            if len(objectdata) != len(sig.parameters) - 1 :
                print("Invalid number of parameters for type SQUARE")
                gameManager.gameShutdown(-1)
            #if params are correct, then this part will run
            self.currentObjects.append(Square(objectdata[0], objectdata[1], objectdata[2],objectdata[3],objectdata[4]))

    def createWall(self, position: Vector3, width: float, height: float, color = "red"):
        X = position.x
        Y = position.y
        Z = position.z
        halfWidth = width / 2
        halfHeight = height / 2
        objectManager.createObject(
            ObjectTypes.SQUARE,
            Vector3(X - halfWidth, Y + halfHeight, Z),
            Vector3(X + halfWidth, Y + halfHeight, Z),
            Vector3(X - halfWidth, Y - halfHeight, Z),
            Vector3(X + halfWidth, Y - halfHeight, Z),
            color,
        )


objectManager = ObjectManager()
