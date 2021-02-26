import random


def choose_best_car(cars_):
    # choice = max(cars, key=len)
    # choice = min(cars, key=len)
    choice = random.choice(cars_)
    return choice


# for the Google Hash code competition
letters = ['b', 'c', 'd', 'e', 'f']
for letter in letters:
    f = open(letter + ".txt", "r")
    first_line = f.readline()
    streets_num = int(first_line.split(' ')[2])
    cars_num = int(first_line.split(' ')[3])
    print(streets_num)
    streets = []
    for _ in range(streets_num):
        streets.append(f.readline())
    cars = []
    for _ in range(cars_num):
        cars.append(f.readline())
    best_car = choose_best_car(cars)
    print(best_car)
    used_streets = []
    for s in streets:
        # if the street is used
        if s.split(' ')[2] in best_car:
            used_streets.append(s)
    f.close()
    f2 = open("new_" + letter + ".txt", "w")
    first_line = first_line.split(' ')
    first_line[3] = '1'
    first_line[2] = str(len(used_streets))
    first_line = ' '.join(first_line)
    print(first_line)
    f2.write(first_line)
    for s in used_streets:
        f2.write(s)
    f2.write(best_car)
    print(len(used_streets))
