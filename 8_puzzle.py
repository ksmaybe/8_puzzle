import copy

class Puzzle:
    def __init__(self,lst,goal):
        self.root=TreeNode(0,0,lst,None,None,None,None,None)
        self.goal=goal
        self.cost=None

class TreeNode:
    def __init__(self, key=0,cost=0, val=None, left=None, right=None, up=None, down=None, parent=None):
        self.key = key
        self.cost= cost
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.upChild = up
        self.downChild = down
        self.parent = parent

    def __iter__(self):
        if self.payload != 0:
            for i in range(3):
                print(self.payload[i])
        else:
            print(0)

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def hasUpChild(self):
        return self.upChild

    def hasDownChild(self):
        return self.downChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isUpChild(self):
        return self.parent and self.parent.upChild == self

    def isDownChild(self):
        return self.parent and self.parent.downChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild or self.upChild or self.downChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild or self.upChild or self.downChild

    def hasAllChildren(self):
        return self.rightChild and self.leftChild and self.upChild and self.downChild

    def replaceNodeData(self, key, value, lc, rc, uc, dc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        self.upChild=uc
        self.downChild=dc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
        if self.hasUpChild():
            self.upChild.parent = self
        if self.hasDownChild():
            self.downChild.parent = self


original = [[0, 2, 3], [1, 8, 4], [7, 6, 5]]
goal=[[2,8,3],[1,0,4],[7,6,5]]
history = {}
current = original
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def print1(lst):
    if lst != 0:
        for i in range(3):
            print(lst[i])
    else:
        print(0)


def seeker(lst,target):  # get position of empty or '0' (row,index)
    for i in range(3):
        try:
            x = (lst[i].index(target))
            return (i, x)
        except ValueError:
            x = 0


def position_tester(puzzle,node, index):
    left=right_to_left(node.payload,index)
    right=left_to_right(node.payload,index)
    up=down_to_up(node.payload,index)
    down=up_to_down(node.payload,index)
    if left!=0:
        puzzle.cost+=1
        z1=TreeNode(node.key+1,node.cost+1,left,None,None,None,None,node)
        node.leftChild=z1
    if right!=0:
        puzzle.cost+=1
        z2=TreeNode(node.key+1,node.cost+1,right,None,None,None,None,node)
        node.rightChild=z2
    if up!=0:
        puzzle.cost+=1
        z3=TreeNode(node.key+1,node.cost+1,up,None,None,None,None,node)
        node.upChild=z3
    if up!=0:
        puzzle.cost+=1
        z4=TreeNode(node.key+1,node.cost+1,down,None,None,None,None,node)
        node.downChild=z4

def right_to_left(lst, index):  # try moving right to left /"left"
    try:
        i0 = index[0]
        i1 = index[1]
        if i1 == 2:  # prevent [1,1,0] to [0,1,1]
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0][i1 + 1], lst1[i0][i1] = lst1[i0][i1], lst1[i0][i1 + 1]
        return lst1
    except IndexError:
        return 0


def left_to_right(lst, index):  # try moving left_to_right "right"
    try:
        i0 = index[0]
        i1 = index[1]
        if i1 == 0:  # prevent [0,1,1] to [1,1,0]
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0][i1 - 1], lst1[i0][i1] = lst1[i0][i1], lst1[i0][i1 - 1]
        return lst1
    except IndexError:
        return 0


def down_to_up(lst, index):  # try moving down to up / "up"
    try:
        i0 = index[0]
        i1 = index[1]
        if i0 == 2:  # prevent flipping
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0 + 1][i1], lst1[i0][i1] = lst1[i0][i1], lst1[i0 + 1][i1]
        return lst1
    except IndexError:
        return 0


def up_to_down(lst, index):  # try moving up to down/ "down"
    try:
        i0 = index[0]
        i1 = index[1]
        if i0 == 0:  # prevent flipping
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0 + 1][i1], lst1[i0][i1] = lst1[i0][i1], lst1[i0 + 1][i1]
        return lst1
    except IndexError:
        return 0

def solve(node):
    return 0

def heuristic(puzzle,node):  #calculate f(n)
    g=node.cost
    h=0
    for i in range(3):
        for j in range(3):
            if node.payload[i][j]!=0 and node.payload[i][j]!=puzzle.goal[i][j]:
                index_current=seeker(node.payload,node.payload[i][j]) #position of elem
                index_goal=seeker(puzzle.goal,node.payload[i][j]) #position of elem in goal
                d1=abs(index_goal[0]-index_current[0])
                d2=abs(index_goal[1]-index_current[1])
                h+=d1+d2
    f=g+h
    return f


kzz=Puzzle(original,goal)

