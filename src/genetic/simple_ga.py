import copy
import random

from src.modelisation.modelisation import Cube, invert_moves
from src.search.evaluation.entropy import entropy_based_score_evaluation_function
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
            print("<============================>")
            print(f"Generation {generation_count}")
            mate_pool = []
            current_generation = copy.deepcopy(generation)
            # generation = current_generation[5:95]
            # generation.extend(current_generation[40:50])
            evaluated = [self.evaluate(individual) if self.evaluate(individual) != 0 else 100 for individual in
                         current_generation]
            print(evaluated)
            evaluated = [self.evaluate(individual) if self.evaluate(individual) != 0 else 100 for individual in
                         generation]
            print(evaluated)
            # Selection
            generation = self.selection(generation)
            mate_pool.extend(self.crossover(generation))

            for individual in generation:
                if random.random() < self.mutation_rate:
                    individual = self.mutate(individual)
                    mutated = self.mutate(individual)
                    if self.evaluate(individual) != self.evaluate(mutated):
                        mate_pool.append(mutated)
            mate_pool.extend(self.select_best(current_generation, int(len(current_generation)/10)))
            print(mate_pool)

            generation = self.select_best(mate_pool, len(generation))
            check_duplicates_generation = []
            for i in generation:
                if i not in check_duplicates_generation:
                    check_duplicates_generation.append(i)
            print("generation size: ", len(generation), "\n#non-duplicates: ", len(check_duplicates_generation))

            best_score = self.evaluate(generation[0])
            best_ind = generation[0]
            for individual in generation:
                if self.evaluate(individual) < best_score:
                    best_ind = individual

            print(f"best : {best_score}")
            print(best_ind)
            if best_score == 0:
                break
            #print(cube.permute(best_ind))

            # print(min([self.evaluate(individual) for individual in generation]))


    def select_best(self, generation, trunc_value):
        new_generation = []
        # Evaluate each individual
        evaluated = [self.evaluate(individual) for individual in generation]
        list_evaluated_generation = []
        # Sorting based on evaluation
        for i in range(len(generation)):
            list_evaluated_generation.append((evaluated[i], generation[i]))

        list_evaluated_generation.sort()

        try:
            for i in list_evaluated_generation[:trunc_value]:
                new_generation.append(i[1])
        except:
            print("trunc_value is too high")
        return new_generation

    def select_worst(self, generation, trunc_value):
        new_generation = []
        # Evaluate each individual
        evaluated = [self.evaluate(individual) for individual in generation]
        list_evaluated_generation = []
        # Sorting based on evaluation
        for i in range(len(generation)):
            list_evaluated_generation.append((evaluated[i], generation[i]))

        list_evaluated_generation.sort(reverse=True)

        try:
            for i in list_evaluated_generation[:trunc_value]:
                new_generation.append(i[1])
        except:
            print("trunc_value is too high")
        return new_generation

    def mutate(self, individual):
        index = random.randint(0, len(individual) - 1)

        possibilities = [*self.cube.perms.keys()]
        for i in range(5):
            possibilities.append("N")
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

        # if self.evaluate(individual) > self.evaluate(mutated):
        #     individual[index] = random_choice

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
        evaluated = [1/self.evaluate(individual) if self.evaluate(individual) !=0 else 100 for individual in generation]

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
        for i in range(int(len(generation)*0.05)):
            for j in range(9):
                new_generation.append(list_evaluated_generation[i][1])

        # Make the 55% best take over the rest of the population
        while len(new_generation) < len(generation):
            new_generation.append(list_evaluated_generation[len(new_generation)][1])

        return new_generation

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
        acceptable_children = []
        x = [
            individual1[:crossover_point] + individual2[crossover_point:],
            individual2[:crossover_point] + individual1[crossover_point:],
        ]

        # if self.evaluate(x[0]) < self.evaluate(individual1):
        #     individual1 = x[0]
        # if self.evaluate(x[1]) < self.evaluate(individual2):
        #     individual2 = x[1]
        #if self.evaluate(x[0]) <= self.evaluate(individual1):
        acceptable_children.append(x[0])
        #if self.evaluate(x[1]) <= self.evaluate(individual2):
        acceptable_children.append(x[1])

        # return [individual1, individual2]
        return acceptable_children


    def evaluate(self, individual):
        cube = self.cube.permute(individual)

        return self.evaluation_function(Cube(cube.n, cube))


    # def evaluate(self, perms):
    #     new_cube = list(self.cube.cube)
    #     min = 24
    #     for perm in perms:
    #         save = list(new_cube)
    #         mvt = self.cube.perms[perm]
    #         for t in mvt:
    #             u = (t[-1],) + t
    #             for i, v in enumerate(t):
    #                 new_cube[v] = save[u[i]]
    #         cubee = Cube(self.cube.n, new_cube)
    #         value = self.evaluation_function(Cube(cubee.n, cubee))
    #         if value < min:
    #             min = value
    #     return min



if __name__ == "__main__":
    cube = Cube(2)
    # print(cube.scramble(8))
    cube = cube.permute(["R'", 'D', "F'", 'U', "L'", 'D', 'B', 'L'])
    # cube = cube.permute(["R'", 'D', "F'", 'U', "L'", 'D', 'B'])
    # cube = cube.permute(["R'", 'D', "F'", 'U', "L'"])
    GeneticAlgorithm(
        100, 500, 30, 0.5, cube, entropy_based_score_evaluation_function
    ).run()
