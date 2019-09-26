# gym-mosuemaze

The [MouseMaze environment](https://github.com/AkasshShah/MouseMaze) is a domain featuring discrete state and action spaces.

## The setup

The mousemaze task initializes a single mouse agent, 2 shock-wire/traps and 2 cheese pieces/pizza slices in the maze.

## Mouse

The mouse agent is rewarded +10 for every cheese piece/pizza slice it lands on and eats. The mouse agent is rewarded -8 for every shock-wire/trap it lands on. The mouse agent is rewarded -1 for every move it takes that does not complete the episode or if the mouse does not land any anything in that step.

## Maze

The maze itself will be a 4x4 block-layout which will have walls between certain blocks. It's starting state might look like this:

![Image of Maze](https://github.com/AkasshShah/MouseMaze/gym-mousemaze/MouseMaze.png)

but it will render for console output.

# Installation

```bash
cd gym-mousemaze
pip install -e .
```
