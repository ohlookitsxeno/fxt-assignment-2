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