import numpy as np
import random

number_of_ind = 200
size = 100

found = True
step = 0

random_individuals = np.random.randint(1, 9, size=(number_of_ind, 8))


# Main function
def main():
    global random_individuals
    fitness = list()
    set_of_s = list()
    set_of_parents = list()
    pop_of_offsprings = np.zeros((number_of_ind, 8))
    offsprings = np.zeros((number_of_ind, 8))
    new_population = pop_of_offsprings

    def ind(gen_of_ind):
        chess_table_ind = np.zeros((8, 8))
        for k in range(8):
            chess_table_ind[gen_of_ind[k] - 1, k] = gen_of_ind[k]

        # The fitness function
        counter = 0
        for v in range(8):
            for s in range(v + 1, len(gen_of_ind)):
                if gen_of_ind[v] == gen_of_ind[s]:
                    counter += 1
                if s - v == abs(gen_of_ind[s] - gen_of_ind[v]):
                    counter += 1
        fitness.append(28 - counter)

    for t in range(number_of_ind):
        ind(random_individuals[t])

    # Roulette wheel function
    def roulette_wheel():

        f = sum(fitness)

        for i in range(number_of_ind):
            if i == 0:
                set_of_s.append(range(0, fitness[0]))
            else:
                set_of_s.append(range(sum(fitness[:i]), sum(fitness[:i+1])))

        for s in range(number_of_ind):
            r = round(random.random(), 8)
            r1 = int(r * f)
            for e in set_of_s:
                if r1 in e:
                    set_of_parents.append(set_of_s.index(e) + 1)
        # End of roulette wheel function

    roulette_wheel()

    # Crossover operator function
    def crossover_operator():

        j = 0
        for i in range(int(number_of_ind/2)):

            r_i = random.randint(0, 8)
            offsprings[j] = random_individuals[set_of_parents[j] - 1]
            offsprings[j+1] = random_individuals[set_of_parents[j+1] - 1]
            pop_of_offsprings[j] = np.concatenate(((offsprings[j])[:r_i], (offsprings[j+1])[r_i:]))
            pop_of_offsprings[j+1] = np.concatenate(((offsprings[j+1])[:r_i], (offsprings[j])[r_i:]))

            j += 2

    crossover_operator()

    # Mutation function
    def mutation():

        random_numbers = np.random.randint(1, size, size=(number_of_ind, 8))

        r_counter = 0
        for q in range(number_of_ind):
            for j in range(8):
                if random_numbers[q][j] == 1:
                    r = random.randint(1, 8)
                    new_population[q][j] = r
                    r_counter += 1
        # End of mutation function

    mutation()

    # Count no attacks function
    def count_steps():

        size_rows = len(new_population)
        while size_rows > 0:

            counter = 0
            for v in range(8):
                for s in range(v + 1, len(new_population[size_rows-1])):
                    if (new_population[size_rows-1])[v] == (new_population[size_rows-1])[s]:
                        counter += 1
                    if s - v == abs((new_population[size_rows-1])[s] - (new_population[size_rows-1])[v]):
                        counter += 1
            global step
            step += 1
            if counter == 0:
                print(f'\nNumber of individuals --> {number_of_ind}\np_m --> {1/size}')
                print(f'\nNo attack in Ind --> {step}')
                print(new_population[size_rows-1])
                print('\n--------------------------')
                global found
                found = False
                break
            size_rows -= 1

    count_steps()
    # End of count no attacks function

    def update():
        global random_individuals
        new_population2 = pop_of_offsprings.astype(int)
        random_individuals = new_population2

    update()


while found:
    main()
