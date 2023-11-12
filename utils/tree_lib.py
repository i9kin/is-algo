# https://en.wikipedia.org/wiki/Tree_traversal#Pre-order_implementation
# build tree PreOrder copy pasted from sort-me solution=99303
from typing import List
from itertools import permutations
from collections import defaultdict


def nextUpper(a: List[int]) -> List[int]:
    stack = []
    res = [len(a) for _ in range(len(a))]
    for i in range(len(a)):
        while len(stack) and a[stack[-1]] < a[i]:
            res[stack[-1]] = i
            stack.pop()
        stack.append(i)
    return res


class Node:
    def __init__(self, x):
        self.x = x
        self.l = None
        self.r = None


class Tree:
    def __init__(self, root: Node):
        self.root = root

    def __dfs(self, root, p=None):
        res = f"{root.x}"
        if p is None or root.x < p.x:
            res += " [first] "
        else:
            res += " [second] "
        childs = []
        if root.l is not None:
            childs.append(self.__dfs(root.l, root))
        if root.r is not None:
            childs.append(self.__dfs(root.r, root))
        res += f"-> {{{','.join(childs)}}}"
        return res

    def __str__(self):
        return self.__dfs(self.root)

    def insert(self, x):
        if self.root == None:
            self.root = x
        else:
            self.__insert(self.root, x)

    def __insert(self, x, z):
        while x != None:
            if z.x > x.x:
                if x.r != None:
                    x = x.r
                else:
                    x.r = z
                    break
            elif z.x < x.x:
                if x.l != None:
                    x = x.l
                else:
                    x.l = z
                    break

    def PreOrder(self):
        return self.__PreOrder(self.root)

    def __PreOrder(self, root):
        res = str(root.x) + " "
        if root.l != None:
            res += self.__PreOrder(root.l)
        if root.r != None:
            res += self.__PreOrder(root.r)
        return res


class PreOrder(Tree):
    def __init__(self, a: List[int]):
        nxt = nextUpper(a)
        super().__init__(self.build(0, len(a) - 1, a, nxt))

    def build(self, l: int, r: int, a, nxt) -> Node:
        if l > r:
            return None
        p = nxt[l]
        res = Node(a[l])
        res.l = self.build(l + 1, p - 1, a, nxt)
        res.r = self.build(p, r, a, nxt)
        return res


if __name__ == "__main__":
    # t = PreOrder([8, 3, 1, 6, 4, 7, 10, 14, 13])
    a = [1, 3, 5, 8]
    m = defaultdict(list)
    for perm in permutations([i for i in range(len(a))]):
        t = Tree(None)
        for i in perm:
            t.insert(Node(a[i]))
        m[t.PreOrder()].append(perm)

    for i, k in enumerate(m):
        text = ",".join(f"[{','.join(map(str, a))}]" for a in m[k])
        # print(f'<div id="item-{i}">```tree\n{k}\n{text}\n```</div>')

    keys = list(m.keys())
    for i, pos in enumerate([1, 2, 4, 5, 10, 14]):
        k = keys[pos - 1]
        text = ",".join(f"[{','.join(map(str, a))}]" for a in m[k])
        print(f'<div id="item32-{i}">```tree\n{k}\n{text}\n```</div>')
