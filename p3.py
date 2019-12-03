#!/usr/bin/python3

with open("inputs/input3.txt", "r") as file:
    content = file.readlines()

pathpoints_list = []
distances_list = []
for line in content:
    path = line.rstrip().split(',')
    pathpoints = set()
    distances = dict()
    cur_pos = (0,0)
    total_distance = 0
    for step in path:
        direction = step[0]
        dist = int(step[1:])
        dx, dy = { 'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0) }[direction]
        for i in range(dist):
            cur_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
            pathpoints.add(cur_pos)
            total_distance += 1
            if cur_pos not in distances:
                distances[cur_pos] = total_distance
    pathpoints_list.append(pathpoints)
    distances_list.append(distances)

intersect = pathpoints_list[0].intersection(pathpoints_list[1])

best_manhattan = None
best_total_dist = None
for p in intersect:
    manhattan = abs(p[0]) + abs(p[1])
    total_dist = sum([d[p] for d in distances_list])
    if best_manhattan is None or manhattan < best_manhattan:
        best_manhattan = manhattan
    if best_total_dist is None or total_dist < best_total_dist:
        best_total_dist = total_dist

print('Part 1:', best_manhattan)
print('Part 2:', best_total_dist)
