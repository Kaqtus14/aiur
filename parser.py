from expr import BinaryExpr, GroupingExpr, LiteralExpr, UnaryExpr
from lexer import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.NEQ, TokenType.EQ):
            op = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, op, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GT, TokenType.GE, TokenType.LT, TokenType.LE):
            op = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, op, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, op, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, op, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            expr = UnaryExpr(op, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        elif self.match(TokenType.FALSE):
            return LiteralExpr(False)
        elif self.match(TokenType.NIL):
            return LiteralExpr(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        elif self.match(TokenType.LPAREN):
            expr = self.expression()
            
            if self.consume().typ != TokenType.RPAREN:
                raise SyntaxError("expected ) after expression")

            return GroupingExpr(expr)
        else:
            assert False

        

    def match(self, *types):
        for typ in types:
            if self.check(typ):
                self.consume()
                return True

        return False

    def consume(self):
        if not self.eof():
            self.current += 1
        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def check(self, typ):
        if self.eof():
            return False
        return self.peek().typ == typ

    def eof(self):
        return self.peek().typ == TokenType.EOF