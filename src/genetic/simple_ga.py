import copy
import random

from src.modelisation.modelisation import Cube, invert_moves
from src.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_2x2,
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
    simple_distances_total_independent_moves_all_2x2
)
from src.evaluation.basic.membership import face_color_membership_evaluation_function

class GeneticAlgorithm:
    def __init__(
        self,
        nb_individuals,
        nb_generations,
        length_individual,
        mutation_rate,
        cube: Cube,
        evaluation_function,
    ):
        self.nb_individuals = nb_individuals
        self.nb_generations = nb_generations
        self.mutation_rate = mutation_rate
        self.cube = cube
        self.length_individual = length_individual
        self.evaluation_function = evaluation_function

    def run(self):
        # Initial population of permutations of the cube
        # The population consists of a list of individuals where each individual is a list of permutations
        generation = [
            random.choices([*self.cube.perms.keys()], k=self.length_individual)
            for _ in range(self.nb_individuals)
        ]

        for generation_count in range(self.nb_generations):
            print("<============================>")
            print(f"Generation {generation_count}")

            mate_pool = []
            current_generation = copy.deepcopy(generation)

            # Select the top half of individuals from the current generation to create the next generation
            generation = current_generation[0:int(self.nb_individuals / 2) + 1]

            # Fill the remaining half of the next generation with mutated individuals
            for i in range(int(self.nb_individuals) - len(generation)):
                generation.append(self.mutate(generation[i]))

            # Perform weighted selection based on fitness
            generation = self.selection(generation)

            # Select the top 10% of individuals from the previous generation to add to the mate pool
            top_generation = self.select_best(current_generation, int(len(current_generation) / 10))
            mate_pool.extend(top_generation)

            # Create new individuals by performing crossover
            crossed = self.crossover(generation)
            mate_pool.extend(crossed)

            # Randomly mutate individuals in the mate pool based on the mutation rate
            for i in range(len(mate_pool)):
                if random.random() < self.mutation_rate:
                    mate_pool[i] = self.mutate(mate_pool[i])

            # Select the top individuals from the mate pool to create the next generation
            generation = self.select_best(mate_pool, len(generation))

            # Evaluate the fitness of all individuals in the current generation and update the best individual
            best_score = self.evaluate(generation[0])
            best_ind = generation[0]
            for individual in generation:
                new_score = self.evaluate(individual)
                if new_score < best_score:
                    best_score = new_score
                    best_ind = individual

            print(f"best : {best_score}")
            self.print_individual(best_ind)

            # If the best individual has a fitness of 0, return it
            if best_score == 0:
                return best_ind
        # Return the best individual from the last generation
        return best_ind

    def print_individual(self, individual):
        """
        Print the individual and its permutation
        """
        print(individual)
        print(self.cube.permute(individual))

    def init_pop(self):
        """
        Initialize the population with random individuals
        """
        return [random.choices([*self.cube.perms.keys()], k=self.length_individual) for _ in range(self.nb_individuals)]

    def select_best(self, generation, trunc_value):
        """
        Select the best individuals from a generation based on the evaluation function
        """
        new_generation = []
        # Evaluate each individual
        evaluated = [self.evaluate(individual) for individual in generation]
        list_evaluated_generation = []
        # Sorting based on evaluation
        for i in range(len(generation)):
            list_evaluated_generation.append((evaluated[i], generation[i]))

        list_evaluated_generation.sort()
        for i in list_evaluated_generation[:trunc_value]:
            new_generation.append(i[1])
        return new_generation

    def mutate(self, individual):
        """
        Mutate an individual
        """
        mutation_nbr = random.randint(1, len(individual) - 1)
        for i in range(mutation_nbr):
            index = random.randint(0, len(individual) - 1)
            possibilities = [*self.cube.perms.keys()]
            gene_value = individual[index]
            possibilities.remove(gene_value)
            try:
                possibilities.remove(invert_moves([gene_value])[0])
            except ValueError:
                pass
            if index > 0:
                try:
                    possibilities.remove(individual[index - 1])
                except ValueError:
                    pass
            if index < len(individual) - 1:
                try:
                    possibilities.remove(individual[index + 1])
                except ValueError:
                    pass
            mutated = individual.copy()
            random_choice = random.choice(possibilities)
            mutated[index] = random_choice

        return mutated

    def next_generation(self, generation):
        """
        The chromosomes of the current population are selected using roulette wheel method with probability =80%
        and offsprings (children) are generated using one point crossover op
        """

        # Selection
        roulette_wheel = self.selection(generation)
        selected_individuals = self.selection_elitist(generation)

        # Crossover
        crossed_generation = self.crossover(roulette_wheel)

        return crossed_generation

    def selection(self, generation):

        # Evaluate each individual
        evaluated = [
            1 / self.evaluate(individual) if self.evaluate(individual) != 0 else 100
            for individual in generation
        ]

        return random.choices(generation, weights=evaluated, k=self.nb_individuals)

    def selection_elitist(self, generation):
        """
        Multiply by 10 the number of the 5% best solutions in the generation
        :param generation:
        :return:
        """
        new_generation = []
        # Evaluate each individual
        evaluated = [self.evaluate(individual) for individual in generation]
        list_evaluated_generation = []
        # Sorting based on evaluation
        for i in range(len(generation)):
            list_evaluated_generation.append((evaluated[i], generation[i]))
        list_evaluated_generation.sort()

        # Make the 5% best take over 45% of the population
        for i in range(int(len(generation) * 0.05)):
            for j in range(9):
                new_generation.append(list_evaluated_generation[i][1])

        # Make the 55% best take over the rest of the population
        while len(new_generation) < len(generation):
            new_generation.append(list_evaluated_generation[len(new_generation)][1])

        return new_generation

    def crossover(self, selected_individuals):
        """
        Perform crossover on a list of selected individuals to generate a new generation of individuals
        """
        new_generation = []
        # loop through pairs of individuals in the list
        for i in range(0, len(selected_individuals), 2):
            # pass them to the crossover_individuals method
            new_generation.extend(
                self.crossover_individuals(
                    selected_individuals[i],
                    selected_individuals[random.randint(0, len(selected_individuals) - 1)],
                )
            )
        # return the new generation of individuals
        return new_generation

    def crossover_individuals(self, individual1, individual2):
        """
        Crossover two individuals by selecting a random crossover point and mixing the genes before and after the point
        """
        crossover_point = random.randint(0, self.length_individual - 1)
        acceptable_children = []
        # swap genes before and after the crossover point to create two new children
        x = [
            individual1[:crossover_point] + individual2[crossover_point:],
            individual2[:crossover_point] + individual1[crossover_point:],
        ]
        # add both new children to a list
        acceptable_children.append(x[0])
        acceptable_children.append(x[1])
        # return the list of new children
        return acceptable_children

    def evaluate(self, individual):
        """
        Evaluate an individual by permuting a given cube object with the individual's permutation keys and passing the resulting cube to an evaluation function
        """
        cube = self.cube.permute(individual)
        # evaluate the resulting cube and return the fitness score of the individual
        return self.evaluation_function(Cube(cube.n, cube))


if __name__ == "__main__":
    cube = Cube(3)
    scramble = cube.scramble(15)
    scrambled_cube = copy.deepcopy(cube)
    print(scramble)

    best_sol = GeneticAlgorithm(
        500, 2000, 10, 0.2, cube, face_color_membership_evaluation_function
    ).run()

    print(best_sol)
    print(scrambled_cube.permute(best_sol))
    print(scramble)
    print(cube)
