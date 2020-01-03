from utils import read_data
from collections import deque
from itertools import combinations
from intcode_vm import IntcodeVM


raw = read_data(25)[0].split(",")
vm = IntcodeVM(raw)


def cc(word):
    command = "Command?\n"
    output = ""
    word_ord = deque(ord(i) for i in word + "\n")
    while True:
        res = vm.run(word_ord)
        if res is None:
            print("Part 1:")
            print(output)
            break

        res = chr(res)
        output += res

        if output[-9:] == command:
            break
    return output


cc("inv")
cc("south")
cc("take boulder")
cc("east")
cc("take food ration")
cc("west")
cc("west")
cc("take asterisk")
cc("east")
cc("north")
cc("east")
cc("take candy cane")
cc("north")
cc("east")
cc("north")
cc("take mug")
cc("south")
cc("west")
cc("north")
cc("take mutex")
cc("north")
cc("take prime number")
cc("south")
cc("south")
cc("south")
cc("east")
cc("north")
cc("take loom")
cc("south")
cc("east")
cc("south")
cc("east")
cc("east")
cc("north")
cc("inv")


items = [
    "prime number",
    "candy cane",
    "loom",
    "asterisk",
    "food ration",
    "boulder",
    "mutex",
    "mug",
]


finished = False
for l in range(1, 9):
    if finished:
        break
    for i_list in combinations(items, l):
        for ii in i_list:
            cc("drop {}".format(ii))
        out = cc("north")
        if "Alert!" not in out:
            finished = True
            break
        for ii in i_list:
            cc("take {}".format(ii))
