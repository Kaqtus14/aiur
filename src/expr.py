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


@dataclass
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: List[Expr]

    def accept(self, acceptor):
        return acceptor.visit_call(self)


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
class ForStmt(Stmt):
    variable: Token
    iterator: Expr
    body: Stmt

    def accept(self, acceptor):
        return acceptor.visit_for_stmt(self)


@dataclass
class FunctionStmt(Stmt):
    name: Token
    params: List[Token]
    body: List[Stmt]

    def accept(self, acceptor):
        return acceptor.visit_function_stmt(self)


@dataclass
class VarStmt(Stmt):
    name: Token
    initializer: Expr

    def accept(self, acceptor):
        return acceptor.visit_var_stmt(self)


@dataclass
class ReturnStmt(Stmt):
    keyword: Token
    value: Expr

    def accept(self, acceptor):
        return acceptor.visit_return_stmt(self)


@dataclass
class BlockStmt(Stmt):
    statements: List[Stmt]

    def accept(self, acceptor):
        return acceptor.visit_block_stmt(self)


@dataclass
class DeferStmt(Stmt):
    block: Stmt

    def accept(self, acceptor):
        return acceptor.visit_defer_stmt(self)
