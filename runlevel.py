import json
from physics.props import *

def getLevel(filename):
    levelFile = open(f"levels/{filename}", "r")
    levelFileStr = levelFile.read()
    levelObj = json.loads(levelFileStr)
    print(levelObj)

    player = PLAYER(np.array(levelObj["player"]))

    win = []
    for win in levelObj["win"]:
        win.append(WIN(np.array(win[0]), np.array(win[1])))
        

    walls = []
    for wall in levelObj["walls"]:
        walls.append(WALL(np.array(wall[0]), np.array(wall[1])))

    wires = []
    for wire in levelObj["wires"]:
        wires.append(WIRE(np.array(wire[0]), np.array(wire[1]), wire[2]))
        
    charges = []
    for charge in levelObj["charges"]:
        charges.append(POINT_CHARGE(np.array(charge[0]), charge[1], charge[2]))


    
    return player
