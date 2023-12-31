import csv
import random


def get_random_int(max_val):
    return random.randint(0, int(max_val - 1))


def load_csv(file_path='./data.csv'):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def calculate_fitness(chromosome, detailed_chromosome):
    total_value, total_weight, total_size = __calculate_sum_of_objects(chromosome, detailed_chromosome)
    calculated_fitness = total_value if total_weight <= 220 and total_size <= 2.0 else 0
    return calculated_fitness


def __calculate_sum_of_objects(chromosome, detailed_chromosome):
    value = sum(
        int(obj["Value"]) for j, obj in enumerate(detailed_chromosome) if chromosome[j] == 1
    )
    weight = sum(
        int(obj["Weight"]) for j, obj in enumerate(detailed_chromosome) if chromosome[j] == 1
    )
    size = sum(
        float(obj["Size"]) for j, obj in enumerate(detailed_chromosome) if chromosome[j] == 1
    )
    return value, weight, size


def calculate_fitness(chromosome, detailed_chromosome):
    total_value, total_weight, total_size = __calculate_sum_of_objects(chromosome, detailed_chromosome)
    calculated_fitness = total_value if total_weight <= 220 and total_size <= 2.0 else 0
    return calculated_fitness


def evaluate_fitness_value(chromosome, detailed_chromosome):
    total_value, total_weight, total_size = __calculate_sum_of_objects(chromosome, detailed_chromosome)
    return round(total_value - (abs(220 - total_weight)) + (abs(2.0 - total_size)))


def generate_population(chromosome_data):
    population_size = 200
    population = []

    for _ in range(population_size):
        total_weight, total_size, chromosome = 0, 0.0, []

        while len(chromosome) < len(chromosome_data):
            take = random.randint(0, 1)
            weight_condition = total_weight + int(chromosome_data[len(chromosome)]["Weight"]) <= 220
            size_condition = total_size + float(chromosome_data[len(chromosome)]["Size"]) <= 2.0

            chromosome.append(take * weight_condition * size_condition)
            total_weight += int(chromosome_data[len(chromosome) - 1]["Weight"]) * chromosome[-1]
            total_size += float(chromosome_data[len(chromosome) - 1]["Size"]) * chromosome[-1]

        if chromosome not in population:
            population.append(chromosome)
            value, weight, size = __calculate_sum_of_objects(chromosome, chromosome_data)
            values.append({'gen': chromosome, 'value': value, 'weight': weight, 'size': size})

    return population, values


def mutate(array):
    mutation_point = random.randint(0, len(array) - 1)
    array[mutation_point] = 1 if array[mutation_point] == 0 else 0
    return array


def selection(chrom_dict, calculated_total_fitness):
    random_select = random.randint(1, calculated_total_fitness)
    wheel = 0
    while wheel < random_select:
        for item in chrom_dict:
            if wheel + item['value'] >= random_select:
                return item['gen']
            wheel += item['value']


def create_children_crossover(population, detailed_chromosome):
    sum_of_values = sum(item["value"] for item in population)
    children = [
        {
            "gen": first_chromosome[:break_p] + second_chromosome[break_p:],
            "value": evaluate_fitness_value(child, detailed_chromosome),
            "knapsack_fitness": calculate_fitness(child, detailed_chromosome),
        }
        for break_p in [random.randint(0, len(population))]  # Indentation corrected
        for first_chromosome, second_chromosome in zip(
            [selection(population, sum_of_values)] * 2,
            [selection(population, sum_of_values)] * 2,
        )
        for child in [first_chromosome[:break_p] + second_chromosome[break_p:]]
        for mutated_child in [
            mutate(child) if random.randint(0, 100) > 50 else child
        ]
    ]

    answers.extend(children)
    return children


if __name__ == '__main__':
    values = []
    answers = []
    objects = load_csv()
    max_weight = 220
    max_size = 2
    population = generate_population(objects)
    sorted_list = sorted(values, key=lambda x: x["value"], reverse=True)
    i = 0
    print(sorted_list)
    answers.append(sorted_list[0])
    while i < 300:
        sorted_list = create_children_crossover(sorted_list, objects)
        sorted_list = sorted_list[-200:]
        sorted_list = sorted(sorted_list, key=lambda x: x["value"], reverse=True)
        i += 1
    answers = sorted(answers, key=lambda x: x["value"], reverse=True)
    print(answers[0])
