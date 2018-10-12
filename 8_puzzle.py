import copy
original = [[0, 2, 3], [1, 8, 4], [7, 6, 5]]
history={}
current = original
numbers=[1,2,3,4,5,6,7,8,9]
def print1(lst):
    if lst!=0:
        for i in range(3):
            print(lst[i])
    else:
        print(0)

def seeker(lst):  #get position of empty or '0'
    for i in range(3):
        try:
            x=(lst[i].index(0))
            return (i,x)
        except ValueError:
            x=0

def position_tester(lst,index):
    return 0
def right_to_left(lst,index): # try moving right to left /"left"
    try:
        i0=index[0]
        i1=index[1]
        if i1==2:      #prevent [1,1,0] to [0,1,1]
            return 0
        lst1=copy.deepcopy(lst)
        lst1[i0][i1+1],lst1[i0][i1]=lst1[i0][i1],lst1[i0][i1+1]
        return lst1
    except IndexError:
        return 0
def left_to_right(lst,index): # try moving left_to_right "right"
    try:
        i0=index[0]
        i1=index[1]
        if i1==0:      #prevent [0,1,1] to [1,1,0]
            return 0
        lst1=copy.deepcopy(lst)
        lst1[i0][i1-1],lst1[i0][i1]=lst1[i0][i1],lst1[i0][i1-1]
        return lst1
    except IndexError:
        return 0

def down_to_up(lst,index): # try moving down to up / "up"
    try:
        i0=index[0]
        i1=index[1]
        if i0==2:      #prevent flipping
            return 0
        lst1=copy.deepcopy(lst)
        lst1[i0+1][i1],lst1[i0][i1]=lst1[i0][i1],lst1[i0+1][i1]
        return lst1
    except IndexError:
        return 0
def up_to_down(lst,index): # try moving up to down/ "down"
    try:
        i0=index[0]
        i1=index[1]
        if i0==0:      #prevent flipping
            return 0
        lst1=copy.deepcopy(lst)
        lst1[i0+1][i1],lst1[i0][i1]=lst1[i0][i1],lst1[i0+1][i1]
        return lst1
    except IndexError:
        return 0

io=seeker(current)
print(io)
print1(current)
print()
kk=left_to_right(current,io)
print('right')
print1(kk)
print()
k1=right_to_left(current,io)
print('left')
print1(k1)
print()
k2=down_to_up(current,io)
print('up')
print1(k2)
print()
k3=up_to_down(current,io)
print('down')
print1(k3)