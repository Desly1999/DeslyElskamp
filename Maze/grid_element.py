from functools import total_ordering
from pygame import draw
from Maze.helpers.directions import Direction


@total_ordering
class GridElement:
    """
    GridElement used as a tile in the maze
    """

    """
    Initialise the GridElement and assign the starting values
    """

    def __init__(self, x, y, size):
        self.position = (x, y)
        self.neighbours = [None, None, None, None]
        self.walls = [True, True, True, True]
        self.generate_walls()
        self.is_visited = False
        self.is_seen = False
        self.is_marked = False
        self.size = (size[0], size[1])
        self.parent = None
        self.fscore = 0
        self.gscore = 999999
        self.score = self.fscore + self.gscore

    """
    Overload the equals operator
    """

    def __eq__(self, other):
        return self.position == other.position


    """
    Overload the less than operator
    """

    def __lt__(self, other):
        return self.score < other.score


    """
    Overload the string representation of the object
    """

    def __repr__(self):
        return "[%s, %s]" % (self.position, self.score)



    """
    Set a wall in all directions
    """

    def generate_walls(self):
        for direction in Direction:
            self.walls[direction.value] = True

    """
    Set the neighbours in all directions to None
    """

    def reset_neighbours(self):
        for direction in Direction:
            self.neighbours[direction.value] = None

    """
    Sets all but the neighbours value back to their starting value
    """

    def reset(self):
        self.generate_walls()
        self.reset_state()

    """
    Sets the state of the GridElement 
    """

    def reset_state(self):
        self.is_marked = False
        self.is_visited = False
        self.is_seen = False
        self.parent = None
        self.fscore = 0
        self.score = self.fscore + self.gscore

    def unvisited_neighbours(self):
        neighbors = []
        for direction in Direction:
            next_element = self.neighbours[direction]
            if next_element is not None:
                if not next_element.is_visited and not self.walls[direction]:
                    neighbors.append(next_element)
        return neighbors

    """
     Method to calculate the Manhattan distance from a certain 
     GridElement to another GridElement of the maze
     """

    def manhattan_distance(self, other):
        x_distance = abs(self.position[0] - other.position[0])
        y_distance = abs(self.position[1] - other.position[1])
        return x_distance + y_distance

    def set_score(self, score):
        self.score = score

    def update_gscore(self, target):
        self.gscore = self.manhattan_distance(target)
        self.score = self.fscore + self.gscore

    def update_fscore(self, fscore):
        self.fscore = fscore
        self.score = self.fscore + self.gscore

    def update_score(self):
        self.score = self.fscore + self.gscore

    """
    Remove the wall in a given direction while 
    also removing the wall in the adjacent neighour GridElement  
    """

    def remove_wall(self, direction):
        if self.neighbours[direction] is not None:
            self.walls[direction] = False
            self.neighbours[direction].walls[(direction + 2) % 4] = False
            # self.print_walls()
            # self.neighbours[direction].print_walls()

    def add_wall(self, direction):
        if self.neighbours[direction] is not None:
            self.walls[direction] = True
            self.neighbours[direction].walls[(direction + 2) % 4] = True
            # self.print_walls()
            # self.neighbours[direction].print_walls()

    def print_walls(self):
        print(self.position)
        for identifier, walls in enumerate(self.walls):
            print(Direction(identifier), self.walls[Direction(identifier)])

    # TODO: Pythonify this!
    """
    Returns position
    """

    def get_position(self):
        return self.position

    def get_position_x(self):
        return self.position[0]

    def get_position_y(self):
        return self.position[1]

    """
    Assign the GridElement used to reach this GridElement
    """

    def set_parent(self, parent):
        self.parent = parent

    """
    Draw the GridElement
    """

    def draw_grid_element(self, surface):
        if self.is_visited or self.is_seen:
            draw.rect(surface, (200, 200, 200),
                      (self.position[0] * self.size[0], self.position[1] * self.size[1], self.size[0], self.size[1]), 0)
        if self.is_marked:
            draw.circle(surface, (0, 255, 0), ((int(self.position[0] * self.size[0] + self.size[0] / 2)),
                                               int(self.position[1] * self.size[1] + self.size[0] / 2)),
                        (int(self.size[0] / 2)), 0)
        if self.walls[Direction.NORTH] is True:
            draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                      ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]), 2)
        if self.walls[Direction.EAST] is True:
            draw.line(surface, (0, 0, 0), ((self.position[0] + 1) * self.size[0], self.position[1] * self.size[1]),
                      ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
        if self.walls[Direction.SOUTH] is True:
            draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]),
                      ((self.position[0] + 1) * self.size[0], (self.position[1] + 1) * self.size[1]), 2)
        if self.walls[Direction.WEST] is True:
            draw.line(surface, (0, 0, 0), (self.position[0] * self.size[0], self.position[1] * self.size[1]),
                      (self.position[0] * self.size[0], (self.position[1] + 1) * self.size[1]), 2)

    def print_neighbour_position(self):
        for identifier, neighbour in enumerate(self.neighbours):
            if neighbour is None:
                print(Direction(identifier), "None")
            else:
                print(Direction(identifier), neighbour.get_position())
