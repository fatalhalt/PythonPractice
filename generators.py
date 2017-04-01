
# here is a simple generator
# a 'yield' returns an expression which then gets invoked in for loop, a num by itself is an expression
def gen1():
    yield 1
    yield 2
    yield 3  # at this point python's list implemention will raise StopIteration since were at last yield

a = [i for i in gen1()]
print(a)


# following example depicts how Comprehensions are syntactically almost the same except the use of () instead of []

gen2 = ("{0} is even".format(i) for i in range(0, 10) if i % 2 == 0)
print(gen2.__next__())  # get a value
print(list(gen2))  # loop till the end
#print(gen2.__next__())  # this would error, generator can only be looped once

# output
#
# 0 is even
# ['2 is even', '4 is even', '6 is even', '8 is even']



# here is a Generator version of string reversal from interator.py

def reverseString2(data):
    for index in range(len(data) - 1, -1, -1):
        yield data[index]

for c in reverseString2('barfoo'):
    print(c)
