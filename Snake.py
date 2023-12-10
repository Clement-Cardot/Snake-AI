import copy


class Snake:

    def __init__(self, coord, default_dir):
        self.dir = default_dir
        self.head = [coord[0], coord[1]]
        self.body = []

    def step(self):

        if len(self.body) > 0:
            self.body.pop()
            self.body.insert(0, self.head)

        match self.dir:
            case "left":
                self.head = [self.head[0] - 1, self.head[1]]
            case "right":
                self.head = [self.head[0] + 1, self.head[1]]
            case "up":
                self.head = [self.head[0], self.head[1] - 1]
            case "down":
                self.head = [self.head[0], self.head[1] + 1]

    def eat(self):
        if len(self.body) == 0:
            self.body.append(copy.deepcopy(self.head))
        else:
            self.body.append(self.body[-1])
