import time

# streets = { "street_name": [(B, E), L, Cars_passing], ... }
streets = dict()
# list of cars path's. each car path is a list of the street names on it's way.
cars_path = []

use_gcd_method = True
use_weights_method = False
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
        streets_weights.append(cars_pass_in_street)
    # if we want to use the gcd method and streets_weights list is not empty
    if use_gcd_method and streets_weights:
        current_gcd = gcd(streets_weights)
        streets_weights = [int(w / current_gcd) for w in streets_weights]
    return num_of_streets_on_inter, streets_names_chosen, streets_weights


def main():
    letters = ['b', 'c', 'e', 'f', 'd']
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
        print('init time took:', init_time)
        print('work time took:', time.time() - start_t)


'''


regular:
init time took: 120.10809779167175
work time took: 515.7313907146454

faster:
init time took: 4.666066884994507
work time took: 686.1625516414642
'''

if __name__ == '__main__':
    main()
