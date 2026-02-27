parser grammar FCSParser;
options { tokenVocab=FCSLexer; }
/* 
 * Parser for FCS Core FCS-QL version 2.0
 * 20150501- /ljo
 */

query
    : main_query (WITHIN within_part)? EOF
    ;


main_query
    : query_simple
    | query_group
    | query_sequence
    | query_disjunction
    ;


query_disjunction
    : (query_simple | query_sequence | query_group)
            (OR (query_simple | query_sequence | query_group))+
    ;


query_sequence
    : (query_simple | query_group)+
    ;


query_group
    : L_PAREN (query_disjunction | query_sequence) R_PAREN quantifier?
    ;


query_simple
    : (query_implicit | query_segment) quantifier?
    ;


quantifier
    : (Q_ONE_OR_MORE | Q_ZERO_OR_MORE | Q_ZERO_OR_ONE |
        (L_CURLY_BRACKET
            (INTEGER |
             INTEGER? Q_COMMA INTEGER |
             INTEGER Q_COMMA INTEGER?) R_CURLY_BRACKET))
    ;


query_implicit
    : regexp
    ;


query_segment
    : L_SQUARE_BRACKET expression? R_SQUARE_BRACKET     /* [ expression? ] */
    ;


within_part
    : within_part_simple
    ;


within_part_simple
    : SIMPLE_WITHIN_SCOPE
    ;


// !/NOT will bind the strongest (more intuitive)
// !a="b" | c="d"  <==> (!a="b") | c="d"
expression
    : expression_basic
    | expression_group
    | expression_or
    | expression_and
    | expression_not
    ;


expression_or
    : (expression_basic | expression_group | expression_and | expression_not) 
        (OR (expression_basic | expression_group | expression_and | expression_not))+
    ;


// expression_and does not allow expression_or in first part due to left-recursion
// this will currently bind &/AND tighter together than |/OR expressions
// a="b" | c="d" & e="f"  <==>  a="b" | (c="d" & e="f")
// a="b" & c="d" | e="f"  <==>  (a="b" & c="d") | e="f"
expression_and
    : (expression_basic | expression_group | expression_not)
        (AND (expression_basic | expression_group | expression_or | expression_not))+
    ;


expression_group
    : L_PAREN (expression_basic | expression_group | expression_or | expression_and | expression_not) R_PAREN
    ;


expression_not
    : NOT (expression_basic | expression_group | expression_not | expression_or | expression_and)
    ;


expression_basic
    : attribute (OPERATOR_EQ | OPERATOR_NE) regexp
    ;


attribute
    : (qualifier COLON)? identifier
    ;


qualifier
    : (IDENTIFIER | WITHIN | SIMPLE_WITHIN_SCOPE | REGEXP_FLAGS)
    ;


identifier
    : (IDENTIFIER | WITHIN | SIMPLE_WITHIN_SCOPE | REGEXP_FLAGS)
    ;


regexp
    : regexp_pattern (FWD_SLASH regexp_flag)?
    ;


regexp_pattern
    : REGEXP
    ;


regexp_flag
    : REGEXP_FLAGS
    ;
