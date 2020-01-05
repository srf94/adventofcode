from collections import deque


class IntcodeVM(object):
    def __init__(
        self, D, input_=None, mutate_input=None, max_timeout=None, default_input=None
    ):
        self.D = {loc: int(i) for loc, i in enumerate(D)}
        self.pointer = 0
        self.relative_base = 0
        self.max_timeout = max_timeout
        self.default_input = default_input

        if input_ is None:
            self.input = deque()
        else:
            self.input = input_

        if mutate_input is not None:
            for k, v in mutate_input.items():
                self.D[k] = v

        self.args = None
        self.modes = None

    @property
    def D_list(self):
        # Useful for tests
        return [self.D[i] for i in range(max(self.D) + 1)]

    def get_input(self):
        if isinstance(self.input, deque):
            try:
                return self.input.popleft()
            except:
                return self.default_input

        return self.input

    def prep_instruction(self):
        i = self.D.get(self.pointer, 0)
        opcode = i % 100
        self.modes = [
            (i // 100) % 10,
            (i // 1000) % 10,
            (i // 10000) % 10,
        ]
        self.args = [
            self.D.get(self.pointer + 1, 0),
            self.D.get(self.pointer + 2, 0),
            self.D.get(self.pointer + 3, 0),
        ]
        return opcode

    def read(self, loc):
        try:
            value = self.args[loc]
        except IndexError:
            value = 0

        mode = self.modes[loc]
        if mode == 0:
            return self.D.get(value, 0)
        if mode == 1:
            return value
        return self.D.get(value + self.relative_base, 0)

    def write(self, loc, value):
        mode = self.modes[loc]
        if mode == 0:
            self.D[self.args[loc]] = value
        if mode == 1:
            raise Exception("Tried to write in mode 1!")
        self.D[self.args[loc] + self.relative_base] = value

    def run(self, input_=None):
        if input_ is not None:
            self.input = input_

        counter = 0
        while True:
            counter += 1
            if self.max_timeout is not None and self.max_timeout < counter:
                return None

            opcode = self.prep_instruction()

            if opcode == 1:
                self.write(2, self.read(0) + self.read(1))
                self.pointer += 4

            elif opcode == 2:
                self.write(2, self.read(0) * self.read(1))
                self.pointer += 4

            elif opcode == 3:
                self.write(0, self.get_input())
                self.pointer += 2

            elif opcode == 4:
                value = self.read(0)
                self.pointer += 2
                return value

            elif opcode == 5:
                value = self.read(0)
                if value != 0:
                    self.pointer = self.read(1)
                else:
                    self.pointer += 3

            elif opcode == 6:
                value = self.read(0)
                if value == 0:
                    self.pointer = self.read(1)
                else:
                    self.pointer += 3

            elif opcode == 7:
                self.write(2, 1 if self.read(0) < self.read(1) else 0)
                self.pointer += 4

            elif opcode == 8:
                self.write(2, 1 if self.read(0) == self.read(1) else 0)
                self.pointer += 4

            elif opcode == 9:
                self.relative_base += self.read(0)
                self.pointer += 2

            elif opcode == 99:
                return

            else:
                raise Exception("Unexpected op code: {}".format(opcode))

    def collect_all_outputs(self):
        outputs = []
        while True:
            out = self.run()
            if out is None:
                break
            outputs.append(out)
        return outputs
