"""
TITLE:          project.py
DIRECTORY:      Reinforcement Racer project.
DESCRIPTION:    Main project file for the reinforcement
                racer project - one of two primary projects
                for DU's ACS 2500: Core Apps of AI course.
MUTABILITY:     This file contains challenges that must be
                resolved for full project completion. (NOTE:
                You may answer relevant TODOs by creating
                additional docstrings and commented segments
                that contain your respective answers.)
"""


# Relative Imports and Instantiations
import numpy as np
import matplotlib.pyplot as plt
import os, sys, math, random
import neat, pygame

from structures.structures import CarAgent


# Setup Agent Variables
AGENT_PARAMETERS = {
    "X": 60, 
    "Y": 60
}

# Setup Game Environment Variables
ENVIRONMENT_PARAMETERS = {
    "WIDTH":    1920,
    "HEIGHT":   1080
}

# Set Color of Racetrack Border for Collision Detection
BORDER_COLOR = (255, 255, 255, 255)

# Set Flag for Tracking Generational Training
current_generation = 0


def racecar_simulator(genomes, configurations):
    """ Custom function to conduct simulated reinforcement learning using naive self-driving car object. """
    # Initialize arrays for storing models and game agent over training
    models, agents = list(), list()

    # Initialize PyGame utilities for training
    pygame.init(); screen = pygame.display.set_mode((ENVIRONMENT_PARAMETERS["WIDTH"], ENVIRONMENT_PARAMETERS["HEIGHT"]), 
                                                     pygame.FULLSCREEN)
    
    # Iteratively train agent using Deep RL
    for iteration, genome in genomes:
        # TODO: What type of neural network is designed here? 
        # Answer: The neural network is classiffied as a feedforward neural network 

        # TODO: Can we utilize more advanced neural networks instead?
        # Yes, we can utilize more advanced networks like convolutional neural networks, recurrent neural networks, etc.
        # So that there is knoedlge of past events and the ability to predict future events on some level
        # TODO: What is the tradeoff of using higher-order and/or lower-order networks? 
        # lower order networks are more computationally expensive, but they are more accurate
        # higher order networks are more computationally efficient, but they are less accurate
        model = neat.nn.FeedForwardNetwork.create(genome, configurations)
        
        # Save instantiated models with (re)set genetic training counter
        models.append(model)
        genome.fitness = 0

        # Instantiate agent with necessary state data
        agents.append(CarAgent(agent_parameters=AGENT_PARAMETERS,
                               environment_parameters=ENVIRONMENT_PARAMETERS,
                               border_color=BORDER_COLOR))

    # Create necessary parameters to set up PyGame environment for training
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)

    # Read in environment image map
    environment = pygame.image.load("assets/environments/newmap.png").convert()

    # Iterate generation counter as global variable 
    global current_generation
    current_generation += 1

    # Create dummy counter for early stopping
    counter = 0

    # Optimize agent driving directionality/velocity choices using game agent policy optimization
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        if event.type == pygame.KEYDOWN:
            #
            # To quit the game the user has to press the escape key
            # Im adding this to the project because I couldnt close it before.

            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        for iteration, agent in enumerate(agents):
            output = models[iteration].activate(agent.get_actions())
            choice = output.index(max(output))
            # TODO: Explain how policy selection works here – how are choices selected
            #       across our reinforcement learning agent? What do those choices
            #       actually do for our game-playing bot?
            # Explanation:
            #   The policy selection process is used to determine
            #   the optimal policy for the agent to use.
            # It is putting in agent actions for each of the models, and then outputting the highest 
            # value of the output. The index of the highest value is then used to determine the action.
            #   The output is then used to determine the action.




            if choice == 0:
                agent.angle += 10
            elif choice == 1:
                agent.angle -= 10
            elif choice == 2:
                if agent.speed - 2 >= 12:
                    agent.speed -= 2
            else:
                agent.speed += 2

        # Check if RL Agent is alive and optimize rewarding schema
        # TODO: Explain how the rewards are selected here – how is the 
        #       rewarding schema related to the model's training fitness?
        #   The fitness is determined by the number of times the car has crashed into the border.
        #   If the car is still alive, the fitness is increased by 1. We want the highest score possible for fitness,
        # so we can pass that generation on to the next iteration
       
        still_alive = 0
        for iteration, agent in enumerate(agents):
            if agent.is_alive():
                still_alive += 1
                agent.play_game(environment)
                genomes[iteration][1].fitness += agent.get_rewards()

        # Escape case if agent dies
        if still_alive == 0:
            break

        # Escape case after sufficient training generations
        counter += 1
        if counter == 30 * 40:
            break

        # Update screen rendition
        screen.blit(environment, (0, 0))
        for agent in agents:
            if agent.is_alive():
                agent.draw(screen)

        # Render additional visual information for RL task
        text = generation_font.render("Generation: {}".format(str(current_generation)),
                                      True,
                                      (0, 0, 0))
        text_rectangle = text.get_rect()
        text_rectangle.center = (900, 450)
        screen.blit(text, text_rectangle)

        text = alive_font.render("Still Alive: {}".format(str(still_alive)),
                                 True,
                                 (0, 0, 0))
        text_rectangle = text.get_rect()
        text_rectangle.center = (900, 490)
        screen.blit(text, text_rectangle)

        pygame.display.flip(); clock.tick(60)





# Run code
if __name__ == "__main__":
    PATH_CONFIG = "./config.txt"
    configurations = neat.config.Config(neat.DefaultGenome,
                                        neat.DefaultReproduction,
                                        neat.DefaultSpeciesSet,
                                        neat.DefaultStagnation,
                                        PATH_CONFIG)
    
    population = neat.Population(configurations)
    population.add_reporter(neat.StdOutReporter(True))
    population_statistics = neat.StatisticsReporter()
    population.add_reporter(population_statistics)

    population.run(racecar_simulator, 21)


    # This project generates an accuracy report for the neural network.
    # This is located in the "reports" folder.
    # The accuracy report is generated by the "neat-report" command.
    # The neat report command is on line 