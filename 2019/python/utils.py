def read_data(day, year=2019):
    filename = "../input/day{0:02d}.txt".format(day)
    with open(filename, "r") as f:
        return f.read().splitlines()
