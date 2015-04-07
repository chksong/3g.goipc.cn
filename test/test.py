import functools

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