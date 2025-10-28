#!/usr/bin/env python3

from sys import argv as arguments
from dataclasses import dataclass as data
from copy import deepcopy

@data
class success ():
    result: object

@data
class failure ():
    reason: str

def read(program):
    return program.split()

context = list()
lexicon = dict()

isfailure   = lambda value: isinstance (value, failure)
iscomposite = lambda value: isinstance (value, list)
isnumeric   = lambda value: value[0].isdigit()
issymbolic  = lambda value: value[0] == "'"

Opener, Closer = "(", ")"
def follow (program):
    if not program:
        return

    term, *rest = program

    if term == "(":
        result = learn (rest)

        if isfailure (result):
            return result
        else:
            definition, rest = result

        context.append (definition)

    elif term in lexicon:
        definition = lexicon [term]

        if iscomposite (definition):
            follow (definition)
        else:
            definition()

    elif isnumeric (term):
        context.append (float (term))

    elif issymbolic (term):
        context.append (term [1:])

    else:
        return failure(f"{term}?")

    follow (rest)


immediates = list()

def learn (program, definition = None):
    definition = definition or list()

    if not program:
        return failure("Definition was never finished.")

    term, *rest = program

    if term == ")":
        return definition, rest

    if term in immediates:
        follow ([term])
    else:
        definition.append (term)

    return learn (rest, definition)


def Term(name):
    def index (term):
        lexicon [name] = term
        return term
    return index

def binary(term):
    def inner():
        b, a = context.pop(), context.pop()
        context.append(term(a, b))
    return inner

@Term("+")
@binary
def _ (a, b):
    """a + b (primitive)"""
    return a + b

@Term("-")
@binary
def _ (a, b):
    """a - b (primitive)"""
    return a - b

@Term("=")
@binary
def _ (a, b):
    """a = b (primitive)"""
    return a == b

@Term("~")
@binary
def _ (a, b):
    """a != b (primitive)"""
    return a != b

@Term(">")
@binary
def _ (a, b):
    """a > b (primitive)"""
    return a > b

@Term("<")
@binary
def _ (a, b):
    """a > b (primitive)"""
    return a > b

@Term(".")
def _ ():
    """let a -> b (primitive)"""
    value, name = context.pop(), context.pop()
    lexicon [name] = value

@Term("swap")
def _ ():
    """a, b -> b, a (primitive)"""
    a, b = context.pop(), context.pop()
    context.append(a)
    context.append(b)

@Term("copy")
def _ ():
    """a -> a a (primitive)"""
    a = context.pop()
    context.append(deepcopy(a))
    context.append(deepcopy(a))

@Term("!")
def _ ():
    """a() (primitive)"""
    follow (context.pop())

@Term("?")
def _ ():
    """print a (primitive)"""
    definition = lexicon[context.pop()]
    print(definition)
    print(f"({' '.join (definition)})" if iscomposite (definition) else definition.__doc__)

@Term("immediate")
def _ ():
    immediates.append(context.pop())

@Term("lexicon")
def _ ():
    """print lexicon (primitive)"""
    print (" ".join (map (str, lexicon)))

@Term("context")
def _ ():
    """print lexicon (primitive)"""
    items = list()
    for item in context:
        if iscomposite (item):
            items.append (f"composite({len (item)})")
        else:
            items.append (str (item))
    print(" ".join (map (str, items)))


def reference (book):
    with open (book) as program:
        follow (program)


def say(text, *styles):
    print (f"\x1b[{';'.join (map (str, styles))}m{text}\x1b[0m", end = "")

def dialog():
    say (f"\t({len (context)}) : ", 33)
    request = input()

    if request == "bye":
        say ("Bye!\n", 32)
        return
    if not request:
        return dialog()

    program = read (request)
    result = follow (program)

    if isfailure (result):
        say (f"{result.reason}\n", 31)
    else:
        say ("Ok.\n", 32)

    dialog()


def main():
    match arguments:
        case [_, location]:
            reference(location)
        case [_]:
            dialog()


if __name__ == "__main__":
    main()

