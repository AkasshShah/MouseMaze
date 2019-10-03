# Using ```gym.make('gym_mousemaze:mm-v0')```

The [MouseMaze environment](https://github.com/AkasshShah/MouseMaze) is a domain featuring discrete state and action spaces.

## The Setup

First install the mousemaze environment as show [here](https://github.com/AkasshShah/MouseMaze/blob/master/gym-mousemaze/README.md).

Then follow the example as shown in the .py file/files on this level.

## Functions that can be accessed in this environment:
* ```step()```:
    * This function takes in one out of the following:
        * 'N'
        * 'S'
        * 'W'
        * 'E'
    * This function will return the following:
        * observation: This is an ```list``` of size 3
            * ```obs[0]``` will have the ```tuple``` of the current position of the mouse
            * ```obs[1]``` will have an ```array``` of the ```tuples``` of positions of the traps still remaining
            * ```obs[2]``` will have an ```array``` of the ```tuples``` of postions of the pizzas still remaining
        * reward: This is an ```int``` that essentially shows whether the mouse made a good move, not so good move and a bad move
        * done: This is a ```boolean``` that is ```True``` if there are no more pizzas on the map, else ```False```
    * The function will move the mouse in the direction specified
    * example:
        ```python
        obs, reward, done = env.step('N')
        ```
* ```encode()```:
    * This function takes in three values:
        * ```tuple``` of the position of the mouse
        * ```array``` of ```tuples``` of the positions of traps on the map
        * ```array``` of ```tupels``` of the positions of the pizzas on the map
    * This function returns nothing
    * This function tries to place the rewards first, then the traps and then the mouse. If an invalid position was given to place a trap, pizza or the mouse, it will not place it. 
* ```decode()```:
    * This array takes in no parameters
    * This function returns a ```list``` of size 3
        * ```dcd[0]``` will have the ```tuple``` of the current position of the mouse
        * ```dcd[1]``` will have an ```array``` of the ```tuples``` of positions of the traps still remaining
        * ```dcd[2]``` will have an ```array``` of the ```tuples``` of postions of the pizzas still remaining
    * The function traverses through the map to identify the traps, pizzas and the mouse, stores the values, and returns them
* ```reset()```:
    * This function takes in no parameters
    * This function returns nothing
    * This function **resets** the map to the original starting position
* ```rewardDictFunc()```:
    * This function takes in no parameters
    * This function returns a ```dictionary```, where the keys are the type of reward, and the ```values``` are the amount assigned for that type
    * This function returns stored values
* ```render()```:
    * This function takes in one parameter:
        * ```mode = ```
    * This function returns nothing
    * This function ```prints``` a visual map based on the ```mode```
        * If the parameter is set like this: ```env.render(mode = 'color')```
            * Then the map is printed as a $$7*7$$ grid, with each block colored according to what that block is
            * The rendering color sequence is as follows:
                * if block is mouse: color is white
                * if block is pizza: color is yellow
                * if block is trap: color is red
                * if block is wall: color is blue
                * if block is empty: color green
        * If the parameter is set like this: ```env.render(mode = 'text')```
            * The function is calls ```printMAP()```
* ```printMAP()```:
    * This function takes in no parameters
    * This function returns nothing
    This function traverses the map and prints out, in text, what each block is