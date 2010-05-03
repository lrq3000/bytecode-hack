import dis
import inspect
import sys

from bytecode_tracer import BytecodeTracer
from bytecode_tracer import rewrite_function


btracer = BytecodeTracer()
def trace(frame, event, arg):
    try:
        for ev, rest in btracer.trace(frame, event):
            if ev == 'c_call':
                func, pargs, kargs = rest
                print "C_CALL", func.__name__, repr(pargs), repr(kargs)
            elif ev == 'c_return':
                print "C_RETURN", repr(rest)
            elif ev == 'print':
                print "PRINT"
    except TypeError:
        if event == 'call':
            print "CALL", frame.f_code.co_name, inspect.getargvalues(frame)
        elif event == 'return':
            print "RETURN", frame.f_code.co_name, repr(arg)
        elif event == 'exception':
            print "EXCEPTION", arg
    return trace

def fun(x):
    return x+1

def doit():
    x = [1, 10]
    fun(1) # Python function
    pow(2, 3) # C function
    y = repr(4)
    range(*x)
    try:
        chr(256)
    except ValueError:
        pass
    property(doc="asdf")
    z = {'real': 1, 'imag': 2}
    complex(**z)
    print 5, 6
    print

def dothat():
    try:
        try:
            x = 4
            y = 5
            chr(256)
        except ValueError:
            complex(3, 10)
    finally:
        chr(128)

def doloop():
    chr(90)
    for x in xrange(10):
        if x < 3:
            continue
        if x > 8:
            break
        chr(97+x)
    else:
        complex(2, 3)
    complex(1, 2)

def dochain():
    xrange(sum([1,2,3,5]) + 0)

def doimport():
    import foo
    foo.bleh()

######################################################################

if __name__ == '__main__':
    btracer.setup()

    dis.dis(doimport)
    rewrite_function(doimport)

    sys.settrace(trace)
    try:
        doimport()
    finally:
        sys.settrace(None)
