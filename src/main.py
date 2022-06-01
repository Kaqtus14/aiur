#!/usr/bin/env python3
import os
import sys

from ctx import Context
from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator


def compile(ctx):
    lexer = Lexer(ctx)
    tokens = lexer.scan_tokens()

    parser = Parser(ctx, tokens)
    statements = parser.parse()

    interpreter = CodeGenerator(ctx)
    return interpreter.compile(statements)


def main():
    with open(sys.argv[1]) as f:
        ctx = Context(sys.argv[1],f.read())
    out = compile(ctx)

    print(out)
    with open("output.cpp", "w+") as f:
        f.write(out)

    include_path = os.path.join(os.path.dirname(__file__), "..", "stdlib")
    if os.system(f"g++ -I {include_path} -o output.exe output.cpp"):
        exit(1)


if __name__ == "__main__":
    main()
