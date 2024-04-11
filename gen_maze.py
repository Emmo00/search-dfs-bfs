import random


def generate_maze(width=25, height=25):
    # Initialize the maze with walls
    maze = [["#" for _ in range(width)] for _ in range(height)]

    # Place the start and end points
    maze[0][0] = "A"
    maze[height - 1][width - 1] = "B"
    for i in range(height):
        for j in range(width):
            if i == j == 0:
                continue
            if i == height - 1 and j == width - 1:
                continue
            maze[i][j] = random.choice("##   ")

    maze = "\n".join(["".join(row) for row in maze])
    with open("maze.txt", "w") as f:
        f.write(maze)
