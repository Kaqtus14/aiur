import sys

from lexer import Lexer


def run(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()

    for token in tokens:
        print(token)


def main():
    if len(sys.argv) == 1:
        while True:
            run(input("lox> "))
    else:
        with open(sys.argv[1]) as f:
            run(f.read())


if __name__ == "__main__":
    main()