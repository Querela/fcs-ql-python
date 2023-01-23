# Generated from FCSParser.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FCSParser import FCSParser
else:
    from FCSParser import FCSParser

# This class defines a complete listener for a parse tree produced by FCSParser.
class FCSParserListener(ParseTreeListener):

    # Enter a parse tree produced by FCSParser#query.
    def enterQuery(self, ctx:FCSParser.QueryContext):
        pass

    # Exit a parse tree produced by FCSParser#query.
    def exitQuery(self, ctx:FCSParser.QueryContext):
        pass


    # Enter a parse tree produced by FCSParser#main_query.
    def enterMain_query(self, ctx:FCSParser.Main_queryContext):
        pass

    # Exit a parse tree produced by FCSParser#main_query.
    def exitMain_query(self, ctx:FCSParser.Main_queryContext):
        pass


    # Enter a parse tree produced by FCSParser#query_disjunction.
    def enterQuery_disjunction(self, ctx:FCSParser.Query_disjunctionContext):
        pass

    # Exit a parse tree produced by FCSParser#query_disjunction.
    def exitQuery_disjunction(self, ctx:FCSParser.Query_disjunctionContext):
        pass


    # Enter a parse tree produced by FCSParser#query_sequence.
    def enterQuery_sequence(self, ctx:FCSParser.Query_sequenceContext):
        pass

    # Exit a parse tree produced by FCSParser#query_sequence.
    def exitQuery_sequence(self, ctx:FCSParser.Query_sequenceContext):
        pass


    # Enter a parse tree produced by FCSParser#query_group.
    def enterQuery_group(self, ctx:FCSParser.Query_groupContext):
        pass

    # Exit a parse tree produced by FCSParser#query_group.
    def exitQuery_group(self, ctx:FCSParser.Query_groupContext):
        pass


    # Enter a parse tree produced by FCSParser#query_simple.
    def enterQuery_simple(self, ctx:FCSParser.Query_simpleContext):
        pass

    # Exit a parse tree produced by FCSParser#query_simple.
    def exitQuery_simple(self, ctx:FCSParser.Query_simpleContext):
        pass


    # Enter a parse tree produced by FCSParser#quantifier.
    def enterQuantifier(self, ctx:FCSParser.QuantifierContext):
        pass

    # Exit a parse tree produced by FCSParser#quantifier.
    def exitQuantifier(self, ctx:FCSParser.QuantifierContext):
        pass


    # Enter a parse tree produced by FCSParser#query_implicit.
    def enterQuery_implicit(self, ctx:FCSParser.Query_implicitContext):
        pass

    # Exit a parse tree produced by FCSParser#query_implicit.
    def exitQuery_implicit(self, ctx:FCSParser.Query_implicitContext):
        pass


    # Enter a parse tree produced by FCSParser#query_segment.
    def enterQuery_segment(self, ctx:FCSParser.Query_segmentContext):
        pass

    # Exit a parse tree produced by FCSParser#query_segment.
    def exitQuery_segment(self, ctx:FCSParser.Query_segmentContext):
        pass


    # Enter a parse tree produced by FCSParser#within_part.
    def enterWithin_part(self, ctx:FCSParser.Within_partContext):
        pass

    # Exit a parse tree produced by FCSParser#within_part.
    def exitWithin_part(self, ctx:FCSParser.Within_partContext):
        pass


    # Enter a parse tree produced by FCSParser#within_part_simple.
    def enterWithin_part_simple(self, ctx:FCSParser.Within_part_simpleContext):
        pass

    # Exit a parse tree produced by FCSParser#within_part_simple.
    def exitWithin_part_simple(self, ctx:FCSParser.Within_part_simpleContext):
        pass


    # Enter a parse tree produced by FCSParser#expression.
    def enterExpression(self, ctx:FCSParser.ExpressionContext):
        pass

    # Exit a parse tree produced by FCSParser#expression.
    def exitExpression(self, ctx:FCSParser.ExpressionContext):
        pass


    # Enter a parse tree produced by FCSParser#expression_or.
    def enterExpression_or(self, ctx:FCSParser.Expression_orContext):
        pass

    # Exit a parse tree produced by FCSParser#expression_or.
    def exitExpression_or(self, ctx:FCSParser.Expression_orContext):
        pass


    # Enter a parse tree produced by FCSParser#expression_and.
    def enterExpression_and(self, ctx:FCSParser.Expression_andContext):
        pass

    # Exit a parse tree produced by FCSParser#expression_and.
    def exitExpression_and(self, ctx:FCSParser.Expression_andContext):
        pass


    # Enter a parse tree produced by FCSParser#expression_group.
    def enterExpression_group(self, ctx:FCSParser.Expression_groupContext):
        pass

    # Exit a parse tree produced by FCSParser#expression_group.
    def exitExpression_group(self, ctx:FCSParser.Expression_groupContext):
        pass


    # Enter a parse tree produced by FCSParser#expression_not.
    def enterExpression_not(self, ctx:FCSParser.Expression_notContext):
        pass

    # Exit a parse tree produced by FCSParser#expression_not.
    def exitExpression_not(self, ctx:FCSParser.Expression_notContext):
        pass


    # Enter a parse tree produced by FCSParser#expression_basic.
    def enterExpression_basic(self, ctx:FCSParser.Expression_basicContext):
        pass

    # Exit a parse tree produced by FCSParser#expression_basic.
    def exitExpression_basic(self, ctx:FCSParser.Expression_basicContext):
        pass


    # Enter a parse tree produced by FCSParser#attribute.
    def enterAttribute(self, ctx:FCSParser.AttributeContext):
        pass

    # Exit a parse tree produced by FCSParser#attribute.
    def exitAttribute(self, ctx:FCSParser.AttributeContext):
        pass


    # Enter a parse tree produced by FCSParser#qualifier.
    def enterQualifier(self, ctx:FCSParser.QualifierContext):
        pass

    # Exit a parse tree produced by FCSParser#qualifier.
    def exitQualifier(self, ctx:FCSParser.QualifierContext):
        pass


    # Enter a parse tree produced by FCSParser#identifier.
    def enterIdentifier(self, ctx:FCSParser.IdentifierContext):
        pass

    # Exit a parse tree produced by FCSParser#identifier.
    def exitIdentifier(self, ctx:FCSParser.IdentifierContext):
        pass


    # Enter a parse tree produced by FCSParser#regexp.
    def enterRegexp(self, ctx:FCSParser.RegexpContext):
        pass

    # Exit a parse tree produced by FCSParser#regexp.
    def exitRegexp(self, ctx:FCSParser.RegexpContext):
        pass


    # Enter a parse tree produced by FCSParser#regexp_pattern.
    def enterRegexp_pattern(self, ctx:FCSParser.Regexp_patternContext):
        pass

    # Exit a parse tree produced by FCSParser#regexp_pattern.
    def exitRegexp_pattern(self, ctx:FCSParser.Regexp_patternContext):
        pass


    # Enter a parse tree produced by FCSParser#regexp_flag.
    def enterRegexp_flag(self, ctx:FCSParser.Regexp_flagContext):
        pass

    # Exit a parse tree produced by FCSParser#regexp_flag.
    def exitRegexp_flag(self, ctx:FCSParser.Regexp_flagContext):
        pass



del FCSParser