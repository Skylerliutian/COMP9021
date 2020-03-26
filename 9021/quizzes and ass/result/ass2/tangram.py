import numpy as np
import re
from math import sqrt


def available_coloured_pieces(file):
    content = file.read()

    all_points = re.findall(r'M[\s\d\w]*z', content)
    arrange_points = []

    all_colors = re.findall(r'"\w*"', content)

    for i in range(len(all_colors)):
        all_colors[i] = all_colors[i][1:-1]

    for i in all_points:
        sort_1 = re.findall(r'\d*', i)

        while '' in sort_1:
            sort_1.remove('')
        for s in range(len(sort_1)):
            sort_1[s] = int(sort_1[s])
        sort = np.array(sort_1)
        sort.resize(int(len(sort)/2), 2)
        arrange_points.append(sort)

    return arrange_points, all_colors


def same_colors(points1, points2):
    colors1 = points1[1]
    colors2 = points2[1]
    if set(colors1) == set(colors2):
        return True
    else:
        return False


def are_valid(pair_points):
    if len(pair_points[0]) == 0:
        return False
    if len(pair_points[0][0]) < 3:
        return False
    count_i = 0
    for i in range(len(pair_points[0])):
        count_j = 0
        length = len(pair_points[0][i])
        for j in range(length - 1):
            if (pair_points[0][i][0] == pair_points[0][i][-1]).all():
                return False
            else:
                if (pair_points[0][i][j+1] == pair_points[0][i][j]).all():
                    return False
                # 如果平行与x轴
                if pair_points[0][i][j][0] == pair_points[0][i][j+1][0]:
                    x = pair_points[0][i][j][0]
                    if all(pair_points[0][i][n][0] > x for n in range(j + 2, length)) and all(pair_points[0][i][n][0] > x for n in range(0, j)):
                        count_j += 1
                    elif all(pair_points[0][i][n][0] < x for n in range(j + 2, length)) and all(pair_points[0][i][n][0] < x for n in range(0, j)):
                        count_j += 1
                # 如果平行与y轴
                elif pair_points[0][i][j][1] == pair_points[0][i][j+1][1]:
                    y = pair_points[0][i][j][1]
                    if all(pair_points[0][i][n][1] > y for n in range(j + 2, length)) and all(pair_points[0][i][n][1] > y for n in range(0, j)):
                        count_j += 1
                    elif all(pair_points[0][i][n][1] < y for n in range(j + 2, length)) and all(pair_points[0][i][n][1] < y for n in range(0, j)):
                        count_j += 1
                # 其他情况
                else:
                    k = (pair_points[0][i][j+1][1] - pair_points[0][i][j][1]) / (pair_points[0][i][j+1][0] - pair_points[0][i][j][0])
                    b = pair_points[0][i][j][1] - k * pair_points[0][i][j][0]
                    if all(pair_points[0][i][n][1] > k * pair_points[0][i][n][0] + b for n in range(j + 2, length)) and all(pair_points[0][i][n][1] > k * pair_points[0][i][n][0] + b for n in range(0, j)):
                        count_j += 1
                    elif all(pair_points[0][i][n][1] < k * pair_points[0][i][n][0] + b for n in range(j + 2, length)) and all(pair_points[0][i][n][1] < k * pair_points[0][i][n][0] + b for n in range(0, j)):
                        count_j += 1
        if count_j == length - 1:
            count_i += 1
    if count_i == len(pair_points[0]):
        return True
    else:
        return False


def analyze_length(points):

    length_list = []
    for i in range(len(points[0])):
        len_list = []
        for j in range(len(points[0][i]) - 1):
            length = int(sqrt(((points[0][i][j][0] - points[0][i][j+1][0]) ** 2) + ((points[0][i][j][1] - points[0][i][j+1][1]) ** 2)))
            len_list.append(length)
        len_list.append(int(sqrt(((points[0][i][0][0] - points[0][i][-1][0]) ** 2) + ((points[0][i][0][1] - points[0][i][-1][1]) ** 2))))
        length_list.append(len_list)
    return length_list


def are_identical_sets_of_coloured_pieces(points1, points2):
    length_1 = analyze_length(points1)
    length_2 = analyze_length(points2)
    compare_len_2 = analyze_length(points2)
    if len(length_1) != len(length_2):
        return False
    count = 0
    for i in range(len(length_1)):
        for k in range(len(length_1[i])):
            flag = 0
            for j in range(len(length_2)):
                if length_1[i][k:] + length_1[i][:k] == length_2[j] or length_1[i][::-1][k:] + length_1[i][::-1][:k] == length_2[j]:
                    flag = 1
            if flag == 1:
                count += 1
                break

    if count == len(compare_len_2) and count == len(length_1) and same_colors(points1, points2):
        return True
    else:
        return False


def judge_inside(tangram, shape):
    # 如果shape的长度不为1，直接return False
    if len(shape[0]) != 1:
        return False
    line_list = []
    truth_list = []
    nb_of_elements = 0
    for i in range(len(tangram[0])):
        for j in range(len(tangram[0][i])):
            nb_of_elements += 1
    for i in range(-1, len(shape[0][0]) - 1):
        if shape[0][0][i + 1][0] == shape[0][0][i][0]:
            line_list.append([shape[0][0][i][0]])
        else:
            k = (shape[0][0][i + 1][1] - shape[0][0][i][1]) / (shape[0][0][i + 1][0] - shape[0][0][i][0])
            b = shape[0][0][i][1] - k * shape[0][0][i][0]
            line_list.append([int(k), int(b)])
    for i in range(len(tangram[0])):
        for j in range(len(tangram[0][i])):
            nb_of_points = 0
            for k in range(len(line_list)):
                if len(line_list[k]) != 1:
                    if line_list[k][0] == 0:
                        # 在平行与y轴边上 不用接着判断
                        if tangram[0][i][j][1] == shape[0][0][k][1] and min(shape[0][0][k][0], shape[0][0][k - 1][0]) <= tangram[0][i][j][0] <= max(shape[0][0][k][0], shape[0][0][k - 1][0]):
                            flag = True
                            truth_list.append(flag)
                            nb_of_points = 0
                            break
                        else:
                            continue
                    elif line_list[k][0] != 0:

                        if min(shape[0][0][k][1], shape[0][0][k - 1][1]) <= tangram[0][i][j][1] <= max(shape[0][0][k][1], shape[0][0][k - 1][1]) and tangram[0][i][j][0] <= min(shape[0][0][k][0], shape[0][0][k - 1][0]):
                            nb_of_points += 1
                        else:
                            continue
                if len(line_list[k]) == 1:
                    if min(shape[0][0][k][1], shape[0][0][k - 1][1]) <= tangram[0][i][j][1] <= max(shape[0][0][k][1], shape[0][0][k - 1][1]):
                        if tangram[0][i][j][0] < line_list[k][0]:
                            nb_of_points += 1
                        elif tangram[0][i][j][0] == line_list[k][0]:
                            flag = True
                            truth_list.append(flag)
                            nb_of_points = 0
                            break
                    else:
                        continue
            if nb_of_points != 0:
                if nb_of_points % 2 != 0:
                    flag = True
                    truth_list.append(flag)
                else:
                    flag = False
                    truth_list.append(flag)

    if len(truth_list) != nb_of_elements:
        return False
    else:
        if False in truth_list:
            return False
        else:
            return True


def get_area(points):
    area = 0
    for i in range(len(points[0])):
        a = 0
        b = 0
        for j in range(-1, len(points[0][i]) - 1):
            a += points[0][i][j][0] * points[0][i][j + 1][1]
            b += points[0][i][j][1] * points[0][i][j + 1][0]
        area += abs(a - b) / 2
    return area


def judge_cross(point_1, point_2, point_3):
    x_1 = point_2[0] - point_1[0]
    x_2 = point_3[0] - point_1[0]
    y_1 = point_2[1] - point_1[1]
    y_2 = point_3[1] - point_1[1]
    cross = x_1 * y_2 - x_2 * y_1
    return cross


def judge_overlap(points):
    if len(points[0]) == 1:
        return True
    for i in range(len(points[0])):
        for j in range(-1, len(points[0][i]) - 1):
            for k in range(i + 1, len(points[0])):
                for m in range(-1, len(points[0][k]) - 1):
                    cross_1 = judge_cross(points[0][i][j], points[0][i][j + 1], points[0][k][m])
                    cross_2 = judge_cross(points[0][i][j], points[0][i][j + 1], points[0][k][m + 1])
                    cross_3 = judge_cross(points[0][k][m], points[0][k][m + 1], points[0][i][j])
                    cross_4 = judge_cross(points[0][k][m], points[0][k][m + 1], points[0][i][j + 1])
                    if cross_1 * cross_2 < 0 and cross_3 * cross_4 < 0:
                        return False
    return True


def is_solution(tangram, shape):

    if get_area(tangram) == get_area(shape) and judge_inside(tangram, shape) and judge_overlap(tangram):
        return True
    else:
        return False



