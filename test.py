def spamrun(fn):
    def sayspam(*args):
        print "ch--1"
        return fn(*args)
    return sayspam


@spamrun
def useful(a,b):
    print a+b

useful(3,4)