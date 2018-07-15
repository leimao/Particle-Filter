
import numpy as np 
import turtle





class Maze(object):

    def __init__(self, maze, grid_height, grid_width):
        '''
        maze: 2D numpy array. 
        passages are coded as a 4-bit number, with a bit value taking 
        0 if there is a wall and 1 if there is no wall. 
        The 1s register corresponds with a square's top edge, 
        2s register the right edge,
        4s register the bottom edge, 
        and 8s register the left edge. 
        (numpy array)
        '''
        self.maze = maze
        self.height = maze.shape[0]
        self.width = maze.shape[1]
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.fix_maze_boundary()
        self.fix_wall_inconsistency()

        #https://docs.python.org/3.0/library/turtle.html#turtle.setworldcoordinates
        turtle.setworldcoordinates(0, self.height * self.grid_height * 1.005, self.width * self.grid_width * 1.005, 0)

    def check_wall_inconsistency(self):

        wall_errors = list()

        # Check vertical walls
        for i in range(self.height):
            for j in range(self.width-1):
                if (self.maze[i,j] & 2 != 0) != (self.maze[i,j+1] & 8 != 0):
                    wall_errors.append(((i,j), 'v'))
        # Check horizonal walls
        for i in range(self.height-1):
            for j in range(self.width):
                if (self.maze[i,j] & 4 != 0) != (self.maze[i+1,j] & 1 != 0):
                    wall_errors.append(((i,j), 'h'))

        return wall_errors

    def fix_wall_inconsistency(self):
        '''
        Whenever there is a wall inconsistency, put a wall there.
        '''
        wall_errors = self.check_wall_inconsistency()

        if wall_errors:
            print('Warning: maze contains wall inconsistency.')

        for (i,j), error in wall_errors:
            if error == 'v':
                self.maze[i,j] |= 2
                self.maze[i,j+1] |= 8
            elif error == 'h':
                self.maze[i,j] |= 4
                self.maze[i+1,j] |= 1
            else:
                raise Exception('Unknown type of wall inconsistency.')
        return

    def fix_maze_boundary(self):
        '''
        Make sure that the maze is bounded.
        '''
        for i in range(self.height):
            self.maze[i,0] |= 8
            self.maze[i,-1] |= 2
        for j in range(self.width):
            self.maze[0,j] |= 1
            self.maze[-1,j] |= 4

    def permissibilities(self, cell):
        '''
        Check if the directions of a given cell are permissible.
        Return:
        (up, right, down, left)
        '''
        cell_value = self.maze[tuple(cell)]
        return (cell_value & 1 == 0, cell_value & 2 == 0, cell_value & 4 == 0, cell_value & 8 == 0)

    def distance_to_walls(self, coordinates):
        '''
        Measure the distance of coordinates to nearest walls at four directions.
        Return:
        (up, right, down, left)
        '''

        x, y = coordinates

        i = y // self.grid_height
        j = x // self.grid_width
        d1 = y - y // self.grid_height * self.grid_height
        while self.permissibilities(cell = (i,j))[0]:
            i -= 1
            d1 += self.grid_height

        i = y // self.grid_height
        j = x // self.grid_width
        d2 = self.grid_width - (x - x // self.grid_width * self.grid_width)
        while self.permissibilities(cell = (i,j))[1]:
            j += 1
            d2 += self.grid_width

        i = y // self.grid_height
        j = x // self.grid_width
        d3 = self.grid_height - (y - y // self.grid_height * self.grid_height)
        while self.permissibilities(cell = (i,j))[2]:
            i += 1
            d3 += self.grid_height

        i = y // self.grid_height
        j = x // self.grid_width
        d4 = x - x // self.grid_width * self.grid_width
        while self.permissibilities(cell = (i,j))[3]:
            j -= 1
            d4 += self.grid_width

        return (d1, d2, d3, d4)

    def show(self):

        wally = turtle.Turtle()
        wally.speed(0)
        wally.width(1.5)
        wally.hideturtle()
        turtle.tracer(0, 0)


        for i in range(self.height):
            for j in range(self.width):
                permissibilities = self.permissibilities(cell = (i,j))
                turtle.up()
                wally.setposition((j * self.grid_width, i * self.grid_height))
                # Set turtle heading orientation
                # 0 - east, 90 - north, 180 - west, 270 - south
                wally.setheading(0)
                if not permissibilities[0]:
                    wally.down()
                else:
                    wally.up()
                wally.forward(self.grid_width)
                wally.setheading(90)
                wally.up()
                if not permissibilities[1]:
                    wally.down()
                else:
                    wally.up()
                wally.forward(self.grid_height)
                wally.setheading(180)
                wally.up()
                if not permissibilities[2]:
                    wally.down()
                else:
                    wally.up()
                wally.forward(self.grid_width)
                wally.setheading(270)
                wally.up()
                if not permissibilities[3]:
                    wally.down()
                else:
                    wally.up()
                wally.forward(self.grid_height)
                wally.up()




if __name__ == '__main__':
    
    window = turtle.Screen()
    window.setup (width = 600, height = 600)

    maze = np.array([[15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15],[15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15]])
    #maze = np.array([[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15]])
    world = Maze(maze = maze, grid_height = 50, grid_width = 50)
    world.show()
    window.exitonclick()











