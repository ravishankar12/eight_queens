import random


def rnd_chrome(size):  # generating random chromosomes
    return [random.randint(1, nq) for _ in range(nq)]


def fitting(chromosome):
    horizontal_collisions = sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2 * n
    right_diagonal = [0] * 2 * n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter / (n - abs(i - n + 1))

    return int(maxfitting - (horizontal_collisions + diagonal_collisions))


def fnprobability(chromosome, fitting):
    return fitting(chromosome) / maxfitting


def rnd_picking(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def reprod(x, y):  # performing crossover between 2 chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutation(x):  # randomizing the value of an index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def genetic_queen(population, fitting):
    mutation_probability = 0.03
    new_population = []
    probabilities = [fnprobability(n, fitting) for n in population]
    for i in range(len(population)):
        x = rnd_picking(population, probabilities)  # 1st best chromosome
        y = rnd_picking(population, probabilities)  # 2nd best chromosome
        child = reprod(x, y)  # producing 2 new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutation(child)
        new_population.append(child)
        if fitting(child) == maxfitting: break
    return new_population


def print_chrome(chrom):
    print("Chromosome = {},  Fitness = {}"
          .format(str(chrom), fitting(chrom)))


if __name__ == "__main__":
    nq = 8  # say N = 8
    maxfitting = (nq * (nq - 1)) / 2  # (8*7)/2 = 28
    population = [rnd_chrome(nq) for _ in range(100)]

    generation = 1

    while not maxfitting in [fitting(chrom) for chrom in population]:
        population = genetic_queen(population, fitting)
        generation += 1
    chrom_out = []
    print("Solved in Generation {}!".format(generation - 1))
    for chrom in population:
        if fitting(chrom) == maxfitting:
            print("");
            print("One of the solutions: ")
            chrom_out = [x-1 for x in chrom]
            print_chrome(chrom_out)