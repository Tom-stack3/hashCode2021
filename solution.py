import time

streets_names = []
streets_co = []
streets_lengths = []
cars_path = []

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


def calc_car_road_length(car_path):
    sum_of_road = 0
    for road_i in car_path:
        sum_of_road += streets_lengths[road_i]
    return sum_of_road


def count_cars_on_street(street_index):
    num_of_future_cars_on_street = 0
    cars_path_without_end = [path[:-1] for path in cars_path]
    for current_car_path in cars_path_without_end:
        if street_index in current_car_path:
            num_of_future_cars_on_street += 1
    return num_of_future_cars_on_street


def count_streets_on_intersection(inter_index):
    counter = 0
    streets_indexes = []
    # going over the streets
    for coordinates in streets_co:
        # if the end of the street is on the intersection
        if coordinates[1] == inter_index:
            counter += 1
            streets_indexes.append(streets_co.index(coordinates))
    return counter, streets_indexes


def decide_streets_opening_on_intersection(inter_index):
    num_of_streets_on_inter, streets_indexes = count_streets_on_intersection(inter_index)
    streets_weights = []
    final_streets_indexes = streets_indexes.copy()
    for street_index in streets_indexes:
        count_cars = count_cars_on_street(street_index)
        # if the street is unused
        if count_cars == 0:
            num_of_streets_on_inter -= 1
            final_streets_indexes.remove(street_index)
            continue
        streets_weights.append(count_cars)
    if streets_weights:
        current_gcd = gcd(streets_weights)
        streets_weights = [int(w / current_gcd) for w in streets_weights]
    return num_of_streets_on_inter, final_streets_indexes, streets_weights


def main():
    letters = ['b', 'c', 'e', 'f']
    # d needs to be run alone! too big
    # letters = ['d']
    for letter in letters:
        global streets_names
        global streets_co
        global streets_lengths
        global cars_path
        streets_names = []
        streets_co = []
        streets_lengths = []
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
            streets_names.append(cur_street[2])
            streets_co.append((int(cur_street[0]), int(cur_street[1])))
            streets_lengths.append(int(cur_street[3]))
        for li in range(cars_num):
            cur_car = all_lines[li + streets_num + 1].strip()  # f.readline().strip()
            cur_car = cur_car.split(' ')
            cur_path = []
            for i in range(1, len(cur_car)):
                cur_street_name = cur_car[i]
                street_index = streets_names.index(cur_street_name)
                cur_path.append(street_index)
            cars_path.append(cur_path)
        f.close()
        # done initializing the information

        init_time = time.time() - start_t
        start_t = time.time()

        output = ''
        num_intersections_changed = num_of_intersections
        output += '\n'
        for inter in range(num_intersections_changed):
            count_streets, streets_indexes, streets_weights = decide_streets_opening_on_intersection(inter)
            if count_streets <= 0:
                num_intersections_changed -= 1
                continue
            output += str(inter) + '\n' + str(count_streets) + '\n'
            num_of_street = 0
            for street_index in streets_indexes:
                output += streets_names[street_index] + ' ' + str(streets_weights[num_of_street]) + '\n'
                # output += streets_names[street_index] + ' 1\n'
                num_of_street += 1
        output = str(num_intersections_changed) + output
        f2 = open("./output/" + "2_" + letter + "_output.txt", "w")
        f2.write(output)
        f2.close()
        print('---------------')
        print('done with ' + letter)
        print('---------------')
        print('init time took:', init_time)
        print('work time took:', time.time() - start_t)

if __name__ == '__main__':
    main()
