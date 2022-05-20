#!/usr/bin/env python3
import os
import sys

from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator


def compile(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = CodeGenerator()
    return interpreter.compile(statements)


def main():
    with open(sys.argv[1]) as f:
        out = compile(f.read())

    print(out)
    with open("output.cpp", "w+") as f:
        f.write(out)

    include_path = os.path.join(os.path.dirname(__file__), "..")
    if os.system(f"g++ -I {include_path} -o output.exe output.cpp"):
        exit(1)


if __name__ == "__main__":
    main()
