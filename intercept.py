import dis
import inspect
import sys

from hack import bytecode_trace
from hackpyc import hack_line_numbers


def trace(frame, event, arg):
    try:
        ev, rest = bytecode_trace(frame, event)
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
    z = {'source': '1', 'filename': '', 'mode': 'eval'}
    compile(**z)
    print 5, 6
    print

######################################################################

print dis.dis(doit)

fun.func_code = hack_line_numbers(fun.func_code)
doit.func_code = hack_line_numbers(doit.func_code)

sys.settrace(trace)
try:
    doit()
finally:
    sys.settrace(None)
