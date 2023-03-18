import random

from src.modelisation.modelisation import Cube, invert_moves
from src.search.evaluation.distance import distance_to_good_face_evaluation_function
from src.search.evaluation.membership import face_color_membership_evaluation_function


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
        generation = [
            random.choices([*self.cube.perms.keys()], k=self.length_individual)
            for _ in range(self.nb_individuals)
        ]

        for generation_count in range(self.nb_generations):
            print(f"Generation {generation_count}")

            generation = self.next_generation(generation)

            for individual in generation:
                self.mutate(individual)

            print(len(generation[0]))

            print(min([self.evaluate(individual) for individual in generation]))

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
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

            before_mutation = individual.copy()

            individual[index] = random.choice(possibilities)

            if self.evaluate(individual) > self.evaluate(before_mutation):
                individual = before_mutation

        return individual

    def next_generation(self, generation):
        """
        The chromosomes of the current population are selected using roulette wheel method with probability =80%
        and offsprings (children) are generated using one point crossover op
        """

        # Selection
        selected_individuals = self.selection(generation)

        # Crossover
        new_generation = self.crossover(selected_individuals)

        return new_generation

    def selection(self, generation):

        # Evaluate each individual
        evaluated = [self.evaluate(individual) for individual in generation]

        return random.choices(generation, weights=evaluated, k=self.nb_individuals)

    def crossover(self, selected_individuals):

        # Crossover
        new_generation = []

        for i in range(0, len(selected_individuals), 2):
            new_generation.extend(
                self.crossover_individuals(
                    selected_individuals[i], selected_individuals[i + 1]
                )
            )

        return new_generation

    def crossover_individuals(self, individual1, individual2):
        """
        Crossover two individuals
        """
        crossover_point = random.randint(0, self.length_individual - 1)

        x = [
            individual1[:crossover_point] + individual2[crossover_point:],
            individual2[:crossover_point] + individual1[crossover_point:],
        ]

        if self.evaluate(x[0]) < self.evaluate(individual1):
            individual1 = x[0]
        if self.evaluate(x[1]) < self.evaluate(individual2):
            individual2 = x[1]

        return [individual1, individual2]

    def evaluate(self, individual):
        cube = self.cube.permute(individual)

        return self.evaluation_function(Cube(3, cube))


if __name__ == "__main__":
    cube = Cube(3)
    cube.scramble(100)
    GeneticAlgorithm(
        100, 1000, 100, 0.2, cube, face_color_membership_evaluation_function
    ).run()
