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

MAP = [
    [x, v, p, v, x, v, x],
    [v, v, w, v, w, v, v],
    [x, w, x, v, t, w, x],
    [v, v, v, v, v, v, v],
    [x, v, x, w, x, w, t],
    [v, v, w, v, v, v, v],
    [p, w, p, v, x, v, x]
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
        self.MAP = MAP
        self._randomMousePos()
        self.possibleActions = ['N', 'S', 'W', 'E']

    def _randomMousePos(self):
        while(True):
            rand1 = random.randint(0, 6)
            rand2 = random.randint(0, 6)
            if(self.MAP[rand1][rand2] == x):
                self.MAP[rand1][rand2] = m
                break

    def _printMAP(self):
        for i in range(7):
            for j in range(7):
                print(self.MAP[i][j]['name'], end='')
                print('', end='\t\t')
            print('\n', end='')

    def _getMousePos(self):
        for y in range(7):
            for xx in range(7):
                if(self.MAP[y][xx] == m):
                    return((xx, y))

    def _render(self, mode='color'):
        if(mode != 'color'):
            self._printMAP()
            return
        out = self.MAP
        for i in range(7):
            for j in range(7):
                if(self.MAP[i][j]['color'] != 'clear'):
                    print(utils.colorize(
                        self.MAP[i][j]['name'], self.MAP[i][j]['color'], highlight=True), end='\t')
                else:
                    print(' ', end='\t')
            print('', end='\n')

    def _step(self, action):
        mPos = self._getMousePos()
        mPosX = mPos[0]
        mPosY = mPos[1]
        if action == 'N':
            if(mPosY == 0):
                print('No')
