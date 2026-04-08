from Renderer import Renderer
from Vectors import Vector3
from PlayerControlls import playerController
from Time import Time
import ObjectManager as objM
import Camera

renderer = Renderer(1280,920)
objectManager = objM.objectManager
camera = Camera.camera

testZ = 120
"""objectManager.createObject(
    objM.ObjectTypes.SQUARE,
    Vector3(-30, -30, testZ),
    Vector3(30, -30, testZ),
    Vector3(-30, 30, testZ),
    Vector3(30, 30, testZ),
    "red",
)"""

objectManager.createWall(Vector3(0, 0, testZ), 30,30)
while True:
    renderer.beginFrame()
    renderer.screen.fill("black")
    playerController.pollInput()
    renderer.drawAllObjects()
    renderer.stepRenderer()
