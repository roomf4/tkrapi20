"""
combo.py

This is a demo of iterating combinations of list members.

combo([]) s.b. None

combo([0]) s.b [0]

combo([0,1]) s.b.
  [0,1] + combo([0]) + combo([1])

combo([0,1]) s.b.
  [0,1], [0], [1]

combo([0,1,2]) s.b.
  [0,1,2],  [0,1], [0,2], [1,2], [0], [1], [2]

combo([0,1,2]) s.b.
  [0,1,2] + combo([0,1])  + combo([0,2])  + combo([1,2]) 

combo([0,1,2,3]) s.b.
 [0,1,2,3,]  [0,1,2], [0,2,3], [0,1,3], [1,2,3] 

combo([0,1,2,3]) s.b.
  [0,1,2,3,] + combo([0,1,2])  ...

In python how to remove one member of list by index?

lst = [4,3,2,1,0]
del(list[2])



lst1    = [0,1,2,3,4,5]
lenlst1 = len(lst1)

for mm in lst1:
    'print(mm)'

for idx1 in range(lenlst1):
    lst2    = lst1[:(idx1+1)]
    lenlst2 = len(lst2)
    for idx2 in range(lenlst2):
      lst3  = lst2[:(idx2+1)]
      print(idx1, idx2)
"""

def combo(lst):
    """This function should transform a lst into all combinations of sublists in a list."""
    subl_l = []
    if (len(lst) > 1):
        for idx in range(len(lst)):
            subl = list(lst)
            del(subl[idx]) # subl 1 shorter
            # subl_l.append(subl)
            subl_l.append(combo(subl))
    return [lst] + subl_l 

"""
print(combo([9]))
print(combo([1,9]))
print(combo([1,4,5]))
print(combo([1,4,5,9]))
"""
    
'bye'

import itertools

lst = [2,4,7,9,3]


combosn_l = []
for idx in range(len(lst)):
    combosn_l.append([mm for mm in itertools.combinations(lst,idx+1)])
#combos_l = [combo[0] for combo in combosn_l] # peel off a layer
#print(combosn_l)

combos_l = []
for mm_l in combosn_l:
    for mm in mm_l:
        combos_l.append(mm)
print(combos_l)
