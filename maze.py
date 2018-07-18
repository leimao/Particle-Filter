
import numpy as np 
import turtle

class Maze(object):

    def __init__(self, grid_height, grid_width, maze = None, num_rows = None, num_cols = None, wall_prob = None, random_seed = None):
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
        self.grid_height = grid_height
        self.grid_width = grid_width

        if maze is not None:
            self.maze = maze
            self.num_rows = maze.shape[0]
            self.num_cols = maze.shape[1]
            self.fix_maze_boundary()
            self.fix_wall_inconsistency()
        else:
            assert num_rows is not None and num_cols is not None and wall_prob is not None, 'Parameters for random maze should not be None.' 
            self.random_maze(num_rows = num_rows, num_cols = num_cols, wall_prob = wall_prob, random_seed = random_seed)

        self.height = self.num_rows * self.grid_height
        self.width = self.num_cols * self.grid_width

        self.turtle_registration()

    def turtle_registration(self):

        turtle.register_shape('tri', ((-3, -2), (0, 3), (3, -2), (0, 0)))

    def check_wall_inconsistency(self):

        wall_errors = list()

        # Check vertical walls
        for i in range(self.num_rows):
            for j in range(self.num_cols-1):
                if (self.maze[i,j] & 2 != 0) != (self.maze[i,j+1] & 8 != 0):
                    wall_errors.append(((i,j), 'v'))
        # Check horizonal walls
        for i in range(self.num_rows-1):
            for j in range(self.num_cols):
                if (self.maze[i,j] & 4 != 0) != (self.maze[i+1,j] & 1 != 0):
                    wall_errors.append(((i,j), 'h'))

        return wall_errors

    def fix_wall_inconsistency(self, verbose = True):
        '''
        Whenever there is a wall inconsistency, put a wall there.
        '''
        wall_errors = self.check_wall_inconsistency()

        if wall_errors and verbose:
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
        for i in range(self.num_rows):
            self.maze[i,0] |= 8
            self.maze[i,-1] |= 2
        for j in range(self.num_cols):
            self.maze[0,j] |= 1
            self.maze[-1,j] |= 4

    def random_maze(self, num_rows, num_cols, wall_prob, random_seed = None):

        if random_seed is not None:
            np.random.seed(0)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.maze = np.zeros((num_rows, num_cols), dtype = np.int8)
        for i in range(self.num_rows):
            for j in range(self.num_cols-1):
                if np.random.rand() < wall_prob:
                    self.maze[i,j] |= 2
        for i in range(self.num_rows-1):
            for j in range(self.num_cols):
                if np.random.rand() < wall_prob:
                    self.maze[i,j] |= 4

        self.fix_maze_boundary()
        self.fix_wall_inconsistency(verbose = False)

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

    def show_maze(self):

        turtle.setworldcoordinates(0, self.height * 1.005, self.width * 1.005, 0)

        wally = turtle.Turtle()
        wally.speed(0)
        wally.width(1.5)
        wally.hideturtle()
        turtle.tracer(0, 0)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
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


    def weight_to_color(self, weight):

        return "#%02x00%02x" % (int(weight * 255), int((1 - weight) * 255))


    def show_particles(self, particles):

        # Clear the particle stamps from the last update
        turtle.clearstamps()
        turtle.shape('tri')

        for particle in particles:
            turtle.setposition((particle.x, particle.y))
            turtle.setheading(90 + particle.heading)
            turtle.color(self.weight_to_color(particle.weight))
            turtle.stamp()

    def show_robot(self, robot):
        turtle.clearstamps()
        turtle.color("green")
        turtle.shape('turtle')
        turtle.shapesize(0.7, 0.7)
        turtle.setposition((robot.x, robot.y))
        turtle.setheading(90 + robot.heading)
        turtle.stamp()
        turtle.update()





class Particle(object):

    def __init__(self, x, y, heading = None, weight = 1, noisy = False):

        if heading is None:
            heading = np.random.uniform(0,360)

        self.x = x
        self.y = y
        self.heading = heading
        self.weight = weight

    @property
    def state(self):

        return (self.x, self.y, self.heading)

    def read_sensor(self, maze):

        return maze.distance_to_walls(coordinates = (self.x, self.y))

    '''
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    '''

    def try_move(self, speed, maze, noisy = False):

        heading = self.heading
        heading_rad = np.radians(heading)

        dx = np.sin(heading_rad) * speed
        dy = np.cos(heading_rad) * speed

        x = self.x + dx
        y = self.y + dy

        gj1 = int(self.x // maze.grid_width)
        gi1 = int(self.y // maze.grid_height)
        gj2 = int(x // maze.grid_width)
        gi2 = int(y // maze.grid_height)

        # Check if the particle is still in the maze
        if gi2 < 0 or gi2 >= maze.num_rows or gj2 < 0 or gj2 >= maze.num_cols:
            return False

        # Move in the same grid
        if gi1 == gi2 and gj1 == gj2:
            self.x = x
            self.y = y
            return True
        # Move across one grid vertically
        elif abs(gi1 - gi2) == 1 and abs(gj1 - gj2) == 0:
            if maze.maze[min(gi1, gi2), gj1] & 4 != 0:
                return False
            else:
                self.x = x
                self.y = y
                return True
        # Move across one grid horizonally
        elif abs(gi1 - gi2) == 0 and abs(gj1 - gj2) == 1:
            if maze.maze[gi1, min(gj1, gj2)] & 2 != 0:
                return False
            else:
                self.x = x
                self.y = y
                return True
        # Move across grids both vertically and horizonally
        elif abs(gi1 - gi2) == 1 and abs(gj1 - gj2) == 1:

            x0 = max(gj1, gj2) * maze.grid_width
            y0 = (y - self.y) / (x - self.x) * (x0 - self.x) + self.y

            if maze.maze[int(y0 // maze.grid_height), min(gj1, gj2)] & 2 != 0:
                return False

            y0 = max(gi1, gi2) * maze.grid_height
            x0 = (x - self.x) / (y - self.y) * (y0 - self.y) + self.x

            if maze.maze[min(gi1, gi2), int(x0 // maze.grid_width)] & 4 != 0:
                return False

            self.x = x
            self.y = y
            return True

        else:
            raise Exception('Unexpected collision detection.')



class Robot(Particle):

    def __init__(self, x, y, heading = None, speed = 0.3, noisy = False):

        super(Robot, self).__init__(x = x, y = y, heading = heading, noisy = noisy)
        self.step_count = 0
        self.noisy = noisy
        self.time_step = 0
        self.speed = speed

    def choose_random_direction(self):

        self.heading = np.random.uniform(0, 360)

    def add_sensor_noise(self, x):

        if not noisy:
            return x

        readings = list(x)
        for i in range(len(readings)):
            mu = readings[i]
            std = readings[i] * 0.05 / 2
            readings[i] = np.random.normal(mu, sigma)

        readings = tuple(readings)

        return readings

    def read_sensor(self, maze, add_noise):

        # Robot has error in reading the sensor while particles do not.
        readings = maze.distance_to_walls(coordinates = (self.x, self.y))
        readings_noisy = self.add_sensor_noise(x = readings)

        return readings_noisy

    def move(self, maze):


        while True:
            self.time_step += 1
            if self.try_move(speed = self.speed, maze = maze, noisy = False):
                break
            self.choose_random_direction()












if __name__ == '__main__':
    
    window = turtle.Screen()
    window.setup (width = 800, height = 800)

    #maze = np.array([[15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15],[15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15], [15,15,15,15,15,15,15,15]])
    #maze = np.array([[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15],[15,15,15,15,15]])
    #world = Maze(maze = maze, grid_height = 50, grid_width = 50)
    world = Maze(grid_height = 50, grid_width = 50, num_rows = 20, num_cols = 20, wall_prob = 0.4, random_seed = 0)

    x = np.random.uniform(0, world.width)
    y = np.random.uniform(0, world.height)
    bob = Robot(x = x, y = y)

    '''
    particles = list()
    for i in range(100):
        x = np.random.uniform(0, world.width)
        y = np.random.uniform(0, world.height)
        particles.append(Particle(x = x, y = y))
    '''
    world.show_maze()
    while True:
        world.show_robot(robot = bob)
        bob.move(maze = world)






    #world.show_particles(particles = particles)
    #window.exitonclick()











