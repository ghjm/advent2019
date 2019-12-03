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
        if direction == 'U':
            dx = 0
            dy = -1
        elif direction == 'D':
            dx = 0
            dy = 1
        elif direction == 'L':
            dx = -1
            dy = 0
        elif direction == 'R':
            dx = 1
            dy = 0
        for i in range(dist):
            cur_pos = (cur_pos[0] + dx, cur_pos[1] + dy)
            pathpoints.add(cur_pos)
            total_distance += 1
            if cur_pos not in distances:
                distances[cur_pos] = total_distance
    pathpoints_list.append(pathpoints)
    distances_list.append(distances)

intersect = pathpoints_list[0].intersection(pathpoints_list[1])

# Part 1
best_so_far = None
for p in intersect:
    manhattan = abs(p[0]) + abs(p[1])
    if best_so_far is None or manhattan < best_so_far:
        best_so_far = manhattan
print(best_so_far)
    
# Part 2
best_so_far = None
for p in intersect:
    total_dist = sum([d[p] for d in distances_list])
    if best_so_far is None or total_dist < best_so_far:
        best_so_far = total_dist
print(best_so_far)
