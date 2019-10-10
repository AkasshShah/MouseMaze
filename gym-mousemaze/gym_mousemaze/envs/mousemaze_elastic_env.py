import gym
from gym import utils
from gym.utils import seeding
from six import StringIO

p = {'name': 'pizza', 'color': 'yellow'}
t = {'name': 'trap', 'color': 'red'}
m = {'name': 'mouse', 'color': 'white'}
w = {'name': 'wall', 'color': 'blue'}
x = {'name': 'empty', 'color': 'green'}
v = {'name': 'void', 'color': 'clear'}


class ElasticMouseMazeEnv(gym.Env):
    def __init__(self):
        self.MAPwithMouse = []
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.numberOfWalls = 0
        self.rewardDict = self.rewardDictFunc()
        self.possibleActions = ['N', 'S', 'W', 'E']
        self.reset()

    def setMapBlockWall(self, xcord, ycord):
        if(xcord % 2 == 1 or ycord % 2 == 1):
            self.MAPwithMouse[ycord][xcord] = w
            return True
        return False

    def setMapBlock(self, xcord, ycord, newVal):
        if(xcord % 2 == 0 and ycord % 2 == 0):
            self.MAPwithMouse[ycord][xcord] = newVal
            return True
        return False

    def initMap(self, side):
        self.MAPwithMouse = []
        for yy in range(side):
            new = []
            for xx in range(side):
                if xx % 2 == 0 and yy % 2 == 0:
                    new.append(x)
                else:
                    new.append(v)
            self.MAPwithMouse.append(new)

    def encode(self, sqn, mTup, arrTrapTup, arrRewTup, arrWallTup):
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.numberOfWalls = 0
        self.initMap(2 * sqn)
        for trap in arrTrapTup:
            if self.setMapBlock(2 * trap[0], 2 * trap[1], t):
                self.numberOfTrapsRemaining += 1
        for rew in arrRewTup:
            if self.setMapBlock(2 * rew[0], 2 * rew[1], p):
                self.numberOfPizzasRemaining += 1
        for wall in arrWallTup:
            new1 = (2 * wall[0][0], 2 * wall[0][1])
            new2 = (2 * wall[1][0], 2 * wall[1][1])
            new3 = (int((new1[0] + new2[0]) / 2), int((new1[1] + new2[1]) / 2))
            if self.setMapBlockWall(new3[0], new3[1]):
                self.numberOfWalls += 1
        if self.setMapBlock(2 * mTup[0], 2 * mTup[1], m):
            return True
        return False

    def reset(self):
        side = 3
        mousePos = (0, 2)
        trapArr = [(0, 1)]
        rewArr = [(0, 0)]
        wallArr = [
            ((0, 0), (0, 1)),
            ((0, 0), (1, 1))
        ]
        self.encode(side, mousePos, trapArr, rewArr, wallArr)

    def getMousePos(self):
        for y in range(len(self.MAPwithMouse)):
            for xx in range(len(self.MAPwithMouse[y])):
                if(self.MAPwithMouse[y][xx] == m):
                    return((xx, y))

    def wantsToGoOutOfBounds(self, amnt, VorH):
        currMousePos = self.getMousePos()
        currX = currMousePos[0]
        currY = currMousePos[1]
        if(VorH == 'V'):
            # return(currY + amnt < 0 or currY + amnt > 6)
            return(currY + amnt < 0 or currY + amnt >= len(self.MAPwithMouse))
        elif(VorH == 'H'):
            #     return(currX + amnt < 0 or currX + amnt > 6)
            return(currX + amnt < 0 or currX + amnt >= len(self.MAPwithMouse))
        return(False)

    def getMapBlock(self, xcord, ycord):
        return(self.MAPwithMouse[ycord][xcord])

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

    def wallDecode(self, xx, yy):
        new1 = [0, 0]
        new2 = [0, 0]
        xx = int(xx)
        yy = int(yy)
        if xx % 2 == 1 and yy % 2 == 1:
            new1[1] = int((yy - 1) / 2)
            new2[1] = int((yy + 1) / 2)
            new1[0] = int((xx - 1) / 2)
            new2[0] = int((xx + 1) / 2)
        if xx % 2 == 0 and yy % 2 == 1:
            new1[1] = int((yy - 1)/2)
            new2[1] = int((yy + 1)/2)
            new1[0] = xx
            new2[0] = xx
        if yy % 2 == 0 and xx % 2 == 1:
            new1[0] = int((xx - 1)/2)
            new2[0] = int((xx + 1)/2)
            new1[1] = yy
            new2[1] = yy
        new1 = tuple(new1)
        new2 = tuple(new2)
        rtn = ((new1), (new2))
        return rtn

    def decode(self):
        arrTrap = []
        arrRew = []
        mousePos = (0, 0)
        wallArr = []
        for yy in range(len(self.MAPwithMouse)):
            for xx in range(len(self.MAPwithMouse[yy])):
                if self.getMapBlock(xx, yy) == t:
                    arrTrap.append((int(xx/2), int(yy/2)))
                elif self.getMapBlock(xx, yy) == p:
                    arrRew.append((int(xx/2), int(yy/2)))
                elif self.getMapBlock(xx, yy) == w:
                    # print("found wall at: ", xx, "   ", yy)
                    wallArr.append(self.wallDecode(xx, yy))
                elif self.getMapBlock(xx, yy) == m:
                    mousePos = (int(xx/2), int(yy/2))
        return((int(len(self.MAPwithMouse)/2), mousePos, arrRew, arrTrap, wallArr))

    def step(self, action):
        if action == 'N':
            return(self.moveNorthSouth(-1))
        elif action == 'S':
            return(self.moveNorthSouth(1))
        elif action == 'W':
            return(self.moveEastWest(-1))
        elif action == 'E':
            return(self.moveEastWest(1))

    def rewardDictFunc(self):
        rewardDict = {
            'wall': -7,
            'trap': -8,
            'normal': -1,
            'pizza': 25
        }
        return(rewardDict)

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

    def printMAP(self):
        for i in range(len(self.MAPwithMouse)):
            for j in range(len(self.MAPwithMouse[i])):
                print(self.MAPwithMouse[i][j]['name'], end='')
                print('', end='\t\t')
            print('\n', end='')

    def render(self, mode='color'):
        if(mode != 'color'):
            self.printMAP()
            return
        for i in range(len(self.MAPwithMouse)):
            for j in range(len(self.MAPwithMouse[i])):
                if(self.MAPwithMouse[i][j]['color'] != 'clear'):
                    print(utils.colorize(
                        '   ', self.MAPwithMouse[i][j]['color'], highlight=True), end='')
                else:
                    print('   ', end='')
            print('', end='\n')


# testing
# if __name__ == '__main__':
#     env = ElasticMouseMazeEnv()
#     env.render(mode='color')
#     print('-----------------------------------------------------------')
#     dcd = env.decode()
#     env.step('N')
#     env.render(mode='color')
#     print('-----------------------------------------------------------')
#     env.encode(dcd[0], dcd[1], dcd[2], dcd[3], dcd[4])
#     env.render()
