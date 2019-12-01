import copy

key = "hxtvlmkl"

def round(lengths, num=1):
    N = 256
    cur = 0
    skip = 0
    array = range(N)

    for _ in range(num):
        for l in lengths:
            length = int(l)

            new = copy.copy(array)
            for i in range(length):
                new[(cur+length-i-1) % N] = array[(cur+i) % N]

            array = new
            cur = (cur + length + skip) % N
            skip = (skip + 1) % N

    return array

def sparse_to_dense(array):
    output = []
    for i in range(16):
        segment = array[16*i: 16*(i+1)]
        xor = reduce(lambda a, b: a ^ b, segment, 0)
        output.append(xor)
    return output

def to_hex(dense):
    hexes = []
    for i in dense:
        h = hex(i)[2:]
        hexes.append('0' + h if len(h) == 1 else h)

    return "".join(hexes)

def to_binary(hex):
    ans = bin(int(hex, 16))[2:]

    # Add initial zeros if needed
    if len(ans) < 128:
        ans = "0" * (128 - len(ans)) + ans
    return ans

def get_hash(input_):
    suffix = [17, 31, 73, 47, 23]
    ascii_ = [ord(i) for i in input_]
    ascii_ = ascii_ + suffix

    sparse = round(ascii_, num=64)
    dense = sparse_to_dense(sparse)

    return to_binary(to_hex(dense))

def set_neighbours(grid, row, col, region):
    grid[row][col] = region

    neighbours = [
        (row - 1, col), 
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)
    ]

    for r, c in neighbours:
        if (0 <= r < 128) and(0 <= c < 128) and grid[r][c] == "1":
            grid = set_neighbours(grid, r, c, region)

    return grid

grid = [list(get_hash("%s-%s" % (key, row))) for row in range(128)]

total_used = sum(sum(int(i) for i in row) for row in grid)
print "Part 1: %s" % total_used

next_region = 1
for row in range(128):
    for col in range(128):
        if grid[row][col] == "1":
            grid = set_neighbours(grid, row, col, next_region)
            next_region += 1
print "Part 2: %s" % (next_region - 1)


