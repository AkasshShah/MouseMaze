# import os
# import sys
# import time
import gym
import random
# from six import StringIO
# from gym import error, spaces
from gym import utils
from gym.utils import seeding
# import numpy as np

# vars initialization:

p = {'name': 'pizza', 'color': 'yellow'}
t = {'name': 'trap', 'color': 'red'}
m = {'name': 'mouse', 'color': 'white'}
w = {'name': 'wall', 'color': 'blue'}
x = {'name': 'empty', 'color': 'green'}
v = {'name': 'void', 'color': 'clear'}
'''
MAP = [
    [x, v, p, v, x, v, x],
    [v, v, w, v, w, v, v],
    [x, w, x, v, t, w, x],
    [v, v, v, v, v, v, v],
    [x, v, x, w, x, w, t],
    [v, v, w, v, v, v, v],
    [p, w, p, v, x, v, x]
]
'''
MAP = [
    [x, v, x, v, x, v, x],
    [v, w, w, v, w, w, v],
    [x, w, x, v, x, w, x],
    [v, v, v, v, v, w, v],
    [x, v, x, w, x, w, x],
    [v, w, w, w, v, v, v],
    [x, w, x, v, x, v, x]
]


class MouseMazeEnv(gym.Env):
    '''
    The MouseMaze Problem

    Rendering:
    -yellow (p): pizza/cheese
    -red (t): shockwire/trap
    -white (m): mouse
    -blue (w): wall
    -green (x): empty space that the mouse can possibly land on
    -clear (v): void
    '''
    metadata = {'render.modes': ['color', 'text']}

    def __init__(self):
        # self.desc = np.asarray(MAP, dtype='c')
        self.rewardDict = self.rewardDictFunc()
        self.MAP = MAP
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.MAPwithMouse = MAP
        # trapArray = [(6, 6), (0, 6)]
        # rewardArray = [(0, 2), (2, 2), (6, 2)]
        # self.encode((0, 0), trapArray, rewardArray)
        self.reset()
        self.possibleActions = ['N', 'S', 'W', 'E']

    def reset(self):
        trapArray = [(6, 6), (0, 6)]
        rewardArray = [(0, 2), (2, 2), (6, 2)]
        self.encode((0, 0), trapArray, rewardArray)

    def rewardDictFunc(self):
        rewardDict = {
            'wall': -7,
            'trap': -8,
            'normal': -1,
            'pizza': 25
        }
        return(rewardDict)

    def randomMousePos(self):
        while(True):
            rand1 = random.randint(0, 6)
            rand2 = random.randint(0, 6)
            if(self.MAP[rand1][rand2] == x):
                self.MAPwithMouse[rand1][rand2] = m
                break

    def decode(self):
        # mousePos=self.getMousePos()
        trapArr = []
        rewArr = []
        mousePos = (-1, -1)
        for yy in range(0, 7):
            for xx in range(0, 7):
                if self.MAPwithMouse[yy][xx] == m:
                    mousePos = (xx, yy)
                elif self.MAPwithMouse[yy][xx] == t:
                    trapArr.append((xx, yy))
                elif self.MAPwithMouse[yy][xx] == p:
                    rewArr.append((xx, yy))
        return((mousePos, rewArr, trapArr))

    def encode(self, mouseTup, shockArrTup, pizzaArrTup):
        self.MAPwithMouse = MAP
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        for i in pizzaArrTup:
            if self.setMapBlock(i[0], i[1], p):
                self.numberOfPizzasRemaining += 1
        for i in shockArrTup:
            if self.setMapBlock(i[0], i[1], t):
                self.numberOfTrapsRemaining += 1
        self.setMapBlock(mouseTup[0], mouseTup[1], m)

    def printMAP(self):
        for i in range(7):
            for j in range(7):
                print(self.MAPwithMouse[i][j]['name'], end='')
                print('', end='\t\t')
            print('\n', end='')

    def getMousePos(self):
        for y in range(7):
            for xx in range(7):
                if(self.MAPwithMouse[y][xx] == m):
                    return((xx, y))

    def render(self, mode='color'):
        if(mode != 'color'):
            self.printMAP()
            return
        for i in range(7):
            for j in range(7):
                if(self.MAPwithMouse[i][j]['color'] != 'clear'):
                    print(utils.colorize(
                        '   ', self.MAPwithMouse[i][j]['color'], highlight=True), end='')
                else:
                    print('   ', end='')
            print('', end='\n')

    def randomAction(self):
        return(self.possibleActions[random.randint(0, 3)])

    def takeRadomAction(self):
        return(self.step(self.randomAction()))

    def wantsToGoOutOfBounds(self, amnt, VorH):
        currMousePos = self.getMousePos()
        currX = currMousePos[0]
        currY = currMousePos[1]
        if(VorH == 'V'):
            return(currY + amnt < 0 or currY + amnt > 6)
        elif(VorH == 'H'):
            return(currX + amnt < 0 or currX + amnt > 6)
        return(False)

    def moveNorthSouth(self, amnt):
        OrgMousePos = self.getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if(not self.wantsToGoOutOfBounds(2*amnt, 'V')):
            if(self.getMapBlock(OrgMousePosX, OrgMousePosY+amnt) != w):
                # self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                if(self.getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
                elif(self.getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
                elif(self.getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
            else:
                rewardUpdate += self.rewardDict['wall']
                rtnIssue = 'wall'
        else:
            rewardUpdate += self.rewardDict['wall']
            rtnIssue = 'wall'
        return(self.decode(), rewardUpdate, done)

    def moveEastWest(self, amnt):
        OrgMousePos = self.getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if(not self.wantsToGoOutOfBounds(2*amnt, 'H')):
            if(self.getMapBlock(OrgMousePosX+amnt, OrgMousePosY) != w):
                if(self.getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
                elif(self.getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
                elif(self.getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
            else:
                rewardUpdate += self.rewardDict['wall']
                rtnIssue = 'wall'
        else:
            rewardUpdate += self.rewardDict['wall']
            rtnIssue = 'wall'
        return(self.decode(), rewardUpdate, done)

    def getMapBlock(self, xcord, ycord):
        return(self.MAPwithMouse[ycord][xcord])

    def setMapBlock(self, xcord, ycord, newVal):
        if(xcord % 2 == 0 and ycord % 2 == 0):
            self.MAPwithMouse[ycord][xcord] = newVal
            return True
        return False

    def step(self, action):
        if action == 'N':
            return(self.moveNorthSouth(-1))
        elif action == 'S':
            return(self.moveNorthSouth(1))
        elif action == 'W':
            return(self.moveEastWest(-1))
        elif action == 'E':
            return(self.moveEastWest(1))


m1 = MouseMazeEnv()
m1.render(mode='color')

stepsTaken = 0
done = False
rewards = 0
frames = []
while(not done):
    decode, reward, done = m1.takeRadomAction()
    rewards += reward
    stepsTaken += 1
    m1.render()
    print('-----------------------------------------------------------')
print('Number of steps taken= ' + str(stepsTaken) +
      '\nReward Acheived=' + str(rewards))
