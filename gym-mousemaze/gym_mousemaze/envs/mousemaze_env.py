import os
import sys
import time
import gym
import random
from six import StringIO
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np

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
        self.rewardDict = self._rewardDictFunc()
        self.MAP = MAP
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.MAPwithMouse = MAP
        # trapArray = [(6, 6), (0, 6)]
        # rewardArray = [(0, 2), (2, 2), (6, 2)]
        # self._encode((0, 0), trapArray, rewardArray)
        self._reset()
        self.possibleActions = ['N', 'S', 'W', 'E']

    def _reset(self):
        trapArray = [(6, 6), (0, 6)]
        rewardArray = [(0, 2), (2, 2), (6, 2)]
        self._encode((0, 0), trapArray, rewardArray)

    def _rewardDictFunc(self):
        rewardDict = {
            'wall': -7,
            'trap': -8,
            'normal': -1,
            'pizza': 25
        }
        return(rewardDict)

    def _randomMousePos(self):
        while(True):
            rand1 = random.randint(0, 6)
            rand2 = random.randint(0, 6)
            if(self.MAP[rand1][rand2] == x):
                self.MAPwithMouse[rand1][rand2] = m
                break

    def _decode(self):
        # mousePos=self._getMousePos()
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

    def _encode(self, mouseTup, shockArrTup, pizzaArrTup):
        self.MAPwithMouse = MAP
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        for i in pizzaArrTup:
            if self._setMapBlock(i[0], i[1], p):
                self.numberOfPizzasRemaining += 1
        for i in shockArrTup:
            if self._setMapBlock(i[0], i[1], t):
                self.numberOfTrapsRemaining += 1
        self._setMapBlock(mouseTup[0], mouseTup[1], m)

    def _printMAP(self):
        for i in range(7):
            for j in range(7):
                print(self.MAPwithMouse[i][j]['name'], end='')
                print('', end='\t\t')
            print('\n', end='')

    def _getMousePos(self):
        for y in range(7):
            for xx in range(7):
                if(self.MAPwithMouse[y][xx] == m):
                    return((xx, y))

    def _render(self, mode='color'):
        if(mode != 'color'):
            self._printMAP()
            return
        for i in range(7):
            for j in range(7):
                if(self.MAPwithMouse[i][j]['color'] != 'clear'):
                    print(utils.colorize(
                        '   ', self.MAPwithMouse[i][j]['color'], highlight=True), end='')
                else:
                    print('   ', end='')
            print('', end='\n')

    def _randomAction(self):
        return(self.possibleActions[random.randint(0, 3)])

    def _takeRadomAction(self):
        return(self._step(self._randomAction()))

    def _wantsToGoOutOfBounds(self, amnt, VorH):
        currMousePos = self._getMousePos()
        currX = currMousePos[0]
        currY = currMousePos[1]
        if(VorH == 'V'):
            return(currY + amnt < 0 or currY + amnt > 6)
        elif(VorH == 'H'):
            return(currX + amnt < 0 or currX + amnt > 6)
        return(False)

    def _moveNorthSouth(self, amnt):
        OrgMousePos = self._getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if(not self._wantsToGoOutOfBounds(2*amnt, 'V')):
            if(self._getMapBlock(OrgMousePosX, OrgMousePosY+amnt) != w):
                # self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                if(self._getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
                elif(self._getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
                elif(self._getMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt)) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX, OrgMousePosY+(2*amnt), m)
            else:
                rewardUpdate += self.rewardDict['wall']
                rtnIssue = 'wall'
        else:
            rewardUpdate += self.rewardDict['wall']
            rtnIssue = 'wall'
        return(self._decode(), rewardUpdate, done)

    def _moveEastWest(self, amnt):
        OrgMousePos = self._getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if(not self._wantsToGoOutOfBounds(2*amnt, 'H')):
            if(self._getMapBlock(OrgMousePosX+amnt, OrgMousePosY) != w):
                if(self._getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
                elif(self._getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
                elif(self._getMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self._setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self._setMapBlock(OrgMousePosX+(2*amnt), OrgMousePosY, m)
            else:
                rewardUpdate += self.rewardDict['wall']
                rtnIssue = 'wall'
        else:
            rewardUpdate += self.rewardDict['wall']
            rtnIssue = 'wall'
        return(self._decode(), rewardUpdate, done)

    def _getMapBlock(self, xcord, ycord):
        return(self.MAPwithMouse[ycord][xcord])

    def _setMapBlock(self, xcord, ycord, newVal):
        if(xcord % 2 == 0 and ycord % 2 == 0):
            self.MAPwithMouse[ycord][xcord] = newVal
            return True
        return False

    def _step(self, action):
        if action == 'N':
            return(self._moveNorthSouth(-1))
        elif action == 'S':
            return(self._moveNorthSouth(1))
        elif action == 'W':
            return(self._moveEastWest(-1))
        elif action == 'E':
            return(self._moveEastWest(1))


m1 = MouseMazeEnv()
m1._render(mode='color')

stepsTaken = 0
done = False
rewards = 0
frames = []
while(not done):
    decode, reward, done = m1._takeRadomAction()
    rewards += reward
    stepsTaken += 1
    m1._render()
    print('-----------------------------------------------------------')
print('Number of steps taken= ' + str(stepsTaken) +
      '\nReward Acheived=' + str(rewards))
