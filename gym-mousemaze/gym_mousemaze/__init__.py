from gym.envs.registration import register
register(
    id='mm-v0',
    entry_point='gym_mousemaze.envs:MouseMazeEnv',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )
