import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def compareX(a, b):
    p1 = a
    p2 = b
    return (p1.x - p2.x)


def compareY(a, b):
    p1 = a
    p2 = b
    return (p1.y - p2.y)


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def bruteForce(P, n):
    min_dist = float("inf")
    closest_pair = None
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(P[i], P[j])
            if d < min_dist:
                min_dist = d
                closest_pair = (P[i], P[j])
    return min_dist, closest_pair


def stripClosest(strip, size, d):
    min_dist = d[0]
    closest_pair = d[1]
    strip = sorted(strip, key=lambda point: point.y)

    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= min_dist:
                break
            d_new = dist(strip[i], strip[j])
            if d_new < min_dist:
                min_dist = d_new
                closest_pair = (strip[i], strip[j])
    return min_dist, closest_pair


def closestUtil(P, n):
    if n <= 3:
        return bruteForce(P, n)
    mid = n // 2
    midPoint = P[mid]
    dl = closestUtil(P[:mid], mid)
    dr = closestUtil(P[mid:], n - mid)
    if dl[0] < dr[0]:
        d = dl
    else:
        d = dr

    strip = []
    for i in range(n):
        if abs(P[i].x - midPoint.x) < d[0]:
            strip.append(P[i])
    strip_result = stripClosest(strip, len(strip), d)
    return strip_result if strip_result[0] < d[0] else d


def closest(P, n):
    P = sorted(P, key=lambda point: point.x)
    return closestUtil(P, n)


def read_pairs_from_file(file_name):
    pairs = set()  # Use a set to track unique pairs

    with open(file_name, "r") as file:
        for line in file:
            x, y = line.split()
            pair = (int(x), int(y))  # Store x and y as integers
            pairs.add(pair)  # Set automatically handles duplicates

    return list(pairs)  # Convert the set back to a list


if __name__ == "__main__":
    i = 1
    while i <= 10:
        file_name = f'./cpp_inputs/cpp_input_{i}.txt'
        values = read_pairs_from_file(file_name)
        P = [Point(x, y) for x, y in values]
        n = len(P)
        result = closest(P, n)
        print(
            f"The smallest distance is {result[0]} between points ({result[1][0].x}, {result[1][0].y}) and ({result[1][1].x}, {result[1][1].y})"
        )
        i += 1
