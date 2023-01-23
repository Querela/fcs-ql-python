# Generated from FCSParser.g4 by ANTLR 4.11.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,25,208,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,1,0,1,0,3,0,50,8,0,1,0,1,0,1,1,1,1,
        1,1,1,1,3,1,58,8,1,1,2,1,2,1,2,3,2,63,8,2,1,2,1,2,1,2,1,2,3,2,69,
        8,2,4,2,71,8,2,11,2,12,2,72,1,3,1,3,4,3,77,8,3,11,3,12,3,78,1,4,
        1,4,1,4,3,4,84,8,4,1,4,1,4,3,4,88,8,4,1,5,1,5,3,5,92,8,5,1,5,3,5,
        95,8,5,1,6,1,6,1,6,1,6,1,6,1,6,3,6,103,8,6,1,6,1,6,1,6,1,6,1,6,3,
        6,110,8,6,3,6,112,8,6,1,6,3,6,115,8,6,1,7,1,7,1,8,1,8,3,8,121,8,
        8,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,11,1,11,1,11,3,11,134,8,
        11,1,12,1,12,1,12,1,12,3,12,140,8,12,1,12,1,12,1,12,1,12,1,12,3,
        12,147,8,12,4,12,149,8,12,11,12,12,12,150,1,13,1,13,1,13,3,13,156,
        8,13,1,13,1,13,1,13,1,13,3,13,162,8,13,4,13,164,8,13,11,13,12,13,
        165,1,14,1,14,1,14,1,14,1,14,3,14,173,8,14,1,14,1,14,1,15,1,15,1,
        15,1,15,1,15,3,15,182,8,15,1,16,1,16,1,16,1,16,1,17,1,17,1,17,3,
        17,191,8,17,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,1,20,3,20,202,
        8,20,1,21,1,21,1,22,1,22,1,22,0,0,23,0,2,4,6,8,10,12,14,16,18,20,
        22,24,26,28,30,32,34,36,38,40,42,44,0,2,1,0,15,16,1,0,18,21,231,
        0,46,1,0,0,0,2,57,1,0,0,0,4,62,1,0,0,0,6,76,1,0,0,0,8,80,1,0,0,0,
        10,91,1,0,0,0,12,114,1,0,0,0,14,116,1,0,0,0,16,118,1,0,0,0,18,124,
        1,0,0,0,20,126,1,0,0,0,22,133,1,0,0,0,24,139,1,0,0,0,26,155,1,0,
        0,0,28,167,1,0,0,0,30,176,1,0,0,0,32,183,1,0,0,0,34,190,1,0,0,0,
        36,194,1,0,0,0,38,196,1,0,0,0,40,198,1,0,0,0,42,203,1,0,0,0,44,205,
        1,0,0,0,46,49,3,2,1,0,47,48,5,18,0,0,48,50,3,18,9,0,49,47,1,0,0,
        0,49,50,1,0,0,0,50,51,1,0,0,0,51,52,5,0,0,1,52,1,1,0,0,0,53,58,3,
        10,5,0,54,58,3,8,4,0,55,58,3,6,3,0,56,58,3,4,2,0,57,53,1,0,0,0,57,
        54,1,0,0,0,57,55,1,0,0,0,57,56,1,0,0,0,58,3,1,0,0,0,59,63,3,10,5,
        0,60,63,3,6,3,0,61,63,3,8,4,0,62,59,1,0,0,0,62,60,1,0,0,0,62,61,
        1,0,0,0,63,70,1,0,0,0,64,68,5,5,0,0,65,69,3,10,5,0,66,69,3,6,3,0,
        67,69,3,8,4,0,68,65,1,0,0,0,68,66,1,0,0,0,68,67,1,0,0,0,69,71,1,
        0,0,0,70,64,1,0,0,0,71,72,1,0,0,0,72,70,1,0,0,0,72,73,1,0,0,0,73,
        5,1,0,0,0,74,77,3,10,5,0,75,77,3,8,4,0,76,74,1,0,0,0,76,75,1,0,0,
        0,77,78,1,0,0,0,78,76,1,0,0,0,78,79,1,0,0,0,79,7,1,0,0,0,80,83,5,
        1,0,0,81,84,3,4,2,0,82,84,3,6,3,0,83,81,1,0,0,0,83,82,1,0,0,0,84,
        85,1,0,0,0,85,87,5,2,0,0,86,88,3,12,6,0,87,86,1,0,0,0,87,88,1,0,
        0,0,88,9,1,0,0,0,89,92,3,14,7,0,90,92,3,16,8,0,91,89,1,0,0,0,91,
        90,1,0,0,0,92,94,1,0,0,0,93,95,3,12,6,0,94,93,1,0,0,0,94,95,1,0,
        0,0,95,11,1,0,0,0,96,115,5,11,0,0,97,115,5,12,0,0,98,115,5,13,0,
        0,99,111,5,9,0,0,100,112,5,22,0,0,101,103,5,22,0,0,102,101,1,0,0,
        0,102,103,1,0,0,0,103,104,1,0,0,0,104,105,5,14,0,0,105,112,5,22,
        0,0,106,107,5,22,0,0,107,109,5,14,0,0,108,110,5,22,0,0,109,108,1,
        0,0,0,109,110,1,0,0,0,110,112,1,0,0,0,111,100,1,0,0,0,111,102,1,
        0,0,0,111,106,1,0,0,0,112,113,1,0,0,0,113,115,5,10,0,0,114,96,1,
        0,0,0,114,97,1,0,0,0,114,98,1,0,0,0,114,99,1,0,0,0,115,13,1,0,0,
        0,116,117,3,40,20,0,117,15,1,0,0,0,118,120,5,3,0,0,119,121,3,22,
        11,0,120,119,1,0,0,0,120,121,1,0,0,0,121,122,1,0,0,0,122,123,5,4,
        0,0,123,17,1,0,0,0,124,125,3,20,10,0,125,19,1,0,0,0,126,127,5,19,
        0,0,127,21,1,0,0,0,128,134,3,32,16,0,129,134,3,30,15,0,130,134,3,
        28,14,0,131,134,3,24,12,0,132,134,3,26,13,0,133,128,1,0,0,0,133,
        129,1,0,0,0,133,130,1,0,0,0,133,131,1,0,0,0,133,132,1,0,0,0,134,
        23,1,0,0,0,135,140,3,32,16,0,136,140,3,28,14,0,137,140,3,30,15,0,
        138,140,3,26,13,0,139,135,1,0,0,0,139,136,1,0,0,0,139,137,1,0,0,
        0,139,138,1,0,0,0,140,148,1,0,0,0,141,146,5,5,0,0,142,147,3,32,16,
        0,143,147,3,28,14,0,144,147,3,30,15,0,145,147,3,26,13,0,146,142,
        1,0,0,0,146,143,1,0,0,0,146,144,1,0,0,0,146,145,1,0,0,0,147,149,
        1,0,0,0,148,141,1,0,0,0,149,150,1,0,0,0,150,148,1,0,0,0,150,151,
        1,0,0,0,151,25,1,0,0,0,152,156,3,32,16,0,153,156,3,28,14,0,154,156,
        3,30,15,0,155,152,1,0,0,0,155,153,1,0,0,0,155,154,1,0,0,0,156,163,
        1,0,0,0,157,161,5,6,0,0,158,162,3,32,16,0,159,162,3,28,14,0,160,
        162,3,30,15,0,161,158,1,0,0,0,161,159,1,0,0,0,161,160,1,0,0,0,162,
        164,1,0,0,0,163,157,1,0,0,0,164,165,1,0,0,0,165,163,1,0,0,0,165,
        166,1,0,0,0,166,27,1,0,0,0,167,172,5,1,0,0,168,173,3,32,16,0,169,
        173,3,30,15,0,170,173,3,24,12,0,171,173,3,26,13,0,172,168,1,0,0,
        0,172,169,1,0,0,0,172,170,1,0,0,0,172,171,1,0,0,0,173,174,1,0,0,
        0,174,175,5,2,0,0,175,29,1,0,0,0,176,181,5,7,0,0,177,182,3,32,16,
        0,178,182,3,30,15,0,179,182,3,24,12,0,180,182,3,26,13,0,181,177,
        1,0,0,0,181,178,1,0,0,0,181,179,1,0,0,0,181,180,1,0,0,0,182,31,1,
        0,0,0,183,184,3,34,17,0,184,185,7,0,0,0,185,186,3,40,20,0,186,33,
        1,0,0,0,187,188,3,36,18,0,188,189,5,17,0,0,189,191,1,0,0,0,190,187,
        1,0,0,0,190,191,1,0,0,0,191,192,1,0,0,0,192,193,3,38,19,0,193,35,
        1,0,0,0,194,195,7,1,0,0,195,37,1,0,0,0,196,197,7,1,0,0,197,39,1,
        0,0,0,198,201,3,42,21,0,199,200,5,8,0,0,200,202,3,44,22,0,201,199,
        1,0,0,0,201,202,1,0,0,0,202,41,1,0,0,0,203,204,5,23,0,0,204,43,1,
        0,0,0,205,206,5,20,0,0,206,45,1,0,0,0,27,49,57,62,68,72,76,78,83,
        87,91,94,102,109,111,114,120,133,139,146,150,155,161,165,172,181,
        190,201
    ]

class FCSParser ( Parser ):

    grammarFileName = "FCSParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'['", "']'", "'|'", "'&'", 
                     "'!'", "'/'", "'{'", "'}'", "'+'", "'*'", "'?'", "','", 
                     "'='", "'!='", "':'", "'within'" ]

    symbolicNames = [ "<INVALID>", "L_PAREN", "R_PAREN", "L_SQUARE_BRACKET", 
                      "R_SQUARE_BRACKET", "OR", "AND", "NOT", "FWD_SLASH", 
                      "L_CURLY_BRACKET", "R_CURLY_BRACKET", "Q_ONE_OR_MORE", 
                      "Q_ZERO_OR_MORE", "Q_ZERO_OR_ONE", "Q_COMMA", "OPERATOR_EQ", 
                      "OPERATOR_NE", "COLON", "WITHIN", "SIMPLE_WITHIN_SCOPE", 
                      "REGEXP_FLAGS", "IDENTIFIER", "INTEGER", "REGEXP", 
                      "QUOTED_STRING", "Space" ]

    RULE_query = 0
    RULE_main_query = 1
    RULE_query_disjunction = 2
    RULE_query_sequence = 3
    RULE_query_group = 4
    RULE_query_simple = 5
    RULE_quantifier = 6
    RULE_query_implicit = 7
    RULE_query_segment = 8
    RULE_within_part = 9
    RULE_within_part_simple = 10
    RULE_expression = 11
    RULE_expression_or = 12
    RULE_expression_and = 13
    RULE_expression_group = 14
    RULE_expression_not = 15
    RULE_expression_basic = 16
    RULE_attribute = 17
    RULE_qualifier = 18
    RULE_identifier = 19
    RULE_regexp = 20
    RULE_regexp_pattern = 21
    RULE_regexp_flag = 22

    ruleNames =  [ "query", "main_query", "query_disjunction", "query_sequence", 
                   "query_group", "query_simple", "quantifier", "query_implicit", 
                   "query_segment", "within_part", "within_part_simple", 
                   "expression", "expression_or", "expression_and", "expression_group", 
                   "expression_not", "expression_basic", "attribute", "qualifier", 
                   "identifier", "regexp", "regexp_pattern", "regexp_flag" ]

    EOF = Token.EOF
    L_PAREN=1
    R_PAREN=2
    L_SQUARE_BRACKET=3
    R_SQUARE_BRACKET=4
    OR=5
    AND=6
    NOT=7
    FWD_SLASH=8
    L_CURLY_BRACKET=9
    R_CURLY_BRACKET=10
    Q_ONE_OR_MORE=11
    Q_ZERO_OR_MORE=12
    Q_ZERO_OR_ONE=13
    Q_COMMA=14
    OPERATOR_EQ=15
    OPERATOR_NE=16
    COLON=17
    WITHIN=18
    SIMPLE_WITHIN_SCOPE=19
    REGEXP_FLAGS=20
    IDENTIFIER=21
    INTEGER=22
    REGEXP=23
    QUOTED_STRING=24
    Space=25

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class QueryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def main_query(self):
            return self.getTypedRuleContext(FCSParser.Main_queryContext,0)


        def EOF(self):
            return self.getToken(FCSParser.EOF, 0)

        def WITHIN(self):
            return self.getToken(FCSParser.WITHIN, 0)

        def within_part(self):
            return self.getTypedRuleContext(FCSParser.Within_partContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery" ):
                listener.enterQuery(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery" ):
                listener.exitQuery(self)




    def query(self):

        localctx = FCSParser.QueryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_query)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.main_query()
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==18:
                self.state = 47
                self.match(FCSParser.WITHIN)
                self.state = 48
                self.within_part()


            self.state = 51
            self.match(FCSParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Main_queryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query_simple(self):
            return self.getTypedRuleContext(FCSParser.Query_simpleContext,0)


        def query_group(self):
            return self.getTypedRuleContext(FCSParser.Query_groupContext,0)


        def query_sequence(self):
            return self.getTypedRuleContext(FCSParser.Query_sequenceContext,0)


        def query_disjunction(self):
            return self.getTypedRuleContext(FCSParser.Query_disjunctionContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_main_query

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMain_query" ):
                listener.enterMain_query(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMain_query" ):
                listener.exitMain_query(self)




    def main_query(self):

        localctx = FCSParser.Main_queryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_main_query)
        try:
            self.state = 57
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.query_simple()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 54
                self.query_group()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 55
                self.query_sequence()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 56
                self.query_disjunction()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_disjunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query_simple(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Query_simpleContext)
            else:
                return self.getTypedRuleContext(FCSParser.Query_simpleContext,i)


        def query_sequence(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Query_sequenceContext)
            else:
                return self.getTypedRuleContext(FCSParser.Query_sequenceContext,i)


        def query_group(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Query_groupContext)
            else:
                return self.getTypedRuleContext(FCSParser.Query_groupContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(FCSParser.OR)
            else:
                return self.getToken(FCSParser.OR, i)

        def getRuleIndex(self):
            return FCSParser.RULE_query_disjunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_disjunction" ):
                listener.enterQuery_disjunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_disjunction" ):
                listener.exitQuery_disjunction(self)




    def query_disjunction(self):

        localctx = FCSParser.Query_disjunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_query_disjunction)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.state = 59
                self.query_simple()
                pass

            elif la_ == 2:
                self.state = 60
                self.query_sequence()
                pass

            elif la_ == 3:
                self.state = 61
                self.query_group()
                pass


            self.state = 70 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 64
                self.match(FCSParser.OR)
                self.state = 68
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                if la_ == 1:
                    self.state = 65
                    self.query_simple()
                    pass

                elif la_ == 2:
                    self.state = 66
                    self.query_sequence()
                    pass

                elif la_ == 3:
                    self.state = 67
                    self.query_group()
                    pass


                self.state = 72 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==5):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_sequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query_simple(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Query_simpleContext)
            else:
                return self.getTypedRuleContext(FCSParser.Query_simpleContext,i)


        def query_group(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Query_groupContext)
            else:
                return self.getTypedRuleContext(FCSParser.Query_groupContext,i)


        def getRuleIndex(self):
            return FCSParser.RULE_query_sequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_sequence" ):
                listener.enterQuery_sequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_sequence" ):
                listener.exitQuery_sequence(self)




    def query_sequence(self):

        localctx = FCSParser.Query_sequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_query_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 76
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [3, 23]:
                    self.state = 74
                    self.query_simple()
                    pass
                elif token in [1]:
                    self.state = 75
                    self.query_group()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 78 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (((_la) & ~0x3f) == 0 and ((1 << _la) & 8388618) != 0):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_groupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_PAREN(self):
            return self.getToken(FCSParser.L_PAREN, 0)

        def R_PAREN(self):
            return self.getToken(FCSParser.R_PAREN, 0)

        def query_disjunction(self):
            return self.getTypedRuleContext(FCSParser.Query_disjunctionContext,0)


        def query_sequence(self):
            return self.getTypedRuleContext(FCSParser.Query_sequenceContext,0)


        def quantifier(self):
            return self.getTypedRuleContext(FCSParser.QuantifierContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_query_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_group" ):
                listener.enterQuery_group(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_group" ):
                listener.exitQuery_group(self)




    def query_group(self):

        localctx = FCSParser.Query_groupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_query_group)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 80
            self.match(FCSParser.L_PAREN)
            self.state = 83
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 81
                self.query_disjunction()
                pass

            elif la_ == 2:
                self.state = 82
                self.query_sequence()
                pass


            self.state = 85
            self.match(FCSParser.R_PAREN)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 14848) != 0:
                self.state = 86
                self.quantifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_simpleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def query_implicit(self):
            return self.getTypedRuleContext(FCSParser.Query_implicitContext,0)


        def query_segment(self):
            return self.getTypedRuleContext(FCSParser.Query_segmentContext,0)


        def quantifier(self):
            return self.getTypedRuleContext(FCSParser.QuantifierContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_query_simple

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_simple" ):
                listener.enterQuery_simple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_simple" ):
                listener.exitQuery_simple(self)




    def query_simple(self):

        localctx = FCSParser.Query_simpleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_query_simple)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.state = 89
                self.query_implicit()
                pass
            elif token in [3]:
                self.state = 90
                self.query_segment()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 14848) != 0:
                self.state = 93
                self.quantifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuantifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Q_ONE_OR_MORE(self):
            return self.getToken(FCSParser.Q_ONE_OR_MORE, 0)

        def Q_ZERO_OR_MORE(self):
            return self.getToken(FCSParser.Q_ZERO_OR_MORE, 0)

        def Q_ZERO_OR_ONE(self):
            return self.getToken(FCSParser.Q_ZERO_OR_ONE, 0)

        def L_CURLY_BRACKET(self):
            return self.getToken(FCSParser.L_CURLY_BRACKET, 0)

        def R_CURLY_BRACKET(self):
            return self.getToken(FCSParser.R_CURLY_BRACKET, 0)

        def INTEGER(self, i:int=None):
            if i is None:
                return self.getTokens(FCSParser.INTEGER)
            else:
                return self.getToken(FCSParser.INTEGER, i)

        def Q_COMMA(self):
            return self.getToken(FCSParser.Q_COMMA, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_quantifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuantifier" ):
                listener.enterQuantifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuantifier" ):
                listener.exitQuantifier(self)




    def quantifier(self):

        localctx = FCSParser.QuantifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_quantifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.state = 96
                self.match(FCSParser.Q_ONE_OR_MORE)
                pass
            elif token in [12]:
                self.state = 97
                self.match(FCSParser.Q_ZERO_OR_MORE)
                pass
            elif token in [13]:
                self.state = 98
                self.match(FCSParser.Q_ZERO_OR_ONE)
                pass
            elif token in [9]:
                self.state = 99
                self.match(FCSParser.L_CURLY_BRACKET)
                self.state = 111
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                if la_ == 1:
                    self.state = 100
                    self.match(FCSParser.INTEGER)
                    pass

                elif la_ == 2:
                    self.state = 102
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==22:
                        self.state = 101
                        self.match(FCSParser.INTEGER)


                    self.state = 104
                    self.match(FCSParser.Q_COMMA)
                    self.state = 105
                    self.match(FCSParser.INTEGER)
                    pass

                elif la_ == 3:
                    self.state = 106
                    self.match(FCSParser.INTEGER)
                    self.state = 107
                    self.match(FCSParser.Q_COMMA)
                    self.state = 109
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==22:
                        self.state = 108
                        self.match(FCSParser.INTEGER)


                    pass


                self.state = 113
                self.match(FCSParser.R_CURLY_BRACKET)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_implicitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def regexp(self):
            return self.getTypedRuleContext(FCSParser.RegexpContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_query_implicit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_implicit" ):
                listener.enterQuery_implicit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_implicit" ):
                listener.exitQuery_implicit(self)




    def query_implicit(self):

        localctx = FCSParser.Query_implicitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_query_implicit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.regexp()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Query_segmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_SQUARE_BRACKET(self):
            return self.getToken(FCSParser.L_SQUARE_BRACKET, 0)

        def R_SQUARE_BRACKET(self):
            return self.getToken(FCSParser.R_SQUARE_BRACKET, 0)

        def expression(self):
            return self.getTypedRuleContext(FCSParser.ExpressionContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_query_segment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuery_segment" ):
                listener.enterQuery_segment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuery_segment" ):
                listener.exitQuery_segment(self)




    def query_segment(self):

        localctx = FCSParser.Query_segmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_query_segment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.match(FCSParser.L_SQUARE_BRACKET)
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 3932290) != 0:
                self.state = 119
                self.expression()


            self.state = 122
            self.match(FCSParser.R_SQUARE_BRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Within_partContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def within_part_simple(self):
            return self.getTypedRuleContext(FCSParser.Within_part_simpleContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_within_part

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithin_part" ):
                listener.enterWithin_part(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithin_part" ):
                listener.exitWithin_part(self)




    def within_part(self):

        localctx = FCSParser.Within_partContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_within_part)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.within_part_simple()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Within_part_simpleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIMPLE_WITHIN_SCOPE(self):
            return self.getToken(FCSParser.SIMPLE_WITHIN_SCOPE, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_within_part_simple

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithin_part_simple" ):
                listener.enterWithin_part_simple(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithin_part_simple" ):
                listener.exitWithin_part_simple(self)




    def within_part_simple(self):

        localctx = FCSParser.Within_part_simpleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_within_part_simple)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 126
            self.match(FCSParser.SIMPLE_WITHIN_SCOPE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression_basic(self):
            return self.getTypedRuleContext(FCSParser.Expression_basicContext,0)


        def expression_not(self):
            return self.getTypedRuleContext(FCSParser.Expression_notContext,0)


        def expression_group(self):
            return self.getTypedRuleContext(FCSParser.Expression_groupContext,0)


        def expression_or(self):
            return self.getTypedRuleContext(FCSParser.Expression_orContext,0)


        def expression_and(self):
            return self.getTypedRuleContext(FCSParser.Expression_andContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)




    def expression(self):

        localctx = FCSParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_expression)
        try:
            self.state = 133
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 128
                self.expression_basic()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 129
                self.expression_not()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 130
                self.expression_group()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 131
                self.expression_or()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 132
                self.expression_and()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_orContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression_basic(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_basicContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_basicContext,i)


        def expression_group(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_groupContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_groupContext,i)


        def expression_not(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_notContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_notContext,i)


        def expression_and(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_andContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_andContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(FCSParser.OR)
            else:
                return self.getToken(FCSParser.OR, i)

        def getRuleIndex(self):
            return FCSParser.RULE_expression_or

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_or" ):
                listener.enterExpression_or(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_or" ):
                listener.exitExpression_or(self)




    def expression_or(self):

        localctx = FCSParser.Expression_orContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expression_or)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.state = 135
                self.expression_basic()
                pass

            elif la_ == 2:
                self.state = 136
                self.expression_group()
                pass

            elif la_ == 3:
                self.state = 137
                self.expression_not()
                pass

            elif la_ == 4:
                self.state = 138
                self.expression_and()
                pass


            self.state = 148 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 141
                    self.match(FCSParser.OR)
                    self.state = 146
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
                    if la_ == 1:
                        self.state = 142
                        self.expression_basic()
                        pass

                    elif la_ == 2:
                        self.state = 143
                        self.expression_group()
                        pass

                    elif la_ == 3:
                        self.state = 144
                        self.expression_not()
                        pass

                    elif la_ == 4:
                        self.state = 145
                        self.expression_and()
                        pass



                else:
                    raise NoViableAltException(self)
                self.state = 150 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_andContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression_basic(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_basicContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_basicContext,i)


        def expression_group(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_groupContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_groupContext,i)


        def expression_not(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(FCSParser.Expression_notContext)
            else:
                return self.getTypedRuleContext(FCSParser.Expression_notContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(FCSParser.AND)
            else:
                return self.getToken(FCSParser.AND, i)

        def getRuleIndex(self):
            return FCSParser.RULE_expression_and

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_and" ):
                listener.enterExpression_and(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_and" ):
                listener.exitExpression_and(self)




    def expression_and(self):

        localctx = FCSParser.Expression_andContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expression_and)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 155
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18, 19, 20, 21]:
                self.state = 152
                self.expression_basic()
                pass
            elif token in [1]:
                self.state = 153
                self.expression_group()
                pass
            elif token in [7]:
                self.state = 154
                self.expression_not()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 163 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 157
                    self.match(FCSParser.AND)
                    self.state = 161
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [18, 19, 20, 21]:
                        self.state = 158
                        self.expression_basic()
                        pass
                    elif token in [1]:
                        self.state = 159
                        self.expression_group()
                        pass
                    elif token in [7]:
                        self.state = 160
                        self.expression_not()
                        pass
                    else:
                        raise NoViableAltException(self)


                else:
                    raise NoViableAltException(self)
                self.state = 165 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,22,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_groupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def L_PAREN(self):
            return self.getToken(FCSParser.L_PAREN, 0)

        def R_PAREN(self):
            return self.getToken(FCSParser.R_PAREN, 0)

        def expression_basic(self):
            return self.getTypedRuleContext(FCSParser.Expression_basicContext,0)


        def expression_not(self):
            return self.getTypedRuleContext(FCSParser.Expression_notContext,0)


        def expression_or(self):
            return self.getTypedRuleContext(FCSParser.Expression_orContext,0)


        def expression_and(self):
            return self.getTypedRuleContext(FCSParser.Expression_andContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_expression_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_group" ):
                listener.enterExpression_group(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_group" ):
                listener.exitExpression_group(self)




    def expression_group(self):

        localctx = FCSParser.Expression_groupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_expression_group)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 167
            self.match(FCSParser.L_PAREN)
            self.state = 172
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,23,self._ctx)
            if la_ == 1:
                self.state = 168
                self.expression_basic()
                pass

            elif la_ == 2:
                self.state = 169
                self.expression_not()
                pass

            elif la_ == 3:
                self.state = 170
                self.expression_or()
                pass

            elif la_ == 4:
                self.state = 171
                self.expression_and()
                pass


            self.state = 174
            self.match(FCSParser.R_PAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_notContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(FCSParser.NOT, 0)

        def expression_basic(self):
            return self.getTypedRuleContext(FCSParser.Expression_basicContext,0)


        def expression_not(self):
            return self.getTypedRuleContext(FCSParser.Expression_notContext,0)


        def expression_or(self):
            return self.getTypedRuleContext(FCSParser.Expression_orContext,0)


        def expression_and(self):
            return self.getTypedRuleContext(FCSParser.Expression_andContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_expression_not

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_not" ):
                listener.enterExpression_not(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_not" ):
                listener.exitExpression_not(self)




    def expression_not(self):

        localctx = FCSParser.Expression_notContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_expression_not)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self.match(FCSParser.NOT)
            self.state = 181
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.state = 177
                self.expression_basic()
                pass

            elif la_ == 2:
                self.state = 178
                self.expression_not()
                pass

            elif la_ == 3:
                self.state = 179
                self.expression_or()
                pass

            elif la_ == 4:
                self.state = 180
                self.expression_and()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expression_basicContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def attribute(self):
            return self.getTypedRuleContext(FCSParser.AttributeContext,0)


        def regexp(self):
            return self.getTypedRuleContext(FCSParser.RegexpContext,0)


        def OPERATOR_EQ(self):
            return self.getToken(FCSParser.OPERATOR_EQ, 0)

        def OPERATOR_NE(self):
            return self.getToken(FCSParser.OPERATOR_NE, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_expression_basic

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression_basic" ):
                listener.enterExpression_basic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression_basic" ):
                listener.exitExpression_basic(self)




    def expression_basic(self):

        localctx = FCSParser.Expression_basicContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_expression_basic)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            self.attribute()
            self.state = 184
            _la = self._input.LA(1)
            if not(_la==15 or _la==16):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 185
            self.regexp()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AttributeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self):
            return self.getTypedRuleContext(FCSParser.IdentifierContext,0)


        def qualifier(self):
            return self.getTypedRuleContext(FCSParser.QualifierContext,0)


        def COLON(self):
            return self.getToken(FCSParser.COLON, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_attribute

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAttribute" ):
                listener.enterAttribute(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAttribute" ):
                listener.exitAttribute(self)




    def attribute(self):

        localctx = FCSParser.AttributeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_attribute)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.state = 187
                self.qualifier()
                self.state = 188
                self.match(FCSParser.COLON)


            self.state = 192
            self.identifier()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(FCSParser.IDENTIFIER, 0)

        def WITHIN(self):
            return self.getToken(FCSParser.WITHIN, 0)

        def SIMPLE_WITHIN_SCOPE(self):
            return self.getToken(FCSParser.SIMPLE_WITHIN_SCOPE, 0)

        def REGEXP_FLAGS(self):
            return self.getToken(FCSParser.REGEXP_FLAGS, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_qualifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifier" ):
                listener.enterQualifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifier" ):
                listener.exitQualifier(self)




    def qualifier(self):

        localctx = FCSParser.QualifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_qualifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 3932160) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(FCSParser.IDENTIFIER, 0)

        def WITHIN(self):
            return self.getToken(FCSParser.WITHIN, 0)

        def SIMPLE_WITHIN_SCOPE(self):
            return self.getToken(FCSParser.SIMPLE_WITHIN_SCOPE, 0)

        def REGEXP_FLAGS(self):
            return self.getToken(FCSParser.REGEXP_FLAGS, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)




    def identifier(self):

        localctx = FCSParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_identifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 3932160) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RegexpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def regexp_pattern(self):
            return self.getTypedRuleContext(FCSParser.Regexp_patternContext,0)


        def FWD_SLASH(self):
            return self.getToken(FCSParser.FWD_SLASH, 0)

        def regexp_flag(self):
            return self.getTypedRuleContext(FCSParser.Regexp_flagContext,0)


        def getRuleIndex(self):
            return FCSParser.RULE_regexp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRegexp" ):
                listener.enterRegexp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRegexp" ):
                listener.exitRegexp(self)




    def regexp(self):

        localctx = FCSParser.RegexpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_regexp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
            self.regexp_pattern()
            self.state = 201
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 199
                self.match(FCSParser.FWD_SLASH)
                self.state = 200
                self.regexp_flag()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Regexp_patternContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGEXP(self):
            return self.getToken(FCSParser.REGEXP, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_regexp_pattern

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRegexp_pattern" ):
                listener.enterRegexp_pattern(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRegexp_pattern" ):
                listener.exitRegexp_pattern(self)




    def regexp_pattern(self):

        localctx = FCSParser.Regexp_patternContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_regexp_pattern)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 203
            self.match(FCSParser.REGEXP)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Regexp_flagContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REGEXP_FLAGS(self):
            return self.getToken(FCSParser.REGEXP_FLAGS, 0)

        def getRuleIndex(self):
            return FCSParser.RULE_regexp_flag

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRegexp_flag" ):
                listener.enterRegexp_flag(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRegexp_flag" ):
                listener.exitRegexp_flag(self)




    def regexp_flag(self):

        localctx = FCSParser.Regexp_flagContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_regexp_flag)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
            self.match(FCSParser.REGEXP_FLAGS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





