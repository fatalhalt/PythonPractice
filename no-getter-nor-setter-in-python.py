class Foo:
	def __init__(self, x):
		self.x = x

obj = Foo(42)
print(obj.x)
obj.x = 22
print(obj.x)
