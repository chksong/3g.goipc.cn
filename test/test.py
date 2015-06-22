import functools

import datetime


print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def spamrun(fn):
    @functools.wraps(fn)
    def sayspam(*args):
        print "ch--1"
        return fn(*args)
    return sayspam


@spamrun
def useful(a,b):
    print a+b

useful(3,4)
print "usefulname ===", useful.__name__

def amazing():
    '''This is the amazing function.
     Want to see it again?'''
    print('This function is named:', amazing.__name__)
    print('And its docstring is:', amazing.__doc__)

amazing()