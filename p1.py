#!/usr/bin/python3

with open("inputs/input1.txt", "r") as file:
    content = file.readlines()

total_basic_fuel = 0
total_extended_fuel = 0

for line in content:
    mass = int(line)
    fuel = mass//3 - 2
    total_basic_fuel += fuel
    while fuel > 0:
        total_extended_fuel += fuel
        fuel = fuel//3 - 2

print(total_basic_fuel)
print(total_extended_fuel)
