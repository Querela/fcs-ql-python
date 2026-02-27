# Generated from FCSParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FCSParser import FCSParser
else:
    from FCSParser import FCSParser

# This class defines a complete generic visitor for a parse tree produced by FCSParser.

class FCSParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FCSParser#query.
    def visitQuery(self, ctx:FCSParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#main_query.
    def visitMain_query(self, ctx:FCSParser.Main_queryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_disjunction.
    def visitQuery_disjunction(self, ctx:FCSParser.Query_disjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_sequence.
    def visitQuery_sequence(self, ctx:FCSParser.Query_sequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_group.
    def visitQuery_group(self, ctx:FCSParser.Query_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_simple.
    def visitQuery_simple(self, ctx:FCSParser.Query_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#quantifier.
    def visitQuantifier(self, ctx:FCSParser.QuantifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_implicit.
    def visitQuery_implicit(self, ctx:FCSParser.Query_implicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#query_segment.
    def visitQuery_segment(self, ctx:FCSParser.Query_segmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#within_part.
    def visitWithin_part(self, ctx:FCSParser.Within_partContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#within_part_simple.
    def visitWithin_part_simple(self, ctx:FCSParser.Within_part_simpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression.
    def visitExpression(self, ctx:FCSParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression_or.
    def visitExpression_or(self, ctx:FCSParser.Expression_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression_and.
    def visitExpression_and(self, ctx:FCSParser.Expression_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression_group.
    def visitExpression_group(self, ctx:FCSParser.Expression_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression_not.
    def visitExpression_not(self, ctx:FCSParser.Expression_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#expression_basic.
    def visitExpression_basic(self, ctx:FCSParser.Expression_basicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#attribute.
    def visitAttribute(self, ctx:FCSParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#qualifier.
    def visitQualifier(self, ctx:FCSParser.QualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#identifier.
    def visitIdentifier(self, ctx:FCSParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#regexp.
    def visitRegexp(self, ctx:FCSParser.RegexpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#regexp_pattern.
    def visitRegexp_pattern(self, ctx:FCSParser.Regexp_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FCSParser#regexp_flag.
    def visitRegexp_flag(self, ctx:FCSParser.Regexp_flagContext):
        return self.visitChildren(ctx)



del FCSParser