import random
from datetime import datetime
from Maze.helpers.constants import Constants
from Maze.grid_element import GridElement
from Maze.helpers.directions import Direction
import bisect


class Maze:
    """
    Generates a grid based maze based on GridElements
    This class also contains search algorithms for
    depth first, breath first, greedy and A* star search to
    solve the generated mazes
    """

    def __init__(self, grid_size_x, grid_size_y, screen_size):
        self.grid_size = (grid_size_x, grid_size_y)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.grid = [[GridElement(x, y, (screen_size[0] / grid_size_x, screen_size[1] / grid_size_y)) for y in
                      range(self.grid_size_y)] for x in range(self.grid_size_x)]
        self.init_grid()
        self.target = self.grid[-1][-1]
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                self.grid[x][y].update_gscore(self.target)

    """
    Initializes the grid with which the maze will be generated
    and links the correct GridElement cells with each other  
    """

    def init_grid(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                self.grid[x][y].reset()
                if x > 0:
                    self.grid[x][y].neighbours[Direction.WEST] = self.grid[x - 1][y]
                if x < self.grid_size_x - 1:
                    self.grid[x][y].neighbours[Direction.EAST] = self.grid[x + 1][y]
                if y > 0:
                    self.grid[x][y].neighbours[Direction.NORTH] = self.grid[x][y - 1]
                if y < self.grid_size_y - 1:
                    self.grid[x][y].neighbours[Direction.SOUTH] = self.grid[x][y + 1]

    """
    Resets the GridElements of the maze
    """

    def reset_maze(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                self.grid[x][y].reset()

    """
    Resets the state of the GridElements of the maze
    """

    def reset_grid_elements(self):
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                self.grid[x][y].reset_state()

    """
    Draw every GridElement in the maze
    """

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                element.draw_grid_element(surface)

    def breadth_first_solution(self):

        # reset the grid elements
        self.reset_grid_elements()
        # select the starting point, and mark it as visited
        start = self.grid[0][0]
        start.is_visited = True
        queue = [start]

        # while there are elements to explore
        while len(queue) > 0:
            # the current element is the first element of the queue
            current_element = queue.pop(0)
            # if  you did not find the target
            if current_element != self.target:
                random.shuffle(current_element.unvisited_neighbours())
                # for all unvisited neighbours, marks them as visited, set their parent and add them to the queue
                for next_element in current_element.unvisited_neighbours():
                    next_element.is_visited = True
                    next_element.set_parent(current_element)
                    queue.append(next_element)
            else:
                # otherwise (target was found), leave the loop
                break

        # If the target was found, compute the path, back to front.
        print("Done")
        if current_element == self.target:
            length = 0
            while current_element is not None:
                current_element.is_marked = True
                current_element = current_element.parent
                length += 1
            print("Path length is: {}".format(length))

    def depth_first_solution(self):

        # reset the grid elements
        self.reset_grid_elements()
        # select the starting point, and mark it as visited
        start = self.grid[0][0]
        start.is_visited = True
        stack = [start]

        # while there are elements to explore
        while len(stack) > 0:
            # the current element is the last element of the stack
            current_element = stack[-1]
            # if  you did not find the target
            if current_element != self.target:
                # get all unvisited neighbours
                possible_neighbors = current_element.unvisited_neighbours()
                # if there are none, pop the last element from the stack
                if len(possible_neighbors) == 0:
                    stack.pop()
                else:
                    # otherwise pick a random unvisited neighbour, update its parent, set to visited and add it to stack
                    # For [0] it prefers to go up, then right, then down and last left. For [-1] it is reversed.
                    next_element = possible_neighbors[0]

                    next_element.set_parent(current_element)
                    next_element.is_visited = True
                    stack.append(next_element)
            else:
                # otherwise (target was found), leave the loop
                break

        # If the target was found, compute the path, back to front.
        if current_element == self.target:
            length = 0
            while current_element is not None:
                current_element.is_marked = True
                current_element = current_element.parent
                length += 1
            print("Path length is: {}".format(length))

    def greedy_search(self):

        # reset the grid elements
        self.reset_grid_elements()
        # select the starting point, and mark it as visited
        start = self.grid[0][0]
        start.is_visited = True
        sorted_list = [start]

        # while there are elements to explore
        while len(sorted_list) > 0:
            # the current element is the first element of the queue
            current_element = sorted_list.pop(0)
            # if  you did not find the target
            if current_element != self.target:
                # for all unvisited neighbours, mark them as visited, set their parent
                # and add them to the queue in the right place
                for next_element in current_element.unvisited_neighbours():
                    next_element.is_visited = True
                    next_element.set_parent(current_element)
                    bisect.insort_right(sorted_list, next_element)

            else:
                # otherwise (target was found), leave the loop
                break

            # If the target was found, compute the path, back to front.
        print("Done")
        if current_element == self.target:
            length = 0
            while current_element is not None:
                current_element.is_marked = True
                current_element = current_element.parent
                length += 1
            print("Path length is: {}".format(length))
        pass

    def a_star_search(self):

        # reset the grid elements
        self.reset_grid_elements()
        # select the starting point, and mark it as visited
        start = self.grid[0][0]
        start.is_seen = True
        # set the fscore to 0 at the start
        start.update_fscore(0)
        sorted_list = [start]

        # while there are elements to explore
        while len(sorted_list) > 0:
            # the current element is the first element of the queue
            current_element = sorted_list.pop(0)
            # if  you did not find the target
            if current_element != self.target:
                # for all unvisited neighbours
                for next_element in current_element.unvisited_neighbours():
                    # if the next_element is not seen yet
                    # mark as visited, update fscore, set their parent and add them to the list at the right place
                    if not next_element.is_seen:
                        next_element.is_seen = True
                        next_element.update_fscore(current_element.fscore + 1)
                        next_element.set_parent(current_element)
                        bisect.insort_left(sorted_list, next_element)
                    # if the element is seen before and the current situation is better
                    elif current_element.score < next_element.score:
                        # if the next_element is in sorted_list, delete the next_element
                        if next_element in sorted_list:
                            sorted_list.remove(next_element)
                        # mark as visited, update fscore, set their parent and add them to the list at the right place
                        next_element.is_seen = True
                        next_element.update_fscore(current_element.fscore + 1)
                        next_element.set_parent(current_element)
                        bisect.insort_left(sorted_list, next_element)

            else:
                # otherwise (target was found), leave the loop
                break

        # If the target was found, compute the path, back to front.
        print("Done")
        if current_element == self.target:
            length = 0
            while current_element is not None:
                current_element.is_marked = True
                current_element = current_element.parent
                length += 1
            print("Path length is: {}".format(length))
        pass

    """
     Generate the maze based on depth first search 
     """

    def generate_maze(self):
        random.seed(datetime.now())
        self.reset_maze()
        stack = [self.grid[0][0]]
        while len(stack) > 0:
            current_element = stack[-1]
            current_element.is_visited = True

            possible_directions = []
            for direction in Direction:
                next_element = current_element.neighbours[direction]
                if next_element is not None:
                    if not next_element.is_visited:
                        possible_directions.append(direction)
            if len(possible_directions) == 0:
                stack.pop()
                continue

            next_direction = random.choice(possible_directions)
            current_element.remove_wall(next_direction)
            next_element = current_element.neighbours[next_direction]
            stack.append(next_element)

        self.reset_grid_elements()

        removed_walls = 0
        while removed_walls < Constants.WALLS_TO_REMOVE:
            random.choice(random.choice(self.grid)).remove_wall(random.choice(list(Direction)))
            removed_walls += 1

    def open_maze(self):
        for x in range(0, self.grid_size_x):
            for y in range(0, self.grid_size_y):
                for direction in Direction:
                    self.grid[x][y].remove_wall(direction)

    def generate_room(self):
        """Generates rooms, with specific positions."""
        self.reset_maze()
        self.open_maze()

        for x in range(self.grid_size_x // 4 + 2, self.grid_size_x // 2 + 1):
            self.grid[x][self.grid_size_y // 4].add_wall(Direction.NORTH)

        for y in range(self.grid_size_y // 4 + 2, self.grid_size_y // 2 + 1):
            self.grid[self.grid_size_x // 4][y].add_wall(Direction.WEST)

        for x in range(0, self.grid_size_x // 2 - 1):
            self.grid[x][self.grid_size_y // 2].add_wall(Direction.SOUTH)

        for x in range(self.grid_size_x // 2 + 1, self.grid_size_x):
            self.grid[x][self.grid_size_y // 2].add_wall(Direction.SOUTH)

        for y in range(0, self.grid_size_y // 2 - 2):
            self.grid[self.grid_size_x // 2][y].add_wall(Direction.EAST)

        for y in range(self.grid_size_y // 2 + 3, self.grid_size_y):
            self.grid[self.grid_size_x // 2][y].add_wall(Direction.EAST)

        for x in range(3 * self.grid_size_x // 4, self.grid_size_x):
            self.grid[x][self.grid_size_y // 4].add_wall(Direction.SOUTH)

        for y in range(0, self.grid_size_y // 4):
            self.grid[3 * self.grid_size_x // 4][y].add_wall(Direction.WEST)

        for x in range(self.grid_size_x // 8, 3 * self.grid_size_x // 4 + 1):
            self.grid[x][3 * self.grid_size_y // 4].add_wall(Direction.NORTH)

        for y in range(3 * self.grid_size_y // 4, self.grid_size_y - 1):
            self.grid[3 * self.grid_size_x // 4][y].add_wall(Direction.EAST)

        for y in range(3 * self.grid_size_y // 4, self.grid_size_y - 5):
            self.grid[self.grid_size_x // 8][y].add_wall(Direction.WEST)

        for y in range(self.grid_size_y - 3, self.grid_size_y):
            self.grid[self.grid_size_x // 8][y].add_wall(Direction.WEST)

    def generate_obstacles(self):
        """Generate a Manhattan like grid, with a few road blocks"""

        self.reset_maze()
        self.open_maze()

        for n in range(0, self.grid_size_x // 5):
            for m in range(0, self.grid_size_y // 5):
                for x in range(n * 5 + 1, n * 5 + 4):
                    self.grid[x][m * 5 + 1].add_wall(Direction.NORTH)
                    self.grid[x][m * 5 + 4].add_wall(Direction.NORTH)
                for y in range(m * 5 + 1, m * 5 + 4):
                    self.grid[n * 5][y].add_wall(Direction.EAST)
                    self.grid[n * 5 + 4][y].add_wall(Direction.WEST)

        # vertical blocks
        block_x = 5 * random.randrange(0, self.grid_size_x // 5) + 2
        self.grid[block_x][0].add_wall(Direction.EAST)
        for m in range(1, self.grid_size_y // 5 - 1):
            block_x = 5 * random.randrange(0, self.grid_size_x // 5) + 2
            self.grid[block_x][m * 5 + 4].add_wall(Direction.EAST)
            self.grid[block_x][m * 5 + 5].add_wall(Direction.EAST)
        block_x = 5 * random.randrange(0, self.grid_size_x // 5) + 2
        self.grid[block_x][self.grid_size_y - 1].add_wall(Direction.EAST)

        # horizontal blocks
        block_y = 5 * random.randrange(0, self.grid_size_y // 5) + 2
        self.grid[0][block_y].add_wall(Direction.NORTH)
        for n in range(1, self.grid_size_x // 5 - 1):
            block_y = 5 * random.randrange(0, self.grid_size_y // 5) + 2
            self.grid[n * 5 + 4][block_y].add_wall(Direction.NORTH)
            self.grid[n * 5 + 5][block_y].add_wall(Direction.NORTH)
        block_y = 5 * random.randrange(0, self.grid_size_y // 5) + 2
        self.grid[self.grid_size_x - 1][block_y].add_wall(Direction.NORTH)
