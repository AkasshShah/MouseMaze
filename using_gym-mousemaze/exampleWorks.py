import gym
if __name__ == '__main__':
    env = gym.make('gym_mousemaze:mm-v1')
    if(env.encode(3, (0, 0), [(1, 1), (2, 2)], [(0, 1), (1, 0)], [((0, 0), (0, 1))])):
        env.render()
