# %% [markdown]
# Source: paustin library

# %%
from collections import namedtuple
import numpy as np
from scipy import optimize
# %%
def make_tuple(in_dict,tupname='values'):
    """
    make a named tuple from a dictionary

    Parameters
    ==========

    in_dict: dictionary
         Any python object with key/value pairs

    tupname: string
         optional name for the new namedtuple type

    Returns
    =======

    the_tup: namedtuple
          named tuple with keys as attributes
    """
    the_tup = namedtuple(tupname, in_dict.keys())
    the_tup = the_tup(**in_dict)
    return the_tup

# %%
def find_interval(the_func, x, *args):
    """
    starting from a 2% difference, move out from a 
    point until the_func changes sign

    Parameters
    ----------

    the_func : function
               function that returns zero when on root
    
    x : float
        argument to the_func

    *args : tuple
            additional arguments for the_func

    Returns
    -------

    brackets : [left,right]
               left,right  brackets for root 
    """
    if x == 0.:
        dx = 1. / 50.
    else:
        dx = x / 50.

    maxiter = 40
    twosqrt = np.sqrt(2)

    failed = True
    for i in range(maxiter):
        dx = dx * twosqrt
        a = x - dx
        fa = the_func(a, *args)
        b = x + dx
        fb = the_func(b, *args)
        if (fa * fb < 0.):
            failed = False
            break
    if failed:
        #
        # load the debugging information into the BracketError exception as a
        # namedtuple
        #
        extra_info = make_tuple(dict(a=a,b=b,fa=fa,fb=fb,x=x,dx=dx,args=args))
        raise BracketError("Couldn't find a suitable range. Providing extra_info",extra_info=extra_info)
    return (a, b)

# %%
def fzero(the_func, root_bracket, *args, **parms):
    """
    simple wrapper for optimize.zeros.brenth

    Parameters
    ----------

    the_func : function
               function that returns zero when on root

    root_bracket : [left, right]
               left and right x values that bracket a sign change

    *args : tuple
            additional arguments for the_func

    **params: dict
              additional parameters for optimize.zeros.brenth

    Returns
    -------

    x value that produces the_func=0
    """
    answer = optimize.zeros.brenth(the_func,
                                   root_bracket[0],
                                   root_bracket[1],
                                   args=args,
                                   **parms)
    return answer
