import itertools
from utils import read_data
from PIL import Image


raw = read_data(8)[0]
x_chunk = 25
y_chunk = 6
image_size = x_chunk * y_chunk
fewest_zero = image_size
images = []
result = None


for i in range(0, len(raw), image_size):
    layer = list(raw[i: i+image_size])
    num_zero = sum(i == '0' for i in layer)
    num_1 = sum(i == '1' for i in layer)
    num_2 = sum(i == '2' for i in layer)

    if num_zero < fewest_zero:
        result = num_1 * num_2
        fewest_zero = num_zero

    images.append(
        [list(layer[j: j+x_chunk]) for j in range(0, image_size, x_chunk)]
    )


print("Part 1:")
print(result)


img = Image.new(mode='1', size=(x_chunk, y_chunk))
for x, y in itertools.product(range(x_chunk), range(y_chunk)):
    i = 0
    while True:
        pixel = images[i][y][x]
        if pixel != '2':
            img.putpixel((x, y), int(pixel))
            break
        i += 1


print("Part 2:")
img.show()
