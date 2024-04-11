# My search DFS and BFS

An implementation of the DFS and BFS algo.

## Usage

To use it, just clone the repo and run `main.py`

```bash
python3 main.py
```

or

```bash
python main.py
```

To run the DFS visualization, use the `Queue` class when calling the solve method in the `main.py` file. Example:

```python
from maze import Maze, Stack, Queue

maze = Maze("maze.txt")


maze.solve(Queue)

```

To run the BFS visualization, use the `Stack` class when calling the solve method in the `main.py` file. Example:

```python
from maze import Maze, Stack, Queue

maze = Maze("maze.txt")


maze.solve(Stack)

```

### Contributions are welcome, but this repo is mostly for my learning

.
