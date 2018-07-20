class ListLike:
    def __init__(self):
        self._items=[]
    def __getattr__(self, name):
        return getattr(self._items, name)
    def __len__(self):
        return len(self._items)

##
import time
class Date:
    def __init__(self, *args):
        if len(args)==0:
            t=time.localtime()
            args=(t.tm_year, t.tm_mon, t.tm_day)
        self.year, self.month, self.day=args
    
    #alternate ctor
    @classmethod
    def today(cls):
        t=time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)

    def __str__(self):
        return '{x.month}/{x.day}/{x.year}'.format(x=self)

##
class LoggedMappingMixin:
    '''
    Add logging to get/set/delete operations for debugging
    '''
    __slots__=()

    def __getitem__(self, key):
        print('getting '+str(key))
        return super().__getitem__(key)

    def __delitem__(self, key):
        print('Deleting '+str(key))
        return super().__delitem__(key)

    def __setitem__(self, key, value):
        print('Setting {}={!r}'.format(key, value))  #use __repr__
        return super().__setitem__(key, value)

class SetOnceMappingMixin:
    '''
    Only allow a key to be set once
    '''
    __slots__=()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key)+ ' already set')
        return super().__setitem__(key, value)

class StringKeysMappingMixin:
    '''
    Restrict keys to strings only
    '''
    slots=()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('Key must be strings')
        return super().__setitem__(key, value)

class LoggedDict(LoggedMappingMixin, dict): pass

##
class Connection:
    def __init__(self):
        self.new_state(ClosedConnectionState)
    def new_state(self, newstate):
        self._state=newstate

    #delegate to the state class
    def read(self):
        return self._state.read(self)
    def write(self, data):
        return self._state.write(self,data)
    def open(self):
        return self._state.open(self)
    def close(self):
        return self._state.close(self)

class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()
    @staticmethod
    def write(conn, data):
        raise NotImplementedError()
    @staticmethod
    def open(conn):
        raise NotImplementedError()
    @staticmethod
    def close(conn):
        raise NotImplementedError()

#implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not Open')
    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not Open')
    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)
    @staticmethod
    def close(conn):
        raise RuntimeError('already closed!')

class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')
    @staticmethod
    def write(conn, data):
        print('writing')
    @staticmethod
    def open(conn):
        raise RuntimeError('already open')
    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

##
import math
class Point:
    def __init__(self, x, y):
        self.x=x; self.y=y
    def __repr__(self):
        return 'Point({!r:}, {!r:})'.format(self.x, self.y)
    def distance(self, x, y):
        return math.hypot(self.x-x, self.y-y)

##
'''
class MyMeta(type):
    def __str__(cls):
        return 'beautiful class {!r}'.format(cls.__name__)
class MyClass(metaclass=MyMeta): pass
x=MyClass()
print(type(x))
'''

import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time
    '''
    @wraps(func)  #for __name__.. yes, always need!
    def wrapper(*args, **kwargs):
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

##
@timethis
def countdown(n:int):
    'counts down'
    while n>0: n-=1

def somedecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
'''
@somedecorator
def add(x, y): return x+y


print(add(5,6))
orig_add=add.__wrapped__
print(orig_add(5,6))  #just type 11
'''

import logging
def logged(level, name=None, message=None):
    '''
    Add logging to a function, level is the logging level, anme is the logger name, 
    and messageis the log message -- if name and message aren't specified, default
    to the function's module and name
    '''
    def decorate(func):
        logname=name if name else func.__module__
        log=logging.getLogger(logname)
        logmsg=message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

'''
#example use:
@logged(logging.CRITICAL)
def add(x,y): return x+y

@logged(logging.CRITICAL, 'example')
def spam(): print('spam!')

print(add(5,6))
spam()
'''
from inspect import signature
def typeassert(*args, **kwargs):
    def decorate(func):
        #if in optimized mode, disable the type checking:
        if not __debug__:
            print('optional')
            return func
        #map the fucntion argument names to supplied types
        sig=signature(func)
        bound_types=sig.bind_partial(*args, *kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values=sig.bind(*args, **kwargs)

            #enforce type assertions across suplied arguments:
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError("wrong type!")
            return func(*args, **kwargs)
        return wrapper
    return decorate

@typeassert(int, int)
def add(x,y):
    return x+y

from functools import wraps
class A:
    #Decaorator as an instance method
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)
        return wrapper

    #decorator as a class method
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)
        return wrapper

##Here is an example how the two decaorator would be applied:
a=A()
@a.decorator1
def spam() : pass

#as a class method:
@A.decorator2
def gork(): pass

spam(); gork()