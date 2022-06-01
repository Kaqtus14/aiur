from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Tuple
import ctx


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    DOT = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MOD = auto()
    SEMICOLON = auto()
    BANG = auto()
    ASSIGN = auto()

    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GE = auto()
    LE = auto()

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    IF = auto()
    RETURN = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    DEFER = auto()

    EOF = auto()


KEYWORDS = {
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "func": TokenType.FUN,
    "if": TokenType.IF,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "let": TokenType.VAR,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "in": TokenType.IN,
    "defer": TokenType.DEFER,
}


@dataclass
class Token:
    typ: TokenType
    lexeme: str
    literal: Any
    pos: Tuple[int, int]


class Lexer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.start = 0
        self.current = 0

    def scan_tokens(self):
        while not self.eof():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(TokenType.EOF, "", None, (self.line, self.pos)))
        return self.tokens

    def scan_token(self):
        c = self.consume()

        if c == "(":
            self.add_token(TokenType.LPAREN)
        elif c == ")":
            self.add_token(TokenType.RPAREN)
        elif c == "{":
            self.add_token(TokenType.LBRACE)
        elif c == "}":
            self.add_token(TokenType.RBRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.eof():
                    self.consume()
            else:
                self.add_token(TokenType.SLASH)
        elif c == "%":
            self.add_token(TokenType.MOD)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "!":
            self.add_token(TokenType.NEQ if self.match("=")
                           else TokenType.BANG)
        elif c == "=":
            self.add_token(TokenType.EQ if self.match("=")
                           else TokenType.ASSIGN)
        elif c == "<":
            self.add_token(TokenType.LE if self.match("=") else TokenType.LT)
        elif c == ">":
            self.add_token(TokenType.GE if self.match("=") else TokenType.GT)
        elif c == "\"":
            self.parse_string()
        elif c.isdigit():
            self.parse_number()
        elif c.isalpha():
            self.parse_identifier()
        elif c == "\n":
            self.line += 1
            self.pos = 0
        elif c.isspace():
            pass
        else:
            ctx.error(
                f"unexpected character: {c}", self.ctx, (self.line, self.pos))

    def parse_number(self):
        value = self.ctx.src[self.current-1]
        while not self.eof() and (self.peek().isdigit() or self.peek() == "."):
            value += self.consume()

        self.add_token(TokenType.NUMBER, int(value))

    def parse_identifier(self):
        value = self.ctx.src[self.current-1]
        while not self.eof() and (self.peek().isalnum() or self.peek() in "_:"):
            value += self.consume()

        self.add_token(KEYWORDS.get(value, TokenType.IDENTIFIER))

    def parse_string(self):
        value = ""
        while not self.eof() and self.peek() != "\"":
            value += self.consume()

        if self.consume() != "\"":
            ctx.error("unterminated string literal",
                        self.file, (self.line, self.pos))

        self.add_token(TokenType.STRING, value)

    def add_token(self, typ, literal=None):
        self.tokens.append(
            Token(typ, self.ctx.src[self.start:self.current], literal, (self.line, self.pos)))

    def match(self, expected):
        if self.eof():
            return False
        if self.peek() != expected:
            return False

        self.current += 1
        self.pos += 1
        return True

    def consume(self):
        c = self.peek()
        self.current += 1
        self.pos += 1
        return c

    def peek(self):
        if self.eof():
            return "\0"
        return self.ctx.src[self.current]

    def eof(self):
        return self.current >= len(self.ctx.src)
