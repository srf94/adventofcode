import numpy as np
from utils import read_data


def get_base_pattern_expanded(base, repeat, data_shape):
    expanded = [v for v in base for _ in range(repeat)]

    num_copies = 1 + (data_shape // len(expanded))
    full = [i for _ in range(num_copies) for i in expanded]

    return np.array(full[1: data_shape+1], dtype=int)


def create_matrix(input_signal, base_pattern):
    dim = input_signal.shape[0]
    m = np.zeros((dim, dim), dtype=int)

    for loc in range(input_signal.shape[0]):
        pattern = get_base_pattern_expanded(base_pattern, loc+1, dim)
        m[loc] = np.array(pattern)

    return m


def get_raw_from_offset(size, raw):
    raw = raw.tolist()
    raw_len = len(raw)
    assert 0.5 * raw_len < offset

    num_copies = size - offset // raw_len - 1
    tail_raw = offset - (offset // raw_len)*raw_len

    full = raw[tail_raw:]
    for _ in range(num_copies):
        full.extend(raw)
    return np.array(full)


def answer(signal):
    print("".join(str(i) for i in signal[:8]))


raw = read_data(16)[0]
offset = int(raw[:7])
raw = np.array(list(raw), dtype=int)
signal = np.array(raw, dtype=int)
base_pattern = [0, 1, 0, -1]


matrix = create_matrix(signal, base_pattern)
for _ in range(100):
    signal = np.abs((matrix * signal).sum(axis=1)) % 10


print("Part 1:")
answer(signal)


signal = get_raw_from_offset(10000, raw)


for _ in range(100):
    new = np.zeros(signal.shape, dtype=int)
    new[:] = signal.sum()
    new[1:] = new[1:] - signal.cumsum()[:-1]
    signal = np.abs(new) % 10


print("Part 2:")
answer(signal)
