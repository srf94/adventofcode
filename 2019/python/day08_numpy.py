from utils import read_data
import numpy as np


raw = read_data(8)[0]
x_chunk = 25
y_chunk = 6
image_size = x_chunk * y_chunk


array = np.array([int(i) for i in raw])
array = array.reshape(-1, y_chunk, x_chunk)

zero_sum = (array == 0).sum(axis=2).sum(axis=1)
least_zeros = array[zero_sum.argmin()]


print("Part 1:")
print(np.sum(least_zeros == 1) * np.sum(least_zeros == 2))


output = array[0]
for layer in array[1:]:
    output = np.where(output == 2, layer, output)


print("Part 2:")
print("\n".join("".join(np.where(row, "0", " ")) for row in output))
