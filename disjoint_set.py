class DisjoinSet:
    def __init__(self):
        self.parents = {}
        self.ranks = {}

    def find(self, a):
        if a not in self.parents:
            self.parents[a] = a
            self.ranks[a] = 0
            return a

        while self.parents[a] != a:
            prev = a
            a = self.parents[a]
            self.parents[prev] = self.parents[a]

        return a

    def union(self, a, b):
        aroot = self.find(a)
        broot = self.find(b)

        if aroot == broot:
            return # already connected

        if self.ranks[aroot] < self.ranks[broot]:
            aroot, broot = broot, aroot

        self.parents[broot] = aroot
        if self.ranks[aroot] == self.ranks[broot]:
            self.ranks[aroot] += 1

    def are_connected(self, a, b):
        return self.find(a) == self.find(b)
