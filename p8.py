#!/usr/bin/python3
import sys

digits = list()
with open("inputs/input8.txt", "r") as file:
    for line in (line.rstrip() for line in file):
        digits.extend([int(c) for c in line])

image_size_x = 25
image_size_y = 6
image_size_total = image_size_x * image_size_y

if len(digits) % image_size_total != 0:
    print("Image is not multiple of layer size")
    sys.exit(0)

layers = list()
for i in range(len(digits) // image_size_total):
    layer = digits[i*image_size_total:(i+1)*image_size_total]
    layers.append(layer)

zero_counts = [len([n for n in layer if n==0]) for layer in layers]
min_zero_layer = zero_counts.index(min(zero_counts))
counts = [len([n for n in layers[min_zero_layer] if n==val]) for val in [1,2]]
print("Part 1:", counts[0]*counts[1])

print("Part 2:")
image = [0] * image_size_total
for i in range(len(layers)-1, -1, -1):
    for j in range(image_size_total):
        if layers[i][j] != 2:
            image[j] = layers[i][j]

pix_chars = [' ', '#', '?']
for y in range(image_size_y):
    for x in range(image_size_x):
        pixel = image[y*image_size_x + x]
        print(pix_chars[pixel], end='')
    print('')

