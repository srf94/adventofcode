from collections import defaultdict
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

        elif row.startswith("deal"):
            increment = int(row.split()[3])
            new = [0] * N

            for i in range(N):
                new[(i * increment) % N] = cards[i]
            cards = new

        else:
            raise Exception("Unexpected row: {}".format(row))
    return cards


shuffled_cards = brute_force(raw, 10007)
print("Part 1:")
print(shuffled_cards.index(2019))


N_cards = 119315717514047
N_shuffles = 101741582076661


