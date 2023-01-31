from dataclasses import dataclass
from typing import List

from src.lexer import Token, TokenType
from src.parser import BinOpNode, BlockNode, FunctionDefNode, FunctionInvocNode, ValueNode

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
        Token(TokenType.LITERAL,    "5"),
        Token(TokenType.IDENTIFIER, "x"),
        Token(TokenType.OPERATOR,   "+"),
        Token(TokenType.LITERAL,    "1"),
    ],
    syntax_tree=BlockNode([
        BinOpNode(Token(TokenType.OPERATOR, "="),
                  ValueNode(Token(TokenType.IDENTIFIER, "x")),
                  ValueNode(Token(TokenType.LITERAL, "5"))),
        BinOpNode(Token(TokenType.OPERATOR, "+"),
                  ValueNode(Token(TokenType.IDENTIFIER, "x")),
                  ValueNode(Token(TokenType.LITERAL, "1"))),
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
        Token(TokenType.LITERAL,        "1"),
        Token(TokenType.CLOSE_SEPARATOR, "}"),
    ],
    syntax_tree=BlockNode([
        BinOpNode(Token(TokenType.OPERATOR, "="),
            ValueNode(Token(TokenType.IDENTIFIER, "x")),
            FunctionDefNode([
                ValueNode(Token(TokenType.IDENTIFIER, "a"))],
                BlockNode([
                    BinOpNode(Token(TokenType.OPERATOR, "+"), ValueNode(Token(TokenType.IDENTIFIER, "a")), ValueNode(Token(TokenType.LITERAL, "1")))
                ])))
    ])
)

singleline_comment_example = LangExample(
    plaintext="x # a singleline comment",
    tokens=[
        Token(TokenType.IDENTIFIER, "x"),
    ],
    syntax_tree=BlockNode([
        ValueNode(Token(TokenType.IDENTIFIER, "x")),
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
            [ValueNode(Token(TokenType.IDENTIFIER, "a")), ValueNode(Token(TokenType.IDENTIFIER, "b"))])
    ])
)
