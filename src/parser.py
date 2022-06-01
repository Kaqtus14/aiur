import ctx
from expr import AssignExpr, BinaryExpr, BlockStmt, CallExpr, DeferStmt, ExpressionStmt, ForStmt, FunctionStmt, GroupingExpr, IfStmt, LiteralExpr, ReturnStmt, UnaryExpr, VarStmt, VariableExpr, WhileStmt
from lexer import TokenType


class Parser:
    def __init__(self, ctx, tokens):
        self.ctx = ctx
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.eof():
            statements.append(self.declaration())

        return statements

    def declaration(self):
        if self.match(TokenType.VAR):
            return self.var_declaration()
        else:
            return self.statement()

    def statement(self):
        if self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.FOR):
            return self.for_statement()
        elif self.match(TokenType.LBRACE):
            return self.block_statement()
        elif self.match(TokenType.FUN):
            return self.function_statement()
        elif self.match(TokenType.RETURN):
            return self.return_statement()
        elif self.match(TokenType.DEFER):
            return self.defer_statement()
        else:
            return self.expression_statement()

    def if_statement(self):
        condition = self.expression()

        then_branch = self.statement()
        else_branch = self.statement() if self.match(TokenType.ELSE) else None

        return IfStmt(condition, then_branch, else_branch)

    def while_statement(self):
        condition = self.expression()
        body = self.statement()
        return WhileStmt(condition, body)

    def for_statement(self):
        variable = self.consume()
        if not self.match(TokenType.IN):
            ctx.error(
                f"expected IN, got {self.peek().typ}", self.ctx, self.peek().pos)
        iterator = self.expression()
        body = self.statement()
        return ForStmt(variable, iterator, body)

    def function_statement(self):
        if not self.match(TokenType.IDENTIFIER):
            ctx.error(
                f"expected function name, got {self.peek().typ}", self.ctx, self.peek().pos)
        name = self.previous()

        if not self.match(TokenType.LPAREN):
            ctx.error(
                f"expected (, got {self.peek().typ}", self.ctx, self.peek().pos)

        parameters = []

        if not self.check(TokenType.RPAREN):
            parameters.append(self.consume())
            while self.match(TokenType.COMMA):
                parameters.append(self.consume())

        if not self.match(TokenType.RPAREN):
            ctx.error(f"expected ), got {self.peek().typ}",
                      self.ctx, self.peek().pos)
        if not self.match(TokenType.LBRACE):
            ctx.error(f"expected {{, got {self.peek().typ}",
                      self.ctx, self.peek().pos)

        body = self.block_statement()
        return FunctionStmt(name, parameters, body)

    def block_statement(self):
        statements = []

        while not self.check(TokenType.RBRACE) and not self.eof():
            statements.append(self.declaration())

        if not self.match(TokenType.RBRACE):
            ctx.error(
                f"expected }}, got {self.peek().typ}", self.ctx, self.peek().pos)

        return BlockStmt(statements)

    def return_statement(self):
        keyword = self.previous()
        value = self.expression()

        return ReturnStmt(keyword, value)

    def defer_statement(self):
        if not self.match(TokenType.LBRACE):
            ctx.error(f"expected {{, got {self.peek().typ}",
                      self.ctx, self.peek().pos)

        return DeferStmt(self.block_statement())

    def expression_statement(self):
        expr = self.expression()
        return ExpressionStmt(expr)

    def var_declaration(self):
        if not self.match(TokenType.IDENTIFIER):
            ctx.error(
                f"expected variable name, got {self.peek().typ}", self.ctx, self.peek().pos)
        name = self.previous()

        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()

        return VarStmt(name, initializer)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.ASSIGN):
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)
            else:
                ctx.error("invalid assignment target",
                          self.ctx, self.peek().pos)

        return expr

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

        while self.match(TokenType.MOD, TokenType.STAR, TokenType.SLASH):
            op = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, op, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.previous()
            right = self.unary()
            return UnaryExpr(op, right)

        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                arguments.append(self.expression())

        if not self.match(TokenType.RPAREN):
            ctx.error(f"expected ), got {self.peek().typ}",
                      self.ctx, self.peek().pos)
        paren = self.previous()

        return CallExpr(callee, paren, arguments)

    def primary(self):
        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        elif self.match(TokenType.FALSE):
            return LiteralExpr(False)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.previous().literal)
        elif self.match(TokenType.LPAREN):
            expr = self.expression()

            if self.consume().typ != TokenType.RPAREN:
                ctx.error(
                    f"expected ), got {self.peek().typ}", self.ctx, self.peek().pos)

            return GroupingExpr(expr)
        elif self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous())
        else:
            ctx.error(f"unexpected {self.peek().typ}",
                      self.ctx, self.peek().pos)

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
