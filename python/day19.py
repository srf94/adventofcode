
with open('../input/day19.txt', 'r') as f:
    data = f.read().splitlines()

def add(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def data_(l):
    try:
        return data[l[0]][l[1]]
    except:
        return ""

steps = 0
run = True
letters = []

direction = [1, 0]
position = [0, data[0].index("|")]

while run:
    steps += 1

    if data_(position) not in ['|', '-', '+']:
        letters.append(data_(position))

    if data_(add(position, direction)) not in ["", " "]:
        position = add(position, direction)

    else:
        if direction[0] == 0:
            to_try = [[1, 0], [-1, 0]]
        else:
            to_try = [[0, 1], [0, -1]]

        for d in to_try:
            if data_(add(position, d)) not in ["", " "]:
                direction = d
                position = add(position, d)
                break
        else:
            run = False

print "Part 1: %s" % steps
print "Part 2: %s" % "".join(letters)
