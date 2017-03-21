from logging import info


def get_levenshtein_dist(name1, name2):
    length1 = len(name1)+1
    length2 = len(name2)+1
    matrix = [[0 for x in range(length2 + 1)] for y in range(length1 + 1)]

    temp = '          '
    for s in name2:
        temp = temp + s + '   '

    x = y = 0
    weight = 1
    for x in range(length1):
        temp = ' ' + name1[x]
        for y in range(length2):

            if x is -1:
                matrix[x][y] = matrix[x][y - 1] + weight
                if y is -1:
                    matrix[x][y] = 0
            elif y is -1:

                matrix[x][y] = matrix[x - 1][y] + weight

            elif name1[x] is name2[y]:
                matrix[x][y] = matrix[x - 1][y - 1]
            else:
                matrix[x][y] = min(matrix[x - 1][y - 1], matrix[x][y - 1], matrix[x - 1][y]) + weight

            temp = temp + (2 - len(str(matrix[x][y]))) * ' ' + str(matrix[x][y]) + "  "

    return matrix[x][y]


def is_levenshtein_fit(name1, name2):
    diff = abs(len(name1) - len(name2))+2

    lev_dist = get_levenshtein_dist(name1, name2)

    result = lev_dist <= diff

    if result:
        strs = ("#ACCEPT ")
        info("is_levenshtein_fit " + strs + str(lev_dist) + "/" + str(diff) + " //// " + name1 + "  ////  " + name2)
    # no else

    return result

print(get_levenshtein_dist("Peter", "Petr"))