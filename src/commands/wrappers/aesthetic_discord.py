

def box(fun, variant=""):

    def wrapper(*args, **fkwargs):
        retstr = fun(*args, **fkwargs)
        retstr = '```'+variant+retstr+'```'
        return retstr

    return wrapper
