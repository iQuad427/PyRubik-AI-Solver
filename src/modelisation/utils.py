
def define_permutation(moves: list[tuple[int, ...]]):
    """
    Simplify the permutation associated to a list of basic permutations
    :param moves: list of permutation

    use: define_permutation([perms[move] for move in moves])
            where:  perms is the dict of moves -> permutation
                    moves is the list of movements (U, F, D, R, L, B)
    """
    fake_cube = [i for i in range(54)]
    apply_permutation(fake_cube, moves)

    return fake_cube


def apply_permutation(num: list[int], perm: list[tuple[int, ...]]):
    save = list(num)
    for t in perm:
        u = (t[-1],) + t
        for i, v in enumerate(t):
            num[v] = save[u[i]]
