from dataclasses import dataclass
from typing import List

from src.lexer import Token, TokenType
from src.parser import LangType
from src.parser import BinOpNode, BlockNode, FunctionDefNode, FunctionInvocNode, VarNode, LiteralNode

@dataclass
class LangExample:
    plaintext: str
    tokens: List[Token]
    syntax_tree: BlockNode = None
    ir_output: str = None


simple_assignment_example = LangExample(
    plaintext="x=5 \n x+1",
    tokens=[
        Token(TokenType.IDENTIFIER, "x"),
        Token(TokenType.OPERATOR,   "="),
        Token(TokenType.LITERAL_NUM, "5"),
        Token(TokenType.IDENTIFIER, "x"),
        Token(TokenType.OPERATOR,   "+"),
        Token(TokenType.LITERAL_NUM, "1"),
    ],
    syntax_tree=BlockNode([
        BinOpNode(Token(TokenType.OPERATOR, "="),
                  VarNode("x"),
                  LiteralNode("5", LangType.INT)),
        BinOpNode(Token(TokenType.OPERATOR, "+"),
                  VarNode("x"),
                  LiteralNode("1", LangType.INT)),
    ]),
)

simple_function_def_example = LangExample(
    plaintext="x = a -> { \n a+1 \n }",
    tokens = [
        Token(TokenType.IDENTIFIER,     "x"),
        Token(TokenType.OPERATOR,       "="),
        Token(TokenType.IDENTIFIER,     "a"),
        Token(TokenType.OPERATOR,       "->"),
        Token(TokenType.OPEN_SEPARATOR, "{"),
        Token(TokenType.IDENTIFIER,     "a"),
        Token(TokenType.OPERATOR,       "+"),
        Token(TokenType.LITERAL_NUM,    "1"),
        Token(TokenType.CLOSE_SEPARATOR, "}"),
    ],
    syntax_tree=BlockNode([
        BinOpNode(Token(TokenType.OPERATOR, "="),
            VarNode("x"),
            FunctionDefNode(
                args=[VarNode("a")],
                body=BlockNode([
                    BinOpNode(Token(TokenType.OPERATOR, "+"), VarNode("a"), LiteralNode("1", LangType.INT))
                ]),
                name="x"
            ))
    ])
)

singleline_comment_example = LangExample(
    plaintext="x # a singleline comment",
    tokens=[
        Token(TokenType.IDENTIFIER, "x"),
    ],
    syntax_tree=BlockNode([
        VarNode("x"),
    ])
)

simple_function_invoc_example = LangExample(
    plaintext="function(a,b)",
    tokens=[
        Token(TokenType.IDENTIFIER, "function"),
        Token(TokenType.OPEN_SEPARATOR, "("),
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.MID_SEPARATOR, ","),
        Token(TokenType.IDENTIFIER, "b"),
        Token(TokenType.CLOSE_SEPARATOR, ")"),
    ],
    syntax_tree=BlockNode([
        FunctionInvocNode(
            "function",
            [VarNode("a"), VarNode("b")])
    ])
)
