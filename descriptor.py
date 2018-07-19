#base class, uses a descriptor to set a value
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name=name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name]=value

#Descriptor for enforcing types
class Typed(Descriptor):
    expected_type=type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected '+str(self.expected_type))
        super().__set__(instance, value)

#descriptor for enforctin values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value<0:
            raise ValueError('expected >=0')
        super().__set__(instance, value)

class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value)>=self.size:
            raise ValueError('size must be < '+str(self.size))
        super().__set__(instance, value)

class Integer(Typed):
    expected_type=int

class UnsignedInteger(Integer, Unsigned):
    pass

class Float(Typed):
    expected_type=float

class UnsignedFloat(Float, Unsigned):
    pass

class String(Typed):
    expected_type=str

class SizedString(String, MaxSized):
    pass

#using these objects, is now possible to define a class such as:
class Stock:
    #specify constraints
    name=SizedString('name', size=8)
    shares=UnsignedInteger('shares')
    price=UnsignedFloat('price')
    def __init__(self, name, shares, price):
        self.name=name
        self.shares=shares
        self.price=price

'''
s=Stock('acem', 50, 80.8)
print(s.name)
s.price='alot'
'''
#class decorator to apply constraints:
def check_attributes(**kwargs):
    def decorator(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name=key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorator

#Example:
@check_attributes(name=SizedString(size=8),
    shares=UnsignedInteger, price=UnsignedFloat)
class Stock2:
    def __init__(self, name, shares, price):
        self.name=name; self.shares=shares; self.price=price
'''
s=Stock2('acc',111,111.1)
print(s.name)
s.price=30.0
'''

#construct a metaclass that applies checking
class checkmeta(type):
    def __new__(cls, clsname, bases, methods):
        #attach attribute names to the descriptors
        for key, value in methods.items():
            if isinstance(value, Descriptor):
                value.name=key
        return type.__new__(cls, clsname, bases, methods)

class Stock3(metaclass=checkmeta):
    name=SizedString(size=8)
    shares=UnsignedInteger()
    price=UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name=name; self.shares=shares; self.price=price

'''
s=Stock3('wu', 11, 11.1)
print(s.name)
print(s.price)
s.price=1
'''