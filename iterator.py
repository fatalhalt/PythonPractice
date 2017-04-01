# this class implements an iterator
# python needs to be told when to stop iterating, this is done by raising StopIteration exception

class ReverseString():
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]


def main():
    foo = ReverseString('foobar')
    for c in foo:
        print(c)


if __name__ == "__main__":
    main()
