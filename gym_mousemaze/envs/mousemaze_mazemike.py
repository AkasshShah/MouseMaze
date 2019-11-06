import gym
from gym import utils
from gym.utils import seeding
from six import StringIO

p = {'name': 'pizza', 'color': 'yellow'}
t = {'name': 'trap', 'color': 'red'}
m = {'name': 'mouse', 'color': 'white'}
w = {'name': 'wall', 'color': 'blue'}
x = {'name': 'empty', 'color': 'clear'}
v = {'name': 'void', 'color': 'clear'}


class MazeMike(gym.Env):
    def __init__(self):
        self.MAPwithMouse = []
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.numberOfWalls = 0
        self.rewardDict = self.rewardDictFunc()
        self.actionSpace = ['N', 'S', 'W', 'E']
        self.reset()

    def rewardDictFunc(self):
        rewardDict = {
            'wall': -7,
            'trap': -8,
            'normal': -1,
            'pizza': 25
        }
        return(rewardDict)

    def initMap(self, side):
        self.MAPwithMouse = []
        for yy in range(side):
            new = []
            for xx in range(side):
                new.append(x)
            self.MAPwithMouse.append(new)

    def setMapBlock(self, xx, yy, thing):
        if xx < len(self.MAPwithMouse) and yy < len(self.MAPwithMouse[0]):
            self.MAPwithMouse[yy][xx] = thing
            return True
        return False

    def encode(self, sqn, mTup, arrTrapTup, arrRewTup, arrWallTup):
        self.numberOfPizzasRemaining = 0
        self.numberOfTrapsRemaining = 0
        self.numberOfWalls = 0
        self.initMap(sqn)
        for trap in arrTrapTup:
            if self.setMapBlock(trap[0], trap[1], t):
                self.numberOfTrapsRemaining += 1
        for rew in arrRewTup:
            if self.setMapBlock(rew[0], rew[1], p):
                self.numberOfPizzasRemaining += 1
        for wall in arrWallTup:
            if self.setMapBlock(wall[0], wall[1], w):
                self.numberOfWalls += 1
        if self.setMapBlock(mTup[0], mTup[1], m):
            return True
        return False

    def reset(self):
        side = 5
        mousePos = (0, 2)
        trapArr = [(0, 1)]
        rewArr = [(0, 0)]
        wallArr = [(2, 2), (2, 1), (4, 3)]
        self.encode(side, mousePos, trapArr, rewArr, wallArr)

    def getMapBlock(self, xx, yy):
        return(self.MAPwithMouse[yy][xx])

    def decode(self):
        arrTrap = []
        arrRew = []
        mousePos = (-1, -1)
        arrWall = []
        for yy in range(len(self.MAPwithMouse)):
            for xx in range(len(self.MAPwithMouse[yy])):
                currBlock = self.getMapBlock(xx, yy)
                if currBlock == t:
                    arrTrap.append((xx, yy))
                elif currBlock == p:
                    arrRew.append((xx, yy))
                elif currBlock == w:
                    arrWall.append((xx, yy))
                elif currBlock == m:
                    mousePos = (xx, yy)
        return((len(self.MAPwithMouse), mousePos, arrRew, arrTrap, arrWall))

    def getMousePos(self):
        for yy in range(len(self.MAPwithMouse)):
            for xx in range(len(self.MAPwithMouse[yy])):
                if(self.MAPwithMouse[yy][xx] == m):
                    return((xx, yy))

    def wantsToGoOutOfBounds(self, amnt, VorH):
        currMousePos = self.getMousePos()
        currX = currMousePos[0]
        currY = currMousePos[1]
        if(VorH == 'V'):
            return(currY + amnt < 0 or currY + amnt >= len(self.MAPwithMouse))
        elif(VorH == 'H'):
            return(currX + amnt < 0 or currX + amnt >= len(self.MAPwithMouse))

    def moveEastWest(self, amnt):
        OrgMousePos = self.getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if(not self.wantsToGoOutOfBounds(amnt, 'H')):
            if(self.getMapBlock(OrgMousePosX+amnt, OrgMousePosY) != w):
                if(self.getMapBlock(OrgMousePosX+(amnt), OrgMousePosY) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(amnt), OrgMousePosY, m)
                elif(self.getMapBlock(OrgMousePosX+(amnt), OrgMousePosY) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(amnt), OrgMousePosY, m)
                elif(self.getMapBlock(OrgMousePosX+(amnt), OrgMousePosY) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX+(amnt), OrgMousePosY, m)
            else:
                rewardUpdate += self.rewardDict['wall']
                rtnIssue = 'wall'
        else:
            rewardUpdate += self.rewardDict['wall']
            rtnIssue = 'wall'
        return(self.decode(), rewardUpdate, done)

    def moveNorthSouth(self, amnt):
        OrgMousePos = self.getMousePos()
        OrgMousePosX = OrgMousePos[0]
        OrgMousePosY = OrgMousePos[1]
        done = False
        rtnIssue = ''
        rewardUpdate = 0
        if not self.wantsToGoOutOfBounds(amnt, 'V'):
            if(self.getMapBlock(OrgMousePosX, OrgMousePosY+amnt) != w):
                if(self.getMapBlock(OrgMousePosX, OrgMousePosY+(amnt)) == x):
                    rewardUpdate += self.rewardDict['normal']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(amnt), m)
                elif(self.getMapBlock(OrgMousePosX, OrgMousePosY+(amnt)) == t):
                    rewardUpdate += self.rewardDict['trap']
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(amnt), m)
                elif(self.getMapBlock(OrgMousePosX, OrgMousePosY+(amnt)) == p):
                    rewardUpdate += self.rewardDict['pizza']
                    self.numberOfPizzasRemaining -= 1
                    if(self.numberOfPizzasRemaining == 0):
                        done = True
                    self.setMapBlock(OrgMousePosX, OrgMousePosY, x)
                    self.setMapBlock(OrgMousePosX, OrgMousePosY+(amnt), m)
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
        strIniWall = '   ' * (len(self.MAPwithMouse) + 2)
        print(utils.colorize(strIniWall, w['color'], highlight=True), end='\n')
        for i in range(len(self.MAPwithMouse)):
            print(utils.colorize('   ', w['color'], highlight=True), end='')
            for j in range(len(self.MAPwithMouse[i])):
                if(self.MAPwithMouse[i][j]['color'] != 'clear'):
                    print(utils.colorize(
                        '   ', self.MAPwithMouse[i][j]['color'], highlight=True), end='')
                else:
                    print('   ', end='')
            print(utils.colorize('   ', w['color'], highlight=True), end='')
            print('', end='\n')
        print(utils.colorize(strIniWall, w['color'], highlight=True), end='\n')

    def step(self, action):
        if action == 'N' or action == 0:
            return(self.moveNorthSouth(-1))
        elif action == 'S' or action == 1:
            return(self.moveNorthSouth(1))
        elif action == 'W' or action == 2:
            return(self.moveEastWest(-1))
        elif action == 'E' or action == 3:
            return(self.moveEastWest(1))


# # testing
# if __name__ == '__main__':
#     env = MazeMike()
#     env.render(mode='color')
#     print('-----------------------------------------------------------')
#     dcd = env.decode()
#     env.step('E')
#     env.render(mode='color')
#     print('-----------------------------------------------------------')
#     env.encode(dcd[0], dcd[1], dcd[2], dcd[3], dcd[4])
#     env.render()
