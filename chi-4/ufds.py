class UFDS:
    point = []
    rank = []
    disjoint = 0

    parents = set()
    sizes = None
    changed = False

    def __init__(self, n):
        self.point = [i for i in range(0, n)]
        self.rank = [0 for i in range(0, n)]
        self.disjoint = n
        self.parents = set(self.point)
        self.changed = True

    def find(self, i):
        if self.point[i] == i:
            return i

        r = self.find(self.point[i])
        self.point[i] = r
        return r

    def is_same(self, i, j):
        return self.find(i) == self.find(j)

    def union(self, i, j):
        if not self.is_same(i, j):
            self.changed = True

            x = self.find(i)
            y = self.find(j)

            if self.rank[x] > self.rank[y]:
                self.point[y] = x
                self.parents.discard(y)
            else:
                self.point[x] = y
                self.parents.discard(x)

                if self.rank[x] == self.rank[y]:
                    self.rank[y] = self.rank[y]+1

            self.disjoint -= 1

    def number(self):
        return self.disjoint

    def _gen_sizes(self):
        self.sizes = {}

        for i in range(0, len(self.point)):
            p = self.find(i)
            self.sizes[p] = self.sizes.get(p, 0) + 1

        assert(set(self.sizes) == self.parents)

    def size(self, i):
        if self.sizes == None or self.changed:
            self._gen_sizes()
            self.changed = False

        return self.sizes[self.find(i)]

def test_ufds():
    u = UFDS(6)
    u.union(1, 3)
    assert(u.number() == 5)
    assert(u.is_same(1, 3) == True)
    assert(u.is_same(1, 2) == False)
    assert(u.size(1) == 2)
    u.union(2, 4)
    assert(u.number() == 4)
    assert(u.is_same(1, 3) == True)
    assert(u.is_same(1, 2) == False)
    assert(u.is_same(2, 4) == True)
    assert(u.is_same(1, 4) == False)
    assert(u.size(2) == 2)
    u.union(2, 3)
    assert(u.number() == 3)
    assert(u.is_same(1, 3) == True)
    assert(u.is_same(1, 2) == True)
    assert(u.is_same(2, 4) == True)
    assert(u.is_same(1, 4) == True)
    assert(u.size(2) == 4)
    u.union(2, 1)
    assert(u.number() == 3)
    assert(u.is_same(1, 3) == True)
    assert(u.is_same(1, 2) == True)
    assert(u.is_same(2, 4) == True)
    assert(u.is_same(1, 4) == True)
    assert(u.size(2) == 4)
    print("DONE")


if __name__ == "__main__":
    test_ufds()
