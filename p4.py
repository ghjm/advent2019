#!/usr/bin/python3

low_bound = 130254
high_bound = 678275

part1_count = 0
part2_count = 0
for n in range(low_bound, high_bound+1):
    s = str(n)
    increasing = True
    has_repeat = False
    has_len_2_repeat = False
    for i in range(1, len(s)):
        if s[i-1] > s[i]:
            increasing = False
            break
        elif s[i-1] == s[i]:
            has_repeat = True
            if (i-2 < 0 or s[i-2] != s[i]) and (i+1 >= len(s) or s[i+1] != s[i]):
                has_len_2_repeat = True
    if increasing and has_repeat:
        part1_count += 1
    if increasing and has_len_2_repeat:
        part2_count += 1

print("Part 1:", part1_count)
print("Part 2:", part2_count)

