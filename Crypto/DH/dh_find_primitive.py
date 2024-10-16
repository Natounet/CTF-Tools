import requests
from itertools import permutations

p = <p>

def is_primitive_root(g, p):
    required_set = set(num for num in range(1, p) if gcd(num, p) == 1)
    actual_set = set(pow(g, powers, p) for powers in range(1, p))
    return required_set == actual_set

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_smallest_primitive_root(p):
    for g in range(2, p):
        if is_primitive_root(g, p):
            return g
    return None

smallest_primitive_root = find_smallest_primitive_root(p)
print(f"The smallest primitive root of the field {p} is {smallest_primitive_root}")