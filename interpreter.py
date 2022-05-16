from lexer import TokenType


class Interpreter:
    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, stmt):
        return stmt.accept(self)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)

    def visit_print_stmt(self, stmt):
        print(self.evaluate(stmt.expr))

    def visit_literal(self, expr):
        return expr.value

    def visit_grouping(self, expr):
        return self.evaluate(expr.expr)

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)

        if expr.op.typ == TokenType.MINUS:
            self.check_number(right)
            return -right
        elif expr.op.typ == TokenType.BANG:
            return not right
        else:
            assert False

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.op.typ == TokenType.PLUS:
            return left + right
        elif expr.op.typ == TokenType.MINUS:
            self.check_number(left, right)
            return left - right
        elif expr.op.typ == TokenType.STAR:
            self.check_number(left, right)
            return left * right
        elif expr.op.typ == TokenType.SLASH:
            self.check_number(left, right)
            return left / right
        elif expr.op.typ == TokenType.EQ:
            return left == right
        elif expr.op.typ == TokenType.NEQ:
            return left != right
        elif expr.op.typ == TokenType.GT:
            self.check_number(left, right)
            return left > right
        elif expr.op.typ == TokenType.GE:
            self.check_number(left, right)
            return left >= right
        elif expr.op.typ == TokenType.LT:
            self.check_number(left, right)
            return left < right
        elif expr.op.typ == TokenType.LE:
            self.check_number(left, right)
            return left <= right
        else:
            assert False

    @staticmethod
    def check_number(*vs):
        for v in vs:
            if type(v) != int and type(v) != float:
                raise RuntimeError(f"expected number, got {type(v)}")
