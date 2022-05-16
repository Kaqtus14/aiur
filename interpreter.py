import time
from typing import Callable

from lexer import TokenType


class Callable:
    def __init__(self, arity_fn, call_fn, tostring_fn):
        self.arity_fn, self.call_fn, self.tostring_fn = arity_fn, call_fn, tostring_fn


class Function(Callable):
    def __init__(self, declaration):
        self.declaration = declaration

    def call(self, interpreter, args):
        env = Env(interpreter.globals)
        for i, param in enumerate(self.declaration.params):
            env.define(param.lexeme, args[i])

        interpreter.execute_block(self.declaration.body.statements, env)

    def arity(self):
        return len(self.declaration.params)

    def tostring(self):
        return f"<function {self.declaration.name}>"


class Env:
    def __init__(self, enclosing=None):
        self.symbols = {}
        self.enclosing = enclosing

    def is_defined(self, key):
        return key in self.symbols or (self.enclosing is not None and self.enclosing.is_defined(key))

    def define(self, key, value, check=False):
        if not check or key in self.symbols:
            self.symbols[key] = value
        elif key in self.enclosing.symbols:
            self.enclosing.define(key, value, True)
        else:
            raise SyntaxError(f"Undefined variable: {key}")

    def get(self, key):
        if key in self.symbols:
            return self.symbols[key]
        elif self.enclosing is not None and self.enclosing.is_defined(key):
            return self.enclosing.get(key)
        else:
            raise SyntaxError(f"Undefined variable: {key}")


class Interpreter:
    def __init__(self):
        self.globals = Env()
        self.env = self.globals

        self.globals.define("clock", Callable(
            lambda: 0, lambda: time.time()/1000, lambda: "<native function>"))

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

    def visit_if_stmt(self, stmt):
        if self.evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt):
        while self.evaluate(stmt.condition):
            self.execute(stmt.body)

    def visit_function_stmt(self, stmt):
        function = Function(stmt)
        self.env.define(stmt.name.lexeme, function)

    def visit_var_stmt(self, stmt):
        value = self.evaluate(
            stmt.initializer) if stmt.initializer is not None else None
        self.env.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Env(self.env))

    def visit_literal(self, expr):
        return expr.value

    def visit_grouping(self, expr):
        return self.evaluate(expr.expr)

    def visit_variable(self, expr):
        return self.env.get(expr.name.lexeme)

    def visit_assign(self, expr):
        value = self.evaluate(expr.value)
        self.env.define(expr.name.lexeme, value, True)
        return value

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)

        if expr.op.typ == TokenType.MINUS:
            self.check_number(right)
            return -right
        elif expr.op.typ == TokenType.BANG:
            return not right
        else:
            assert False

    def visit_logical(self, expr):
        left = self.evaluate(expr.left)

        if expr.op.typ == TokenType.OR:
            if left:
                return bool(left)
        elif expr.op.typ == TokenType.AND:
            if not left:
                return bool(left)
        else:
            assert False

        return self.evaluate(expr.right)

    def visit_call(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = list(map(self.evaluate, expr.arguments))

        if len(arguments) != callee.arity():
            raise TypeError(
                f"Expected {callee.arity()} arguments, got {len(arguments)}")

        callee.call(self, arguments)

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

    def execute_block(self, statements, env):
        prev_env = self.env
        try:
            self.env = env

            for stmt in statements:
                self.execute(stmt)
        finally:
            self.env = prev_env

    @staticmethod
    def check_number(*vs):
        for v in vs:
            if type(v) != int and type(v) != float:
                raise RuntimeError(f"expected number, got {type(v)}")
