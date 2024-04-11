import os
from time import sleep


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def __repr__(self):
        return f"<Node {self.action}, {self.action}, {self.action}>"


class Stack:
    def __init__(self):
        self.frontier = []

    def add(self, item):
        self.frontier.append(item)

    def contains_state(self, node):
        return any([n.state == node.state for n in self.frontier])

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("Frontier is empty")
        item = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return item

    def length(self):
        return len(self.frontier)


class Queue(Stack):
    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("Frontier is empty")
        item = self.frontier[0]
        self.frontier = self.frontier[1:]
        return item


class Maze:
    def __init__(self, file):
        self.maze_file_content = ""
        self.maze_walls = []
        self.start = tuple()
        self.goal = tuple()
        self.solution = []
        self.print_buf = []
        with open(file, "r") as f:
            self.maze_file_content = f.read()
        if (
            "A" not in self.maze_file_content
            and len(self.maze_file_content.split("A")) != 2
        ):
            raise Exception("Maze must have one starting point")
        if (
            "B" not in self.maze_file_content
            and len(self.maze_file_content.split("B")) != 2
        ):
            raise Exception("Maze must have a goal")
        self.parse_file()

    def clear_solution(self):
        self.solution = []
        self.print_buff = []

    def parse_file(self):
        rows = self.maze_file_content.split("\n")
        self.height = len(rows)
        self.width = max(len(list(row)) for row in rows)
        row_walls = []
        for i, row in enumerate(rows):
            cols = list(row)
            col_walls = []
            for j, col in enumerate(cols):
                if col == "#":
                    col_walls.append(True)
                elif col == " ":
                    col_walls.append(False)
                elif col == "A":
                    col_walls.append(False)
                    self.start = (i, j)
                elif col == "B":
                    col_walls.append(False)
                    self.goal = (i, j)
                else:
                    raise Exception(f"Invalid Maze Pixel: {col}")
            row_walls.append(col_walls)
        self.maze_walls = row_walls

    def print(self):
        optimal_path = self.optimal_path()
        map = ""
        for i, row in enumerate(self.maze_walls):
            for j, pixel in enumerate(row):
                if pixel:
                    map = map + "#"
                elif (i, j) == self.start:
                    map = map + "A"
                elif (i, j) == self.goal:
                    map = map + "B"
                elif optimal_path and any(
                    node.state == (i, j) for node in optimal_path
                ):
                    map = map + "\033[92m*\033[0m"
                elif self.solution and any(
                    node.state == (i, j) for node in self.solution
                ):
                    map = map + "\033[91m*\033[0m"
                else:
                    map = map + (" ")
            map = map + "\n"
        return map


    def neighbors(self, node: Node) -> list[Node]:
        x, y = node.state
        neighbors = [
            Node((x, y + 1), node, ""),
            Node((x, y - 1), node, ""),
            Node((x - 1, y), node, ""),
            Node((x + 1, y), node, ""),
        ]
        valid_neighbors = []
        for neighbor in neighbors:
            (x, y) = neighbor.state
            if x < 0 or x > self.height - 1:
                continue
            if (y < 0) or (y > self.width - 1):
                continue
            if self.maze_walls[x][y]:
                continue
            if any([(x, y) == n.state for n in self.explored]):
                continue
            valid_neighbors.append(neighbor)
        return valid_neighbors

    def solve(self, Frontier=Stack):
        frontier = Frontier()
        self.explored = set()

        start_node = Node(self.start, None, None)
        frontier.add(start_node)
        while not frontier.empty():
            node = frontier.remove()
            if node.state == self.goal:
                self.fin_print()
                return True
            self.explored.add(node)
            self.solution.append(node)
            self.print_buf.append(self.print())
            for child in self.neighbors(node):
                if not frontier.contains_state(child):
                    frontier.add(child)
        self.fin_print()
        return False

    def fin_print(self):
        for frame in self.print_buf:
            os.system("cls")
            print(frame)
            sleep(0.011)

    def optimal_path(self):
        goal = self.solution[-1]
        o_path = [goal]
        for node in reversed(
            self.solution[:-1]
        ):  
            g_x, g_y = goal.state
            x, y = node.state
            if (x == g_x - 1 or x == g_x + 1 or x == g_x) and (
                y == g_y - 1 or y == g_y + 1 or y == g_y
            ):
                o_path.insert(0, node)
                goal = node
        return o_path
