lower = 134564
upper = 585159


part_1_total = 0
part_2_total = 0
for num_int in range(lower, upper + 1):
    num = str(num_int)
    assert len(num) == 6

    adjacent = any(num[i] == num[i + 1] for i in range(5))
    increasing = all(num[i] <= num[i + 1] for i in range(5))

    if adjacent and increasing:
        part_1_total += 1

    # Pad number to simplify indexing
    p = "p{}p".format(num)
    run_of_two = False
    for i in range(1, 6):
        if p[i - 1] != p[i] and p[i] == p[i + 1] and p[i + 1] != p[i + 2]:
            run_of_two = True
            break

    if increasing and run_of_two:
        part_2_total += 1

print("Part 1:")
print(part_1_total)

print("Part 2:")
print(part_2_total)
