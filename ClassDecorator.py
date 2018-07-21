import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls=0

    def __call__(self, *args, **kwargs):
        self.ncalls+=1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

@Profiled
def add(x,y):return x+y

'''
print(add.ncalls)   #0
add(2,3)
print(add.ncalls)   #1
'''

class Spam1:
    def bar(self, x):
        print(self, x)
    bar=Profiled(bar)

def pro(func):
    ncalls=0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls+=1
        return func(*args,**kwargs)
    wrapper.ncalls=lambda: ncalls
    return wrapper

#example:

@pro
def sub(x,y): return x-y

'''
sub(1,2)
print(sub.ncalls())
'''
import time
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start=time.time()
        r=func(*args, **kwargs)
        end=time.time()
        print(end-start)
        return r
    return wrapper

class Spam:
    @timethis
    def instance_method(self, n):
        print(self,n)
        while n>0: n-=1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n>0: n-=1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n>0: n-=1

'''
s=Spam()
s.instance_method(10000)
Spam.class_method(10000)
Spam.static_method(10000)
'''

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

@optional_debug
def sp(a, b, c):
    print(a, b, c)

'''
sp(1,2,3)
print(end='\n\n')
sp(1,2,3, debug=True)
'''
'''
with open(r'D:\Python\textwriter.txt',encoding='utf-16') as f:
    while True:
        line=next(f, None)
        if line is None:
             break
        print(line, end='')
'''
class Node1:
    def __init__(self, value):
        self._value=value
        self._children=[]

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

'''
root, child1, child2=Node(0), Node(1), Node(2)
root.add_child(child1); root.add_child(child2)
for ch in root: print(ch)     
'''
def frange(start, stop, increment):
    x=start
    while x<stop:
        yield x
        x+=increment
'''
for n in frange(0,4,0.5): print(n)
print(list(frange(0,1,0.125)))
'''

class Node:
    def __init__(self, value):
        self._value=value
        self._children=[]

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)
    
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

'''
root, child1, child2=Node(0), Node(1), Node(2)
root.add_child(child1); root.add_child(child2)
child1.add_child(Node(3))
child1.add_child(Node(4))
for ch in root.depth_first(): print(ch)
'''

class CountDown:
    def __init__(self, start):
        self.start=start
    #forward iterator
    def __iter__(self):
        n=self.start
        while n>0: yield n; n-=1

    #reverse iterator
    def __reversed__(self):
        n=1
        while n<=self.start:
            yield n; n+=1

'''
for i in CountDown(5): print(i,end='')
print()
for i in reversed(CountDown(5)): print(i,end='')
'''

from collections import deque
class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines=lines
        self.history=deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()
'''
with open (r'd:\python\textwriter.txt', encoding='utf-16') as f:
    lines=linehistory(f)
    for line in lines:
        if 'bool' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
'''

class HelloWorld:
    def __init__(self, chars):
        self.chars=chars
        self.deque=deque(maxlen=len(chars))

    def __iter__(self):
        for charno, ch in enumerate(self.chars, 1):
            self.deque.append((charno, ch))
            yield charno, ch

    def clear(self):
        self.deque.clear()
'''
s='Hello world'
h1=HelloWorld(s)
for charno, ch in h1:
    print(charno, ch)

def count(n):
    while True:
        yield n; n+=1
c=count(0)
#c[10:20]  #error, generator is not subscriptable
import itertools
for x in itertools.islice(c,10,20):
    print(x)'''

from itertools import dropwhile
with open (r'd:\python\textwriter.txt', encoding='utf-16') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print(line, end='')