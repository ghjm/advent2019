#!/usr/bin/python3
import math

reactions = dict()

with open("inputs/input14.txt", "r") as file:
    for line in (line.rstrip() for line in file):
        reagents, product = (s.strip() for s in line.split('=>'))
        prod_amount, prod_resource = (s.strip() for s in product.split(' '))
        reag = dict()
        for r in (s.strip() for s in reagents.split(',')):
            reag_amount, reag_resource = (s.strip() for s in r.split(' '))
            reag[reag_resource] = int(reag_amount)
        reactions[prod_resource] = (int(prod_amount), reag)
    reactions['ORE'] = (1, {})

def make(qty, res):
    p = list()
    prod_qty, reagents = reactions[res]
    num_reactions = math.ceil(qty / prod_qty)
    for r in reagents:
        p.extend(make(num_reactions * reagents[r], r))
    p.append([num_reactions, res])
    return p

def consolidate(plan):
    new_plan = list()
    for num_reactions, res in plan:
        for i in range(len(new_plan)):
            if new_plan[i][1] == res:
                new_plan[i][0] += num_reactions
                break
        else:
            new_plan.append([num_reactions, res])
    return new_plan

def execute(plan):
    on_hand = dict()
    for num_reactions, res in plan:
        if res not in on_hand:
            on_hand[res] = 0
        prod_amount, reagents = reactions[res]
        for r in reagents:
            if r not in on_hand:
                on_hand[r] = 0
            on_hand[r] -= reagents[r] * num_reactions
        on_hand[res] += prod_amount * num_reactions
    return on_hand

def ore_required_for_fuel(fuel):
    plan = make(fuel, 'FUEL')
    plan = consolidate(plan)
    while True:
        leftovers = execute(plan)
        for i in range(len(plan)-1, -1, -1):
            num_reactions, res = plan[i]
            if res == 'FUEL':
                continue
            prod_qty = reactions[res][0]
            needed = (num_reactions * prod_qty) - leftovers[res]
            new_num_react = math.ceil(needed / prod_qty)
            if new_num_react != plan[i][0]:
                plan[i][0] = new_num_react
                break
        else:
            break
    return plan[0][0]

print("Part 1:", ore_required_for_fuel(1))

target = 1000000000000
floor = 0
ceil = target
fuel = target//2
while True:
    ore = ore_required_for_fuel(fuel)
    if ore < target:
        floor = fuel
    elif ore > target:
        ceil = fuel
    old_fuel = fuel
    fuel = floor + (ceil-floor)//2
    if old_fuel == fuel:
        break
print("Part 2:", fuel)
