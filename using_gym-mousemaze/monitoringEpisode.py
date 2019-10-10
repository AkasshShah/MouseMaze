import gym
import random
if __name__ == '__main__':
    env = gym.make('gym_mousemaze:mm-v1')
    if(env.encode(3, (0, 0), [(1, 1), (2, 2)], [(0, 1), (1, 0)], [((0, 0), (0, 1))])):
        batchSize = 16
        # env.render()
        episodes = []
        possibleMoves = ['N', 'S', 'W', 'E']
        done = False
        for i in range(batchSize):
            episode = []
            done = False
            env.encode(3, (0, 0), [(1, 1), (2, 2)], [
                       (0, 1), (1, 0)], [((0, 0), (0, 1))])
            while(not done):
                randMove = possibleMoves[random.randint(0, 3)]
                obs, reward, done = env.step(randMove)
                stepp = (obs, reward, done)
                episode.append(stepp)
            episodes.append(episode)
        # rendering
        for i in episodes:
            for steppp in i:
                enc = steppp[0]
                env.encode(enc[0], enc[1], enc[2], enc[3], enc[4])
                env.render()
                print("-----------------------------------------------")
            print("-----------------------------------------------")
