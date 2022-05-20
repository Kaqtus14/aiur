import os
import sys

from lexer import Lexer
from parser import Parser
from codegen import CodeGenerator


def run(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = CodeGenerator()
    out = interpreter.compile(statements)

    print(out)
    with open("output.cpp", "w+") as f:
        f.write(out)
    os.system("g++ -o output.exe output.cpp")


def main():
    with open(sys.argv[1]) as f:
        run(f.read())


if __name__ == "__main__":
    main()
