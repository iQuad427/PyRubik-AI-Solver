import copy
import random

from src.evaluation.basic.entropy import entropy_based_score_evaluation_function
from src.modelisation.modelisation import Cube, invert_moves
from src.evaluation.look_up.functions.distances import (
    simple_distances_total_independent_moves_2x2,
    simple_distances_total_independent_moves_3x3,
    simple_distances_total_independent_moves_all_3x3,
    simple_distances_total_independent_moves_all_2x2
)
from src.evaluation.basic.membership import face_color_membership_evaluation_function

from src.genetic.simple_ga import GeneticAlgorithm


FULL_ROTATIONS = ["L' M M M R".split(" "),
    "L M R'".split(" "),
    "L L M M R' R'".split(" "),
    "U E E E D'".split(" "),
    "U' E D".split(" "),
    "U' U' E E D D".split(" ")]


ORIENTATIONS = [
    "F S B'".split(" "),
    "F F S S B' B'".split(" "),
    "F' S S S B".split(" ")]
PERMUTATIONS = [
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
    "M M U M M U U M M U M M".split(" ")
]
POSSIBILITIES = [i for i in range(len(PERMUTATIONS))]

class PermutationsGa(GeneticAlgorithm):

    def run(self):
        generation = self.init_pop()
        for generation_count in range(self.nb_generations):
            print("<============================>")
            print(f"Generation {generation_count}")
            mate_pool = []
            current_generation = copy.deepcopy(generation)
            generation = current_generation[0 : int(self.nb_individuals / 10) + 1]
            for i in range(int(self.nb_individuals) - len(generation)):
                generation.append(generation[0][:int(len(generation[i])/10)+1])
            # evaluated = [
            #     self.evaluate(individual) if self.evaluate(individual) != 0 else 100
            #     for individual in generation
            # ]
            # print(evaluated)

            # Selection
            generation = self.selection_elitist(generation)
            top_generation = self.select_best(
                current_generation, int(len(current_generation) / 10)
            )
            mate_pool.extend(top_generation)

            # crossed = self.crossover(generation)

            # mate_pool.extend(crossed)
            mate_pool.extend(generation[int(len(current_generation) / 10):])

            for i in range(int(len(generation)/10),len(mate_pool)):
                if random.random() < self.mutation_rate:
                    mate_pool[i] = self.mutate(top_generation[random.randint(0,len(top_generation)-1)])
            # generation = self.select_best(mate_pool, len(generation))
            generation = self.select_best(mate_pool, len(current_generation))

            best_score = self.evaluate(generation[0])
            best_ind = generation[0]

            for individual in generation:
                new_score = self.evaluate(individual)
                if new_score < best_score:
                    best_score = new_score
                    best_ind = individual

            print(f"best : {best_score}")
            self.print_best(best_ind)

            if best_score == 0:
                return best_ind

            # print(cube.permute(best_ind))
            # print(min([self.evaluate(individual) for individual in generation]))
        return best_ind

    def print_best(self, best_ind):
        best_moves = []
        print(best_ind)
        for i in best_ind:
            best_moves.extend(PERMUTATIONS[i])
        print(best_moves)
        print(len(best_moves))
        print(self.cube.permute(best_moves))
    def init_pop(self):
        return [random.choices(POSSIBILITIES, k=self.length_individual)for _ in range(self.nb_individuals)]
    def mutate(self, individual):
    # mutation_nbr = random.randint(1, len(individual) - 1)
    # for i in range(mutation_nbr):
        # index = random.randint(0, len(individual) - 1)
        # gene_value = individual[index]
        # possibilities.remove(gene_value)

        mutated = individual.copy()
        # random_choice = random.choice(possibilities)
        # mutated[index] = random_choice

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
        perms = []
        for i in individual:
            perms.extend(PERMUTATIONS[i])
        cube = self.cube.permute(perms)

        return self.evaluation_function(Cube(cube.n, cube))

if __name__ == "__main__":
    best_sol =[]
    cube = Cube(3, include_crown_moves=True)
    scramble = cube.scramble(15)
    print(scramble)

    best_sol = GeneticAlgorithm(
        100, 100, 25, 0.3, cube, face_color_membership_evaluation_function
    ).run()

    cube = cube.permute(best_sol)
    PermutationsGa(
        500, 300, 1, 1, cube, face_color_membership_evaluation_function
    ).run()

    print(scramble)
    print(cube)