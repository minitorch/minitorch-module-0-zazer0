"""
Collection of the core mathematical operators used throughout the code base.
"""

import math
from typing import Callable, Iterable

# ## Task 0.1
#
# Implementation of a prelude of elementary functions.

def mul(x: float, y: float) -> float:
    "$f(x, y) = x * y$"
    return x * y

def id(x: float) -> float:
    "$f(x) = x$"
    return x

def add(x: float, y: float) -> float:
    "$f(x, y) = x + y$"
    return x + y


def neg(x: float) -> float:
    "$f(x) = -x$"
    return (-1 * x)


def lt(x: float, y: float) -> float:
    "$f(x) =$ 1.0 if x is less than y else 0.0"
    return 1.0 if x < y else 0.0


def eq(x: float, y: float) -> float:
    "$f(x) =$ 1.0 if x is equal to y else 0.0"
    return 1.0 if x == y else 0.0


def max(x: float, y: float) -> float:
    "$f(x) =$ x if x is greater than y else y"
    return x if x > y else y


def is_close(x: float, y: float) -> float:
    "$f(x) = |x - y| < 1e-2$"

    return abs(x - y) < 1e-2

def sigmoid(x: float) -> float:
    r"""
    $f(x) =  \frac{1.0}{(1.0 + e^{-x})}$

    (See https://en.wikipedia.org/wiki/Sigmoid_function )

    Calculate as

    $f(x) =  \frac{1.0}{(1.0 + e^{-x})}$ if x >=0 else $\frac{e^x}{(1.0 + e^{x})}$

    for stability.
    """
    if x >= 0:
        return (1.0)/(1.0+exp(-x))
    else:
        return (exp(x))/(1.0+exp(x))


def relu(x: float) -> float:
    """
    $f(x) =$ x if x is greater than 0, else 0

    (See https://en.wikipedia.org/wiki/Rectifier_(neural_networks) .)
    """
    return x if x > 0 else 0.0


EPS = 1e-6

def log(x: float) -> float:
    "$f(x) = log(x)$"
    return math.log(x + EPS)

def exp(x: float) -> float:
    "$f(x) = e^{x}$"
    return math.exp(x)

def log_back(x: float, d: float) -> float:
    r"If $f = log$ as above, compute $d \times f'(x)$"
    print("TODO: wtf")
    # this is saying take f(x) = log
        # based off this value, return `d` *  d/dx(f) # i.e, d/dx(log)
        # so: d/dx  log
        # so: 1/x
        # = 1/x # rmbr to mult by d
        # = d/x
    return d/x


def inv(x: float) -> float:
    "$f(x) = 1/x$"
    return 1/x


def inv_back(x: float, d: float) -> float:
    r"If $f(x) = 1/x$ compute $d \times f'(x)$"
    # this is saying take f(x) = 1/x
        # based off this value, return `d` *  d/dx(f) # i.e, d/dx(1/x)
        # so: d/dx  x^(-1)
        # so: - x^(-2)
        # = - 1/x**2 # rmbr to mult by d
    return d * -(1/x**2)


def relu_back(x: float, d: float) -> float:
    r"If $f = relu$ compute $d \times f'(x)$"
    if (x < 0): return 0.0
    elif (x > 0): return d * 1; # f'(x) = 1
    else: return None


# ## Task 0.3

# Small practice library of elementary higher-order functions.


def map(fn: Callable[[float], float]) -> Callable[[Iterable[float]], Iterable[float]]:
    """
    Higher-order map.

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: Function from one value to one value.

    Returns:
        A function that takes a list, applies `fn` to each element, and returns a
         new list
    """
    # need to setup an abstracted function, `f(list)
    # -> it should apply the passed `fn` on each elem of the passed list; returns a new one
    def list_mapper(runtimeList):
        return [ fn(x) for x in runtimeList ]

    return list_mapper


def negList(ls: Iterable[float]) -> Iterable[float]:
    "Use `map` and `neg` to negate each element in `ls`"
    neg_mapfn = map(lambda x : -x)
    return neg_mapfn(ls)
    # def neglist_mapper(runtimeList):
    #     return [ neg_mapfn(x) for x in runtimeList ]


def zipWith(
    fn: Callable[[float, float], float]
) -> Callable[[Iterable[float], Iterable[float]], Iterable[float]]:
    """
    Higher-order zipwith (or map2).

    See https://en.wikipedia.org/wiki/Map_(higher-order_function)

    Args:
        fn: combine two values

    Returns:
        Function that takes two equally sized lists `ls1` and `ls2`, produce a new list by
         applying fn(x, y) on each pair of elements.

    """
    # need to call `fn(a,b) for pairs of l_x, l_y`

    def zip_map(l1, l2):
        newList = []
        for x,y in zip(l1,l2):
            newList.append(fn(x,y))
        return newList

    return zip_map


def addLists(ls1: Iterable[float], ls2: Iterable[float]) -> Iterable[float]:
    "Add the elements of `ls1` and `ls2` using `zipWith` and `add`"
    addWith = zipWith(add)
    addedList = addWith(ls1, ls2)
    return addedList


def reduce(
    fn: Callable[[float, float], float], start: float
) -> Callable[[Iterable[float]], float]:
    r"""
    Higher-order reduce.

    Args:
        fn: combine two values
        start: start value $x_0$

    Returns:
        Function that takes a list `ls` of elements
         $x_1 \ldots x_n$ and computes the reduction :math:`fn(x_3, fn(x_2,
         fn(x_1, x_0)))`
    """
    # (origFn(), start)

    # make reduceFn: takes (lsToReduce)
        # should call origFn on each pair of elems;
        # starting with the passed `start var and ls[0]`!

    def reduceFn(lsToReduce):
        if len(lsToReduce) == 0: # passed `start` was first original elem
            return start

        acc = start
        for elem in lsToReduce:
            acc = fn(acc,elem)
        return acc

    return reduceFn


def sum(ls: Iterable[float]) -> float:
    "Sum up a list using `reduce` and `add`."
    if (len(ls)) == 0:
        return 0
    start = ls[0]
    reducer = reduce(add,start)
    return reducer(ls[1:])


def prod(ls: Iterable[float]) -> float:
    "Product of a list using `reduce` and `mul`."
    if (len(ls)) == 0:
        return 0
    start = 1
    reducer = reduce(mul,start)
    return reducer(ls)
