text = """
deal with increment 15
cut 2234
deal with increment 30
cut -1865
deal with increment 26
cut -5396
deal with increment 69
deal into new stack
deal with increment 64
cut -5111
deal with increment 23
deal into new stack
deal with increment 53
deal into new stack
deal with increment 54
cut -5384
deal with increment 18
cut -1325
deal into new stack
deal with increment 49
cut 1174
deal with increment 71
deal into new stack
cut -5632
deal with increment 12
cut -6300
deal with increment 73
cut -1310
deal into new stack
cut 6522
deal with increment 36
deal into new stack
cut 2878
deal with increment 50
cut 7596
deal with increment 40
cut 3179
deal with increment 27
cut 538
deal with increment 46
cut 7520
deal with increment 71
cut -3471
deal with increment 5
cut -274
deal into new stack
cut -846
deal into new stack
deal with increment 60
cut -5584
deal with increment 13
deal into new stack
deal with increment 47
deal into new stack
cut -5887
deal with increment 4
cut -7255
deal with increment 54
cut 8329
deal with increment 18
cut -1293
deal into new stack
cut -2840
deal into new stack
cut -2203
deal with increment 74
cut 4303
deal with increment 42
cut -7783
deal with increment 43
cut -4040
deal with increment 21
cut -8001
deal with increment 70
cut 7243
deal with increment 41
cut 9882
deal with increment 50
cut -1588
deal with increment 35
cut 4225
deal with increment 5
cut 9281
deal with increment 57
deal into new stack
deal with increment 10
deal into new stack
cut -29
deal with increment 71
cut -3739
deal with increment 20
cut 2236
deal with increment 9
deal into new stack
cut -1199
deal with increment 33
deal into new stack
deal with increment 30
cut -2735
deal with increment 54
""".strip()


import re
import numpy as np


# 1
def deal_into_new_stack(cards):
    return cards[::-1]

def cut_cards(cards, n):
    return np.hstack((cards[n:], cards[:n]))

def deal_with_increment(cards, n):
    new_cards = cards.copy()
    new_cards[np.arange(cards.size*n, step=n) % cards.size] = cards[:]
    return new_cards


cards = np.arange(10007)
for line in text.splitlines():
    if line.startswith("deal into"):
        cards = deal_into_new_stack(cards)
    elif line.startswith("cut"):
        n = int(re.findall('-?\d+', line)[0])
        cards = cut_cards(cards, n)
    else:
        n = int(re.findall('\d+', line)[0])
        cards = deal_with_increment(cards, n)
print((cards == 2019).argmax())


# 2
def modinv(a, p):
    return pow(a, p-2, p)


def get_increment_and_firstcard_multipliers(text):
    firstcard, increment = 0, 1
    for line in text.splitlines():
        if line.startswith("deal into"):
            firstcard -= increment
            increment *= -1
        elif line.startswith("cut"):
            n = int(re.findall('-?\d+', line)[0])
            firstcard += n*increment
        else:
            n = int(re.findall('\d+', line)[0])
            increment *= modinv(n, NCARDS)
    return increment, firstcard


NCARDS = 119315717514047
NSHUFFLES = 101741582076661

a, b = get_increment_and_firstcard_multipliers(text)
final_increment = pow(a, NSHUFFLES, NCARDS)
final_firstcard = (b * (1-final_increment) * modinv(1-a, NCARDS))
print((final_firstcard + 2020 * final_increment) % NCARDS)
