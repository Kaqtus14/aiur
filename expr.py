from dataclasses import dataclass
from typing import Any

from lexer import Token


class Expr:
    pass


@dataclass
class BinaryExpr(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, acceptor):
        return acceptor.visit_binary(self)


@dataclass
class GroupingExpr(Expr):
    expr: Expr

    def accept(self, acceptor):
        return acceptor.visit_grouping(self)


@dataclass
class LiteralExpr(Expr):
    value: Any

    def accept(self, acceptor):
        return acceptor.visit_literal(self)


@dataclass
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def accept(self, acceptor):
        return acceptor.visit_unary(self)


@dataclass
class UnaryExpr(Expr):
    op: Token
    right: Expr

    def accept(self, acceptor):
        return acceptor.visit_unary(self)


@dataclass
class VariableExpr(Expr):
    name: Token

    def accept(self, acceptor):
        return acceptor.visit_variable(self)


@dataclass
class AssignExpr(Expr):
    name: Token
    value: Expr

    def accept(self, acceptor):
        return acceptor.visit_assign(self)


class Stmt:
    pass


@dataclass
class ExpressionStmt(Stmt):
    expr: Expr

    def accept(self, acceptor):
        return acceptor.visit_expression_stmt(self)


@dataclass
class PrintStmt(Stmt):
    expr: Token

    def accept(self, acceptor):
        return acceptor.visit_print_stmt(self)


@dataclass
class VarStmt(Stmt):
    name: Token
    initializer: Expr

    def accept(self, acceptor):
        return acceptor.visit_variable_stmt(self)
