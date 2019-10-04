from gym.envs.registration import register
register(
    id='mm-v0',
    entry_point='gym_mousemaze.envs:MouseMazeEnv',
)
register(
    id='mm-v1',
    entry_point='gym_mousemaze.envs:ElasticMouseMazeEnv',
)
