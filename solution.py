streets_names = []
streets_co = []
streets_lengths = []
cars_path = []


def calc_car_road(car_path):
    sum_of_road = 0
    for road_i in car_path:
        sum_of_road += streets_lengths[road_i]
    return sum_of_road


def count_cars_on_street(street_index):
    num_of_future_cars_on_street = 0
    cars_path_without_beginning = [cars_path[i] for i in range(1, len(cars_path))]
    for current_car_path in cars_path_without_beginning:
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
    # print(num_of_streets_on_inter, streets_indexes)
    for street_index in streets_indexes:
        count_cars = count_cars_on_street(street_index)
        # if the street is unused
        if count_cars == 0:
            num_of_streets_on_inter -= 1
            streets_indexes.remove(street_index)

    # print(num_of_streets_on_inter, streets_indexes)
    return num_of_streets_on_inter, streets_indexes


def main():
    letters = ['b', 'c', 'e', 'f']
    # d needs to be run alone! to big
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
        # f = open("new_" + letter + ".txt", "r")
        f = open("./input/" + letter + ".txt", "r")
        first_line = f.readline()
        num_of_intersections = int(first_line.split(' ')[1])
        streets_num = int(first_line.split(' ')[2])
        cars_num = int(first_line.split(' ')[3])

        for _ in range(streets_num):
            cur_street = f.readline().strip()
            cur_street = cur_street.split(' ')
            streets_names.append(cur_street[2])
            streets_co.append((int(cur_street[0]), int(cur_street[1])))
            streets_lengths.append(int(cur_street[3]))
        for _ in range(cars_num):
            cur_car = f.readline().strip()
            cur_car = cur_car.split(' ')
            cur_path = []
            for i in range(1, len(cur_car)):
                cur_street_name = cur_car[i]
                street_index = streets_names.index(cur_street_name)
                cur_path.append(street_index)
            cars_path.append(cur_path)
        f.close()
        # done initializing the information
        print('path:', cars_path)
        # cars_path.sort(key=calc_car_road)
        # print('new path:', cars_path)
        f.close()
        f2 = open("./output/" + "1_" + letter + "_output.txt", "w")
        '''
        first_car_path = cars_path[0]
        print(first_car_path)
        num_intersections_changed = len(first_car_path) - 1
        f2.write(str(num_intersections_changed) + '\n')
        first_car_path.pop()
        for street in first_car_path:
            cur_inters = streets_co[street]
            print(cur_inters)
            f2.write(str(cur_inters[1]) + '\n1\n')
            cur_street_to_open = streets_names[street]
            f2.write(cur_street_to_open + ' 1\n')
        '''
        output = ''
        num_intersections_changed = num_of_intersections
        # f2.write(str(num_intersections_changed) + '\n')
        output += '\n'
        for inter in range(num_intersections_changed):
            count_streets, streets_indexes = decide_streets_opening_on_intersection(inter)
            if count_streets <= 0:
                num_intersections_changed-=1
                continue
            #f2.write(str(inter) + '\n' + str(count_streets) + '\n')
            output += str(inter) + '\n' + str(count_streets) + '\n'
            for street_index in streets_indexes:
                # f2.write(streets_names[street_index] + ' 1\n')
                output += streets_names[street_index] + ' 1\n'
        output = str(num_intersections_changed) + output
        f2.write(output)
        f2.close()


if __name__ == '__main__':
    main()
