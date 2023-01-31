from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext
from antlr4 import ParseTreeWalker

from fcsql import antlr_parse
from fcsql import parse
from fcsql.FCSLexer import FCSLexer
from fcsql.FCSParser import FCSParser
from fcsql.FCSParserListener import FCSParserListener


def parse_raw(query):
    tree = antlr_parse(query)

    print(tree.toStringTree(FCSParser.ruleNames))

    class MyFCSParserListener(FCSParserListener):
        def enterQuery(self, ctx: FCSParser.QueryContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())

        def enterMain_query(self, ctx: FCSParser.Main_queryContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())

        def enterExpression(self, ctx: FCSParser.ExpressionContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())
            # print(ctx.getTokens(FCSLexer.OPERATOR_EQ))

        def enterExpression_basic(self, ctx: FCSParser.Expression_basicContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())
            print(
                ctx.getSourceInterval(),
                " " * (ctx.depth() + 1),
                ctx.children[0].getText(),
            )
            print(
                ctx.getSourceInterval(),
                " " * (ctx.depth() + 1),
                ctx.children[1].getText(),
            )
            print(
                ctx.getSourceInterval(),
                " " * (ctx.depth() + 1),
                ctx.children[2].getText(),
            )
            # print(ctx.getTokens(FCSLexer.OPERATOR_EQ))

        def enterAttribute(self, ctx: FCSParser.AttributeContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())

        def enterRegexp(self, ctx: FCSParser.RegexpContext):
            print(ctx.getSourceInterval(), " " * ctx.depth(), ctx.getText())

    listener = MyFCSParserListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


def parse_fcs(query):
    tree = parse(query)
    print(tree)


if __name__ == "__main__":
    query = '[ word = "a" ] [ lemma = "worlf"]'
    parse_raw(query)
    parse_fcs(query)
