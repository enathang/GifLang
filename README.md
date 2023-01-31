# GifLang
GifLang is a small programming language written in Python. It compiles to LLVM.

## Features
GifLang supports the following features:
- Variable assignment
- Function definition/invocation
- Comments

Giflang does not support the following features:
- Importing/exporting symbols
- Control flow
- Types, classes

## Syntax
    x = 5 # No type declaration

    # Function definition
    incr = a -> {
      a = a+1
      return a
    }

    y = incr(x)

## Running
To use the language, download the project and run the compiler.py file. Note the src
will need to be added to the PYTHONPATH. This repo will probably eventually support Nix
or other tool to allow easy setup.
