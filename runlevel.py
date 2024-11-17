import json
from main import *

def getLevel(filename):
    levelFile = open(f"levels/{filename}", "r")
    levelFileStr = levelFile.read()
    levelObj = json.loads(levelFileStr)
    print(levelObj)

    player = PLAYER(np.array(levelObj["player"]))

    charges = []
    for charge in levelObj["charges"]:
        charges.append(POINT_CHARGE(np.array(charge[0]), charge[1], charge[2]))

    wires = []
    for wire in levelObj["wires"]:
        wires.append(WIRE(np.array(wire[0]), np.array(wire[1]), wire[2]))

    walls = []
    for wall in levelObj["walls"]:
        x_vals = [wall[0][0], wall[1][0]]
        y_vals = [wall[1][0], wall[1][1]]
        x_bot, y_bot = min(x_vals), min(y_vals)
        x_top, y_top = max(x_vals), max(y_vals)
        walls.append(WALL([x_bot, x_top, y_bot, y_top]))

getLevel()
