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

    if os.system("g++ -o output.exe output.cpp"):
        exit(1)


if __name__ == "__main__":
    main()
