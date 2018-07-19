class tag:
    def __init__(self, tagname):
        self.tagname=tagname
    def __enter__(self):
        print('<{}>'.format(self.tagname, end=''))
    def __exit__(self, etyp, einst, etb):
        print('</{}>'.format(self.tagname))

import contextlib

@contextlib.contextmanager
def xmltag(tagname):
    print('<{}>'.format(tagname), end='')
    try:
        yield
    finally:
        print('</{}>'.format(tagname))

def cross_product(seq1, seq2):
    if not seq1 or not seq2:
        raise ValueError("Sequence arguments must be non-empty!")
    return [(x1,x2) for x1 in seq1 for x2 in seq2]

#v2 v3 portable version:
import errno

def read_or_default(filepath, default):
    try:
        with open(filepath) as f:
            return f.read()
    except IOError as e:
        if e.errno== errno.ENOENT:
            return default
        else: raise

# in v3, using an OSError or subclass
def read_or_default_v3(filepath, default):
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError:
        return default

##


class InvalidAttribute(AttributeError):
    '''Used to indicate attributes that could never be valid'''


class SomeFunkyClass:
    '''much hypothetical functionality snipped'''

    def __getattr__(self, name):
        '''only clarifies the kind of attribute error'''
        if name.startswith('_'):
            raise InvalidAttribute('Unknown private attribute ' + name)
        else:
            raise AttributeError('Unknown attribute ' + name)
##

import sys
class CustomException(Exception):
    '''wrap arbitrary pending exception, if any,
    in addition to other info'''
    def __init__(self, *args):
        super().__init__(self,*args)
        self.wrapped_exc=sys.exc_info()

def call_wrapped(callable, *args, **kwds):
    try:
        return callable(*args, **kwds)
    except:
        raise CustomException('Wapped function', 'propagated exception')   

##
class CustomAttribute(CustomException, AttributeError):
    '''An attributeError which is also a CustomException'''

##
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html=urlopen(url)
    except HTTPError:
        return None
    try:
        bsobj=BeautifulSoup(html.read())
        title=bsobj.body.h1
    except AttributeError:
        return None
    return title

###aaaabbccdd6
html=urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsobj=BeautifulSoup(html)
namelist=bsobj.findAll("span", {"class":"green"})
for name in namelist:
    print(name.get_text())