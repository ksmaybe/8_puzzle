import copy

class Puzzle:   #whole structure of the search
    def __init__(self,lst,goal):
        self.root=TreeNode(0,lst,None,None,None,None,None,None,None)
        self.goal=goal  #
        self.cost=1
        self.lowest=10^9
        self.found=False
        self.founded=True
        self.history=[]
        self.frontier=[]

class TreeNode:   #tree of the search
    def __init__(self,cost, val, left=None, right=None, up=None, down=None, parent=None,move=None,actual=None):
        self.cost= cost    #cost of moving to the node/ g(n)
        self.payload = val   #the state
        self.leftChild = left
        self.rightChild = right
        self.upChild = up
        self.downChild = down
        self.parent = parent
        self.heuristic=None   #f(n)
        self.move=move       #which direction this node is moving,L,R,U,D
        self.actual=actual
        self.explore=False    #has it been explored

    def __str__(self):
        string1=""
        string1+=str(self.payload[0])
        string1+='\n'
        string1+=str(self.payload[1])
        string1+='\n'
        string1+=str(self.payload[2])
        return string1

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

    def replaceNodeData(self, value, lc, rc, uc, dc):
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


def position_tester(puzzle,node, index):  #test left, right, up, down
    left=right_to_left(puzzle,node.payload,index)
    right=left_to_right(puzzle,node.payload,index)
    up=down_to_up(puzzle,node.payload,index)
    down=up_to_down(puzzle,node.payload,index)
    if left!=0:   #if it can move, it creates a child node
        puzzle.cost+=1
        z1=TreeNode(node.cost+1,left,None,None,None,None,node,'R',None)
        node.leftChild=z1
        node.leftChild.parent=node
    if right!=0:
        puzzle.cost+=1
        z2=TreeNode(node.cost+1,right,None,None,None,None,node,'L',None)
        node.rightChild=z2
        node.rightChild.parent=node
    if up!=0:
        puzzle.cost+=1
        z3=TreeNode(node.cost+1,up,None,None,None,None,node,'D',None)
        node.upChild=z3
        node.upChild.parent=node
    if down!=0:
        puzzle.cost+=1
        z4=TreeNode(node.cost+1,down,None,None,None,None,node,'U',None)
        node.downChild=z4
        node.downChild.parent=node

def right_to_left(puzzle,lst, index):  # try moving right to left /"left"
    try:
        i0 = index[0]
        i1 = index[1]
        if i1 == 2:  # prevent [1,1,0] to [0,1,1]
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0][i1 + 1], lst1[i0][i1] = lst1[i0][i1], lst1[i0][i1 + 1]  #try moving the tiles
        if lst1 in puzzle.history:        #graph search, ignore state previously explored
            return 0
        else:
            puzzle.history.append(lst1)  #add this state to memory
        return lst1
    except IndexError:
        return 0


def left_to_right(puzzle,lst, index):  # try moving left_to_right "right"
    try:
        i0 = index[0]
        i1 = index[1]
        if i1 == 0:  # prevent [0,1,1] to [1,1,0]
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0][i1 - 1], lst1[i0][i1] = lst1[i0][i1], lst1[i0][i1 - 1]
        if lst1 in puzzle.history:
            return 0
        else:
            puzzle.history.append(lst1)
        return lst1
    except IndexError:
        return 0


def down_to_up(puzzle,lst, index):  # try moving down to up / "up"
    try:
        i0 = index[0]
        i1 = index[1]
        if i0 == 2:  # prevent flipping
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0 + 1][i1], lst1[i0][i1] = lst1[i0][i1], lst1[i0 + 1][i1]
        if lst1 in puzzle.history:
            return 0
        else:
            puzzle.history.append(lst1)
        return lst1
    except IndexError:
        return 0


def up_to_down(puzzle,lst, index):  # try moving up to down/ "down"
    try:
        i0 = index[0]
        i1 = index[1]
        if i0 == 0 :  # prevent flipping
            return 0
        lst1 = copy.deepcopy(lst)
        lst1[i0 - 1][i1], lst1[i0][i1] = lst1[i0][i1], lst1[i0 - 1][i1]
        if lst1 in puzzle.history:
            return 0
        else:
            puzzle.history.append(lst1)
        return lst1
    except IndexError:
        return 0


def heuristic(puzzle,node):  #calculate f(n)
    g=node.cost            #g(n)
    h=0
    for i in range(3):
        for j in range(3):
            if node.payload[i][j]!=0 and node.payload[i][j]!=puzzle.goal[i][j]:
                index_current=seeker(node.payload,node.payload[i][j]) #position of elem
                index_goal=seeker(puzzle.goal,node.payload[i][j]) #position of elem in goal
                d1=abs(index_goal[0]-index_current[0])
                d2=abs(index_goal[1]-index_current[1])
                h+=d1+d2
    f=g+h   #f(n)=g(n)+h(n)
    return f

def a_search(puzzle):   #find the lowest frontier node to explore
    dude=puzzle.frontier[-1]
    for elem in puzzle.frontier:
        if elem[0].explore==False:
            if elem[1]<dude[1]:
                dude=elem
    return dude[0]

def solve(puzzle,node):
    zero=seeker(node.payload,0)  #find empty position
    position_tester(puzzle,node,zero)
    if node.leftChild!=None:
        nom=heuristic(puzzle,node.leftChild)
        node.leftChild.heuristic=nom
        puzzle.frontier.append((node.leftChild,nom)) #add state to frontier
        if node.leftChild.payload==goal:            #check if reached goal
            puzzle.found=True
            puzzle.founded=node.leftChild         #designate as goal node
    if node.rightChild!=None:
        nom=heuristic(puzzle,node.rightChild)
        node.rightChild.heuristic=nom
        puzzle.frontier.append((node.rightChild,nom))
        if node.rightChild.payload==goal:
            puzzle.found=True
            puzzle.founded=node.rightChild
    if node.upChild!=None:
        nom=heuristic(puzzle,node.upChild)
        node.upChild.heuristic=nom
        puzzle.frontier.append((node.upChild,nom))
        if node.upChild.payload==goal:
            puzzle.found=True
            puzzle.founded=node.upChild
    if node.downChild!=None:
        nom=heuristic(puzzle,node.downChild)
        node.downChild.heuristic=nom
        puzzle.frontier.append((node.downChild,nom))
        if node.downChild.payload==goal:
            puzzle.found=True
            puzzle.founded=node.downChild

    node.explore=True      #this node is explored, thus not a frontier node anymore
    k=a_search(puzzle) #find the frontier node with lowest f(n)
    if puzzle.found==True and puzzle.founded==k: #return if goal node found
        return puzzle.founded
    else:
        k=solve(puzzle,k)       #explore frontier node with lowest f(n)
        return k


original=[[],[],[]]
goal =[[],[],[]]
wow=[]
input="Input2.txt"              #type input file here
output="Output22.txt"           #type output file here
f=open(input,'r')
w=open(output,'w')
lines=f.read().strip().split('\n')
for i in range(len(lines)):     #read from input file and insert values to puzzle
    if i<4:
        wow.append(lines[i])
    elif i>3:
        wow.append(lines[i])
    w.write(lines[i]+'\n')

for i in range(len(wow)):
    if i<=2:
        x=wow[i]
        x1=x.split(' ')
        for elem in x1:
            if elem!='':
                original[i].append(int(elem))

    if i>=4:
        x=wow[i]
        x1=x.split(' ')
        for elem in x1:
            if elem!='':
                goal[i-4].append(int(elem))

current = original
print1(original)                #print original puzzle
print()
print1(goal)                    #print intended state

kzz=Puzzle(original,goal)       #create frame for search
kzz.history.append(original)    #original state added to memory
kpp=solve(kzz,kzz.root)
str2=""
node=kpp
while node!=kzz.root:           #go up from goal node to find all directions leading up to it
    str2+=node.move
    str2+=' '
    node=node.parent
str1=''
for i in range(len(str2)):      #reverse the directions to find beginning
    str1+=str2[-i-1]



print(kpp.cost)                 #print cost to get to goal
print(kzz.cost)                 #print nodes found
print(str1)                     #print directions to goal

w.write('\n')                   #write to output file
w.write(str(kpp.cost)+'\n')
w.write(str(kzz.cost)+'\n')
w.write(str1+'\n')