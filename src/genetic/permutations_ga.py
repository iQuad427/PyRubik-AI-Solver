import copy
import random

from src.evaluation.basic.entropy import entropy_based_score_evaluation_function
from src.modelisation.modelisation import Cube, invert_moves, simplify_formula
from src.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_2x2,
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
    simple_distances_total_independent_moves_all_2x2
)
from src.evaluation.basic.membership import face_color_membership_evaluation_function

from src.genetic.simple_ga import GeneticAlgorithm


class PermutationsGa(GeneticAlgorithm):

    def __init__(
            self,
            nb_individuals,
            nb_generations,
            length_individual,
            mutation_rate,
            cube: Cube,
            evaluation_function,
    ):
        super().__init__(nb_individuals,nb_generations,length_individual,mutation_rate,cube,evaluation_function)
        self.permutations = [
        "L' M M M R".split(" "),
        "L M R'".split(" "),
        "L L M M R' R'".split(" "),
        "U E E E D'".split(" "),
        "U' E D".split(" "),
        "U' U' E E D D".split(" "),
        "F S B'".split(" "),
        "F F S S B' B'".split(" "),
        "F' S S S B".split(" "),
        # permutes two edges: U face, bottom edge and right edge
        "F' L' B' R' U' R U' B L F R U R' U".split(" "),
        # permutes two edges: U face, bottom edge and left edge
        "F R B L U L' U B' R' F' L' U' L U'".split(" "),
        # permutes two corners: U face, bottom left and bottom right
        "U U B U U B' R R F R' F' U U F' U U F R'".split(" "),
        # permutes three corners: U face, bottom left and top left
        "U U R U U R' F F L F' L' U U L' U U L F'".split(" "),
        # permutes three centers: F face, top, right, bottom
        "U' B B D D L' F F D D B B R' U'".split(" "),
        # permutes three centers: F face, top, right, left
        "U B B D D R F F D D B B L U".split(" "),
        # U face: bottom edge <-> right edge, bottom right corner <-> top right corner
        "D' R' D R R U' R B B L U' L' B B U R R".split(" "),
        # U face: bottom edge <-> right edge, bottom right corner <-> left right corner
        "D L D' L L U L' B B R' U R B B U' L L".split(" "),
        # U face: top edge <-> bottom edge, bottom left corner <-> top right corner
        "R' U L' U U R U' L R' U L' U U R U' L U'".split(" "),
        # U face: top edge <-> bottom edge, bottom right corner <-> top left corner
        "L U' R U U L' U R' L U' R U U L' U R' U".split(" "),
        # permutes three corners: U face, bottom right, bottom left and top left
        "F' U B U' F U B' U'".split(" "),
        # permutes three corners: U face, bottom left, bottom right and top right
        "F U' B' U F' U' B U".split(" "),
        # permutes three edges: F face bottom, F face top, B face top
        "L' U U L R' F F R".split(" "),
        # permutes three edges: F face top, B face top, B face bottom
        "R' U U R L' B B L".split(" "),
        # H permutation: U Face, swaps the edges horizontally and vertically
        "M M U M M U U M M U M M".split(" ")]
    def run(self):
        generation = self.init_pop()
        # Iterate over generations
        for generation_count in range(self.nb_generations):
            print("<============================>")
            print(f"Generation {generation_count}")

            # Create a mating pool
            mate_pool = []

            # Copy the current generation
            current_generation = copy.deepcopy(generation)

            # Select the top 10% of individuals and add them to the next generation
            generation = current_generation[0: int(self.nb_individuals / 10) + 1]

            # Fill the rest of the next generation by duplicating the top individual and adding mutations
            for i in range(int(self.nb_individuals) - len(generation)):
                generation.append(generation[0][:int(len(generation[i]) / 10) + 1])

            # Perform elitist selection on the current generation and add the top individuals to the mating pool
            generation = self.selection_elitist(generation)
            top_generation = self.select_best(current_generation, int(len(current_generation) / 10))
            mate_pool.extend(top_generation)
            mate_pool.extend(generation[int(len(current_generation) / 10):])

            # Mutate individuals in the mating pool
            for i in range(int(len(generation) / 10), len(mate_pool)):
                if random.random() < self.mutation_rate:
                    mate_pool[i] = self.mutate(top_generation[random.randint(0, len(top_generation) - 1)])

            # Select the best individuals from the mating pool to form the next generation
            generation = self.select_best(mate_pool, len(current_generation))

            # Evaluate the fitness of the best individual in the current generation
            best_score = self.evaluate(generation[0])
            best_ind = generation[0]

            # Evaluate the fitness of each individual in the current generation and update the best individual if necessary
            for individual in generation:
                new_score = self.evaluate(individual)
                if new_score < best_score:
                    best_score = new_score
                    best_ind = individual

            # Print the best individual and its fitness score
            print(f"best : {best_score}")
            self.print_individual(best_ind)

            # If a solution is found, return the corresponding sequence of moves
            if best_score == 0:
                best_moves = []
                for i in best_ind:
                    best_moves.extend(self.permutations[i])
                return best_moves

        # If no solution is found, return the sequence of moves for the best individual in the last generation
        best_moves = []
        for i in best_ind:
            best_moves.extend(self.permutations[i])
        return best_moves

    def print_individual(self, individual):
        """
        Given the best individual, print its corresponding moves, its length and the final state of the cube.
        """
        best_moves = []
        print(individual)
        # Loop through each move of the best individual and get the corresponding permutation moves
        for i in individual:
            best_moves.extend(self.permutations[i])
        print(best_moves)
        # Print the length of the permutation sequence
        print(len(best_moves))
        # Permute the cube with the obtained permutation sequence and print the resulting cube state
        print(self.cube.permute(best_moves))

    def init_pop(self):
        """
        Initialize a population of individuals where each individual is a list of integer values representing moves.
        """
        possibilities = [i for i in range(len(self.permutations))]
        return [random.choices(possibilities, k=self.length_individual) for _ in range(self.nb_individuals)]

    def mutate(self, individual):
        """
        Given an individual, apply mutation to it by appending new random moves.
        This mutation method is from this project https://github.com/rvaccarim/genetic_rubik
        """
        mutated = individual.copy()
        # Select a mutation type randomly from the given six types
        evolution_type = random.randint(0, 5)
        if evolution_type == 0:
            perms = random.randint(9, 23)
            mutated.append(perms)
        elif evolution_type == 1:
            perms = random.randint(9, 23)
            mutated.append(perms)
            perms = random.randint(9, 23)
            mutated.append(perms)
        elif evolution_type == 2:
            perms = random.randint(0, 5)
            mutated.append(perms)
            perms = random.randint(9, 23)
            mutated.append(perms)
        elif evolution_type == 3:
            perms = random.randint(6, 8)
            mutated.append(perms)
            perms = random.randint(9, 23)
            mutated.append(perms)
        elif evolution_type == 4:
            perms = random.randint(0, 5)
            mutated.append(perms)
            perms = random.randint(6, 8)
            mutated.append(perms)
            perms = random.randint(9, 23)
            mutated.append(perms)
        elif evolution_type == 5:
            perms = random.randint(6, 8)
            mutated.append(perms)
            perms = random.randint(0, 5)
            mutated.append(perms)
            perms = random.randint(9, 23)
            mutated.append(perms)

        return mutated

    def evaluate(self, individual):
        """
        Evaluate an individual by permuting a given cube object with the individual's permutation keys and passing the resulting cube to an evaluation function
        """
        perms = []
        for i in individual:
            perms.extend(self.permutations[i])
        cube = self.cube.permute(perms)

        return self.evaluation_function(Cube(cube.n, cube))

if __name__ == "__main__":
    best_sol =[]
    cube = Cube(3, include_crown_moves=True)
    scramble = cube.scramble(20)
    print(scramble)

    best_sol = GeneticAlgorithm(
        200, 300, 25, 0.8, cube, face_color_membership_evaluation_function
    ).run()

    cube = cube.permute(best_sol)
    best_sol.extend(PermutationsGa(
        500, 400, 1, 1, cube, face_color_membership_evaluation_function
    ).run())

    print(best_sol)
    print(cube.permute(best_sol))
    print(scramble)
    print(cube)
    print("length of the solution : ", len(simplify_formula(best_sol)))