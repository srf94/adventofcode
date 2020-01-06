from collections import deque
from utils import read_data
from intcode.vm import IntcodeVM


raw = read_data(23)[0].split(",")


computers = {
    n: IntcodeVM(raw, input_=deque([n]), max_timeout=1000, default_input=-1)
    for n in range(50)
}


N = 50
nat_x_y = None
nat_y_sent = set()
part_1_seen = False


while True:
    idle = 0
    for i in range(N):
        vm = computers[i]
        dest = vm.run()
        if dest is None:
            idle += 1
            continue
        x = vm.run()
        y = vm.run()
        if dest == 255:
            nat_x_y = [x, y]
            print("nat_x_y:", nat_x_y)

            if not part_1_seen:
                print("Part 1:")
                print(y)
                part_1_seen = True
        else:
            computers[dest].input.extend([x, y])

    if idle == N:
        print("IDLE")
        print("Using nat_x_y:", nat_x_y)
        if nat_x_y[1] in nat_y_sent:
            print("Part 2:")
            print(nat_x_y[1])
            break
        computers[0].input.extend(nat_x_y)
        nat_y_sent.add(nat_x_y[1])
