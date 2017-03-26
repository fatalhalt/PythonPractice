#!/usr/bin/env python

# below snippet demonstrates list datatype in python (akin to arrays)
# lists are ordered, mutable, hold arbitrary objects, expand dynamically
l = [21, 'foo', 13, True, 21, [0, 1.0]]
l.append({'ipv4': '8.8.8.8'})
l.extend(['12', '33'])
l.insert(0, '1st')
# len is 10, the list or dict count as 1 element
print('len is: ' + str(len(l)) + ', ' + str(l))
bar = l.pop(2)  # bar = 'foo'
ip = l[-3]['ipv4']  # 3rd from last index
print('bar = ' + bar + ', ip: ' + ip)

# tuple, ordered, immutable, const-like object with no methods
t = ('foo', 'bar', 1, False, [1,2,3])
t[-1].extend([4,5])  # while tuples are constant and cannot be changed
print(t)             # the list at index -1 can still be mutated

# set, unordered
s = {1,2,3, 'string'}
ss = {1,2, "bar"}
sss = s.union(ss)  # values 1 and 2 won't show up as duplicates
print(sss)

# control flow
x = 1 if True else 2  # x = 1, this is example of ternary operator, akin to ? in C
print(x)

# List Comprehensions
mysum = sum([i for i in range(1, 10) if i%2==0])
squares = [x**2 for x in range(10)]
squares = list(map(lambda x: x**2, range(10)))
