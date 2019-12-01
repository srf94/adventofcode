
with open('../input/day21.txt', 'r') as f:
    data = f.read().splitlines()


board = """.#.
..#
###""".splitlines()


patterns = {}
for i in data:
    in_, out = i.split(" => ")
    in_ = in_.split("/")
    out = out.split("/")

    ll = len(in_)
    in_rot = ["".join(in_[j][i] for j in range(ll)) for i in range(ll)]

    for pattern in [in_, in_rot]:
        patterns[tuple(pattern)] = out
        patterns[tuple(list(reversed(pattern)))] = out

        pattern_rev = [i[::-1] for i in pattern]
        patterns[tuple(pattern_rev)] = out
        patterns[tuple(list(reversed(pattern_rev)))] = out


for count in range(18):
    l = len(board)
    if l % 2 == 0:
        N = 2
    elif l % 3 == 0:
        N = 3

    new_board = []
    for i in range(l/N):
        rows = board[N*i: N*i+N]
        new_row = []

        for j in range(l/N):
            square = [r[N*j: N*j+N] for r in rows]
            new_row.append(patterns[tuple(square)])

        new_row = ["".join(new_row[ii][jj] for ii in range(l/N)) for jj in range(N+1)]

        for row in new_row:
            new_board.append(row)

    board = new_board

    if count == 4:
        print "Part 1: %s" % sum(sum(i=="#" for i in r) for r in board)
    elif count == 17:
        print "Part 2: %s" % sum(sum(i=="#" for i in r) for r in board)
