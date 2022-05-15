import sys

from lexer import Lexer
from parser import Parser


def run(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()

    parser = Parser(tokens)
    expr = parser.expression()


def main():
    if len(sys.argv) == 1:
        while True:
            run(input("lox> "))
    else:
        with open(sys.argv[1]) as f:
            run(f.read())


if __name__ == "__main__":
    main()