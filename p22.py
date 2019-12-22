#!/usr/bin/pypy3
import sys

shuffle_cmds = list()
with open("inputs/input22.txt", "r") as file:
    for line in (s.rstrip() for s in file.readlines()):
        if line.startswith("deal into new stack"):
            shuffle_cmds.append(('dins', 0))
        elif line.startswith("cut"):
            shuffle_cmds.append(('cut', int(line[4:])))
        elif line.startswith("deal with increment"):
            shuffle_cmds.append(('dwi', int(line[20:])))


class Deck():
    def __init__(self, size):
        self.deck = list(range(size))

    def deal_into_new_stack(self, _):
        self.deck.reverse()

    def cut(self, cut):
        d1 = self.deck[0:cut]
        d2 = self.deck[cut:]
        self.deck = d2 + d1

    def deal_with_increment(self, incr):
        new_deck = [0] * len(self.deck)
        for i in range(len(self.deck)):
            new_pos = (i*incr) % len(self.deck)
            new_deck[new_pos] = self.deck[i]
        self.deck = new_deck

    def run_shuffle(self):
        scfunc = {
                'dins': self.deal_into_new_stack,
                'cut': self.cut,
                'dwi': self.deal_with_increment,
                }
        for sc, value in shuffle_cmds:
            scfunc[sc](value)

deck = Deck(10007)
deck.run_shuffle()
print("Part 1:", deck.deck.index(2019))

