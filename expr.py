from dataclasses import dataclass
from typing import Any, List

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
class LogicalExpr(Expr):
    left: Expr
    op: Token
    right: Expr

    def accept(self, acceptor):
        return acceptor.visit_logical(self)


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
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def accept(self, acceptor):
        return acceptor.visit_if_stmt(self)


@dataclass
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, acceptor):
        return acceptor.visit_while_stmt(self)


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
        return acceptor.visit_var_stmt(self)


@dataclass
class BlockStmt(Stmt):
    statements: List[Stmt]

    def accept(self, acceptor):
        return acceptor.visit_block_stmt(self)
