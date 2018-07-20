
import numpy as np 
import turtle
import argparse
import time

from maze import Maze, Particle, Robot, WeightedDistribution, weight_gaussian_kernel

def main(window_width, window_height, num_particles, sensor_limit_ratio, grid_height, grid_width, num_rows, num_cols, wall_prob, random_seed, robot_speed, kernel_sigma, particle_show_frequency):

    sensor_limit = sensor_limit_ratio * max(grid_height * num_rows, grid_width * num_cols)

    window = turtle.Screen()
    window.setup (width = window_width, height = window_height)

    world = Maze(grid_height = grid_height, grid_width = grid_width, num_rows = num_rows, num_cols = num_cols, wall_prob = wall_prob, random_seed = random_seed)

    x = np.random.uniform(0, world.width)
    y = np.random.uniform(0, world.height)
    bob = Robot(x = x, y = y, maze = world, speed = robot_speed, sensor_limit = sensor_limit)

    particles = list()
    for i in range(num_particles):
        x = np.random.uniform(0, world.width)
        y = np.random.uniform(0, world.height)
        particles.append(Particle(x = x, y = y, maze = world, sensor_limit = sensor_limit))

    world.show_maze()

    time.sleep(5)
    
    while True:

        readings_robot = bob.read_sensor(maze = world)

        particle_weight_total = 0
        for particle in particles:
            readings_particle = particle.read_sensor(maze = world)
            particle.weight = weight_gaussian_kernel(x1 = readings_robot, x2 = readings_particle, std = kernel_sigma)
            particle_weight_total += particle.weight

        world.show_robot(robot = bob)
        world.show_particles(particles = particles, show_frequency = particle_show_frequency)
        world.show_robot(robot = bob)
        world.show_estimated_location(particles = particles)
        world.clear_objects()

        # Make sure normalization is not divided by zero
        if particle_weight_total == 0:
            particle_weight_total = 1e-8

        # Normalize particle weights
        for particle in particles:
            particle.weight /= particle_weight_total

        # Resampling particles
        distribution = WeightedDistribution(particles = particles)
        particles_new = list()

        for i in range(num_particles):

            particle = distribution.random_select()

            if particle is None:
                x = np.random.uniform(0, world.width)
                y = np.random.uniform(0, world.height)
                particles_new.append(Particle(x = x, y = y, maze = world, sensor_limit = sensor_limit))

            else:
                particles_new.append(Particle(x = particle.x, y = particle.y, maze = world, heading = particle.heading, sensor_limit = sensor_limit, noisy = True))

        particles = particles_new

        heading_old = bob.heading
        bob.move(maze = world)
        heading_new = bob.heading
        dh = heading_new - heading_old

        for particle in particles:
            particle.heading = (particle.heading + dh) % 360
            particle.try_move(maze = world, speed = bob.speed)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Particle filter in maze.')

    window_width_default = 800
    window_height_default = 800
    num_particles_default = 3000
    sensor_limit_ratio_default = 0.3
    grid_height_default = 100
    grid_width_default = 100
    num_rows_default = 25
    num_cols_default = 25
    wall_prob_default = 0.25
    random_seed_default = 100
    robot_speed_default = 10
    kernel_sigma_default = 500
    particle_show_frequency_default = 10

    parser.add_argument('--window_width', type = int, help = 'Window width.', default = window_width_default)
    parser.add_argument('--window_height', type = int, help = 'Window height.', default = window_height_default)
    parser.add_argument('--num_particles', type = int, help = 'Number of particles used in particle filter.', default = num_particles_default)
    parser.add_argument('--sensor_limit_ratio', type = float, help = 'Distance limit of sensors (real value: 0 - 1). 0: Useless sensor; 1: Perfect sensor.', default = sensor_limit_ratio_default)
    parser.add_argument('--grid_height', type = int, help = 'Height for each grid of maze.', default = grid_height_default)
    parser.add_argument('--grid_width', type = int, help = 'Width for each grid of maze.', default = grid_width_default)
    parser.add_argument('--num_rows', type = int, help = 'Number of rows in maze', default = num_rows_default)
    parser.add_argument('--num_cols', type = int, help = 'Number of columns in maze', default = num_cols_default)
    parser.add_argument('--wall_prob', type = float, help = 'Wall probability of a random maze.', default = wall_prob_default)
    parser.add_argument('--random_seed', type = int, help = 'Random seed for random maze and particle filter.', default = random_seed_default)
    parser.add_argument('--robot_speed', type = int, help = 'Robot movement speed in maze.', default = robot_speed_default)
    parser.add_argument('--kernel_sigma', type = int, help = 'Standard deviation for Gaussian distance kernel.', default = kernel_sigma_default)
    parser.add_argument('--particle_show_frequency', type = int, help = 'Frequency of showing particles on maze.', default = particle_show_frequency_default)

    argv = parser.parse_args()

    window_width = argv.window_width
    window_height = argv.window_height
    num_particles = argv.num_particles
    sensor_limit_ratio = argv.sensor_limit_ratio
    grid_height = argv.grid_height
    grid_width = argv.grid_width
    num_rows = argv.num_rows
    num_cols = argv.num_cols
    wall_prob = argv.wall_prob
    random_seed = argv.random_seed
    robot_speed = argv.robot_speed
    kernel_sigma = argv.kernel_sigma
    particle_show_frequency = argv.particle_show_frequency

    main(window_width = window_width, window_height = window_height, num_particles = num_particles, sensor_limit_ratio = sensor_limit_ratio, grid_height = grid_height, grid_width = grid_width, num_rows = num_rows, num_cols = num_cols, wall_prob = wall_prob, random_seed = random_seed, robot_speed = robot_speed, kernel_sigma = kernel_sigma, particle_show_frequency = particle_show_frequency)
