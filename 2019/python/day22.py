import math
from utils import read_data


raw = read_data(22)


def brute_force(data, N):
    cards = list(range(N))
    for row in data:
        if row == "deal into new stack":
            # Reverse ordering
            cards = list(reversed(cards))

        elif row.startswith("cut"):
            cut = int(row[4:])
            if cut < 0:
                cut += N
            cards = cards[cut:] + cards[:cut]

        elif row.startswith("deal with increment"):
            increment = int(row.split()[3])
            new = [0] * N

            for i in range(N):
                new[(i * increment) % N] = cards[i]
            cards = new

        else:
            raise Exception("Unexpected row: {}".format(row))

    return cards


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    s = 0
    t = 1
    r = b
    old_s = 1
    old_t = 0
    old_r = a

    while r != 0:
        quotient = old_r / r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t)

    return old_s


def modulo_divide(N, a, b):
    # Calculate a / b (mod N)
    # 1) Find u such that bu = 1 (mod N)
    u = extended_gcd(b, N)

    # 2) Calculate a*u
    return a * u


def raise_to_power(base, power, modulo):
    power_dict = {1: base}

    for i in range(1, int(math.ceil(math.log(power, 2) + 1))):
        prev = power_dict[2 ** (i - 1)]
        power_dict[2 ** i] = (prev * prev) % modulo

    val = 1
    x = power
    while True:
        exp = 2 ** int(math.floor(math.log(x, 2)))
        val = (val * power_dict[exp]) % modulo
        x -= exp
        if x < 1:
            break

    return val


def track_position(data, N, pos):
    """
    Deal into new stack: Reverse ordering
    Equivalent to f(x) = -x-1 (mod N)

    Cut: Subtract value
    Equivalent to f(x) = x - y (mod N)

    Deal with increment: Multiply by z
    Equivalent to f(x) = xz (mod N)
    """

    for row in data:
        if row == "deal into new stack":
            pos = -pos - 1

        elif row.startswith("cut"):
            cut = int(row[4:])
            pos -= cut

        elif row.startswith("deal with increment"):
            increment = int(row.split()[3])
            pos *= increment

    return pos


def track_position_reverse(data, N, pos):
    """
    Deal into new stack: Reverse ordering
    Equivalent to f(x) = -x-1 (mod N)

    Cut: Add value
    Equivalent to f(x) = x + y (mod N)

    Deal with increment: Divide by z
    Equivalent to f(x) = x/z (mod N)
    """
    for row in reversed(data):
        if row == "deal into new stack":
            # Reverse ordering
            pos = -pos - 1

        elif row.startswith("cut"):
            cut = int(row[4:])
            pos += cut

        elif row.startswith("deal with increment"):
            increment = int(row.split()[3])
            pos = modulo_divide(N, pos, increment)

    return pos


N_cards = 10007
index = 2019
print("Part 1:")
print("Method 1 - brute force: {}".format(brute_force(raw, N_cards).index(index)))
position = track_position(raw, N_cards, index)
print("Method 2 - track position: {}".format(position % N_cards))


N_cards = 119315717514047
N_repeats = 101741582076661
index = 2020
x_0 = index
x_1 = track_position_reverse(raw, N_cards, x_0)
x_2 = track_position_reverse(raw, N_cards, x_1)

# track_position_reverse is a essentially a linear function:
# f(x) = ax + b

# Solve simultaneous equation to find a, b
a = (x_2 - x_1) / (x_1 - x_0)
b = x_1 - a * x_0

# Want f(f(...f(2020))), where f is repeated 'N_repeats' times
# Denote this as f_N(2020)

# Note
# f_N(x) = f(f_N-1(x)) = f(f_N-1(f(N-2(x))) = ...
# so
# f_N(x) = a ** N * x + b * (a ** N) / (a - 1)
a_to_n = raise_to_power(a, N_repeats, N_cards)
answer = a_to_n * x_0 + (a_to_n - 1) * b * modulo_divide(N_cards, 1, a - 1)
print("Part 2:")
print(answer % N_cards)
