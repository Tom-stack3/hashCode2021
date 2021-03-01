import time
import random

# streets = { "street_name": [(B, E), L, Cars_passing], ... }
streets = dict()
# list of cars path's. each car path is a list of the street names on it's way.
cars_path = []

use_gcd_method = False
use_half_method = True
use_weights_method = True
ignore_unused_streets = True


'''
With giving one second to every street:
b: 4,565,642 points
c: 1,231,878 points
d: 969,685 points
e: 661,797 points
f: 455,737 points

With giving one second to every street + ignoring unused streets in intersections:
b: 4,566,576 points + (+934)
c: 1,299,357 points + (+19,979)
d: 1,573,100 points + (+603,415)
e: 684,769 points + (+22,972)
f: 819,083 points + (+11,685)

With the GCD + removing unused streets:
b: 4,562,350 points -
c: 1,243,532 points -
d: 1,191 points -
e: 692,645 points + (+7,876)
f: 807,398 points -

With half method (giving 2 to above average) + removing unused streets:
b: 4,566,452 points -
c: 1,300,021 points + (+664)
d: 476,068 points -
e: 715,932 points + (+23,287)
f: 1,131,136 points + (+312,053)

With half method (giving 3 to above average) + removing unused streets:
b: 4,565,238 points -
c: 1,296,088 points -
d: 31,445 points -
e: 695,505 points -
f: 1,241,303 points + (+110,167)

With half method (giving 4 to above average) + removing unused streets:
b: 4,563,960 points -
c: 1,293,007 points -
d: 130,054 points -
e: 666,647 points -
f: 1,282,297 points + (+40,994)

With half method (giving 5 to above average) + removing unused streets:
b: 4,562,340 points -
c: 1,287,333 points -
d: 0 points -
e: 635,520 points -
f: 1,289,613 points + (+7,316)

With half method (choosing random between 5 and 6) + removing unused streets:
f: 1,300,888 points + (+11,275)
b,c,d,e were always worsened
'''


def gcd(my_list):
    result = my_list[0]
    for x in my_list[1:]:
        if result < x:
            temp = result
            result = x
            x = temp
        while x != 0:
            temp = x
            x = result % x
            result = temp
    return result


# we currently don't use this function
def calc_car_road_length(car_path):
    sum_of_road = 0
    for name in car_path:
        sum_of_road += streets[name][1]
    return sum_of_road


# counts the cars passing on each street and updates the streets dict() accordingly
def count_cars_on_streets():
    for current_path in cars_path:
        for i in range(len(current_path) - 1):
            # we add to the cars_passing in the right street (in the dict)
            streets[current_path[i]][2] += 1


def count_streets_on_intersection(inter_index):
    counter = 0
    intersection_streets_names = []
    # going over the streets
    for street_name in streets:
        # if the end of the street is on the intersection
        if streets[street_name][0][1] == inter_index:
            counter += 1
            intersection_streets_names.append(street_name)
    return counter, intersection_streets_names


def decide_streets_opening_on_intersection(inter_index):
    num_of_streets_on_inter, intersection_streets_names = count_streets_on_intersection(inter_index)
    streets_weights = []
    streets_names_chosen = intersection_streets_names.copy()
    for street_name in intersection_streets_names:
        cars_pass_in_street = streets[street_name][2]
        # if we want to ignore unused streets
        if ignore_unused_streets:
            # if the street is unused
            if cars_pass_in_street == 0:
                num_of_streets_on_inter -= 1
                streets_names_chosen.remove(street_name)
                continue
        # if the street is used, we add the number of cars pass it
        streets_weights.append(cars_pass_in_street)

    # if we want to use the gcd method and streets_weights list is not empty
    if use_gcd_method and streets_weights:
        current_gcd = gcd(streets_weights)
        streets_weights = [int(w / current_gcd) for w in streets_weights]

    # if we want to use the half method and streets_weights list is not empty
    elif use_half_method and streets_weights:
        cars_passes_average = sum(streets_weights)/len(streets_weights)
        for i in range(len(streets_weights)):
            if streets_weights[i] > cars_passes_average:
                streets_weights[i] = random.randint(5, 6)
            else:
                streets_weights[i] = 1

    return num_of_streets_on_inter, streets_names_chosen, streets_weights


def main():
    letters = ['b', 'c', 'e', 'f', 'd']
    letters = ['f','e','b','c']
    letters = ['f']
    for letter in letters:
        global streets
        global cars_path
        streets = dict()
        cars_path = []
        f = open("./input/" + letter + ".txt", "r")
        start_t = time.time()
        # its better to read all lines at once, rather than file.readline() in a loop.
        all_lines = f.readlines()
        first_line = all_lines[0].strip()  # f.readline()
        num_of_intersections = int(first_line.split(' ')[1])
        streets_num = int(first_line.split(' ')[2])
        cars_num = int(first_line.split(' ')[3])
        for i in range(streets_num):
            cur_street = all_lines[i + 1].strip()  # f.readline().strip()
            cur_street = cur_street.split(' ')
            streets[cur_street[2]] = [(int(cur_street[0]), int(cur_street[1])), int(cur_street[3]), 0]
        for li in range(cars_num):
            cur_car = all_lines[li + streets_num + 1].strip()  # f.readline().strip()
            cur_car = cur_car.split(' ')
            cur_path = []
            for i in range(1, len(cur_car)):
                cur_street_name = cur_car[i]
                cur_path.append(cur_street_name)
            cars_path.append(cur_path)
        f.close()
        count_cars_on_streets()
        # done initializing the information

        init_time = time.time() - start_t
        start_t = time.time()

        output = ''
        num_intersections_changed = num_of_intersections
        output += '\n'
        for inter in range(num_intersections_changed):
            count_streets, streets_chosen, streets_weights = decide_streets_opening_on_intersection(inter)
            # if the intersection has no used streets in it, we just skip it.
            if count_streets <= 0:
                num_intersections_changed -= 1
                continue
            output += str(inter) + '\n' + str(count_streets) + '\n'
            num_of_street = 0
            for street in streets_chosen:
                if use_gcd_method or use_weights_method:
                    output += street + ' ' + str(streets_weights[num_of_street]) + '\n'
                else:
                    output += street + ' 1\n'
                num_of_street += 1
        output = str(num_intersections_changed) + output
        f2 = open("./output/" + "1_" + letter + "_output.txt", "w")
        f2.write(output)
        f2.close()
        print('---------------')
        print('done with ' + letter)
        print('---------------')
        print('init time took:', init_time, 'seconds')
        print('work time took:', time.time() - start_t, 'seconds')


if __name__ == '__main__':
    main()
