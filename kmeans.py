import random
import math as m

def step_points(points, centroids):
    newp = []
    for p in points:
        mindist = dist(p, centroids[0])
        minc = 0
        for c in range(len(centroids)):
            d = dist(p,centroids[c])
            if d < mindist:
                mindist = d
                minc = c
        newp.append((p[0], p[1], minc))
    return newp

def dist(p, c):
    return m.sqrt(((p[0] - c[0]) ** 2) + ((p[1] - c[1]) ** 2))

def step_centroids(points, centroids):
    newc = []
    for c in range(len(centroids)):
        sx = sy = num = 0.
        for p in points:
            if p[2] == c:
                sx = sx + p[0]
                sy = sy + p[1]
                num = num + 1
        if num > 0:
            newc.append(((sx/num), (sy/num), -1))
        else:
            newc.append(centroids[c])
    return newc

def reset_points(points):
    newp = []
    for p in points:
        newp.append((p[0], p[1], -1))
    return newp

def generate_dataset(n):
    print("meow2")
    points = []
    for _ in range(n):
        points.append((random.uniform(-10,10), random.uniform(-10,10), -1))
    return points

def init_random(points, n):
    cent = {(points[random.randint(0, len(points)-1)])}

    while len(cent) < n:
        cent.add(points[random.randint(0, len(points)-1)])
    return list(cent)

def init_far(points, n):
    cent = {(points[random.randint(0, len(points)-1)])}
    while len(cent) < n:
        maxdist = maxp = 0
        for p in range(len(points)):
            mind = dist(points[p], list(cent)[0])
            for c in cent:
                d = dist(points[p], c)
                if d < mind:
                    mind = d
            if mind > maxdist:
                maxdist = mind
                maxp = p
        cent.add(points[maxp])

    return list(cent)

def init_kmeans(points, n):
    cent = {(points[random.randint(0, len(points)-1)])}

    while len(cent) < n:
        dists = []
        for p in range(len(points)):
            mind = dist(points[p], list(cent)[0])
            for c in cent:
                d = dist(points[p], c)
                if d < mind:
                    mind = d
            dists.append(mind)
        psel = random.choices(points, weights=dists, k=1)[0]
        cent.add(psel)
    return list(cent)