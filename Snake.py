import copy


class Snake:

    def __init__(self, coord, default_dir):
        self.dir = default_dir
        self.head = [coord[0], coord[1]]
        self.body = []
        self.grow = False

    def step(self, action):

        if len(self.body) > 0:
            self.body.pop()
            self.body.insert(0, self.head)

        match action:
            case 0:  # Left
                self.dir = self.dir - 1
                if self.dir == -1:
                    self.dir = 3
            case 1:  # Right
                self.dir = self.dir + 1
                if self.dir == 4:
                    self.dir = 0
            case 2:  # Do Nothing
                pass

        match self.dir:
            case 0:  # Left
                self.head = [self.head[0] - 1, self.head[1]]
            case 1:  # Up
                self.head = [self.head[0], self.head[1] - 1]
            case 2:  # Right
                self.head = [self.head[0] + 1, self.head[1]]
            case 3:  # Down
                self.head = [self.head[0], self.head[1] + 1]

    def eat(self):
        if len(self.body) == 0:
            self.body.append(copy.deepcopy(self.head))
        else:
            self.body.append(self.body[-1])
