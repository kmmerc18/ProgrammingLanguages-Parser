#3aeee2ffb6bdcec698011572b6bbcaf180807419 

import lexer
import ply.yacc as yacc

from ast1 import *

###################
# Parser for Cool #
###################

# possible cool tokens
tokens = [ 'AT', 'CASE', 'CLASS', 'COLON', 'COMMA', 'DIVIDE', 'DOT',
'ELSE', 'EQUALS', 'ESAC', 'FALSE', 'FI', 'IDENTIFIER', 'IF', 'IN', 'INHERITS',
'INTEGER', 'ISVOID', 'LARROW', 'LBRACE', 'LE', 'LET', 'LOOP', 'LPAREN', 'LT',
'MINUS', 'NEW', 'NOT', 'OF', 'PLUS', 'POOL', 'RARROW', 'RBRACE', 'RPAREN', 
'SEMI', 'STRING', 'THEN', 'TILDE', 'TIMES', 'TRUE', 'TYPE', 'WHILE' ]

# precedence increases downward
precedence = (
    ('right', 'LARROW'),
    ('right', 'NOT'),
    ('nonassoc', 'LE', 'LT', 'EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ISVOID'),
    ('right', 'TILDE'),
    ('right', 'AT'),
    ('right', 'DOT')
 )

# create ast starting with a list of classes
def p_program(p):
    """program : class_list"""
    p[0] = CoolProgram(CoolList(p[1]))                  # class list as CoolList

# create classes
def p_class(p):
    """class : CLASS TYPE LBRACE RBRACE
            | CLASS TYPE INHERITS TYPE LBRACE RBRACE
            | CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE
            | CLASS TYPE LBRACE feature_list RBRACE"""
    # no inherits or feature list
    if len(p) == 5:
        p[0] = CoolClass(
                CoolIdentifier(p.lineno(2), p[2]))      # type as id 
    
    # inherits, but no feature list
    elif len(p) == 7:
        p[0] = CoolClass(
                CoolIdentifier(p.lineno(2), p[2]),      # type as id 
                None,                                   # no feature list
                CoolIdentifier(p.lineno(4), p[4]))      # inherit type as id 
    
    # inherits and has a feature list
    elif len(p) == 8:
        p[0] = CoolClass(
                CoolIdentifier(p.lineno(2), p[2]),      # type as id  
                CoolList(p[6]),                         # feature list as CoolList
                CoolIdentifier(p.lineno(4), p[4]))      # inherit type as id 
    
    # no inherits, but as a feature list
    else:
        p[0] = CoolClass(
                CoolIdentifier(p.lineno(2), p[2]),      # name as id  
                CoolList(p[4]))                         # feature list as CoolList
    

# create class list with zero or more classes
def p_class_list(p):
    """class_list : class SEMI class_list
        | empty"""
    # empty list for no classes
    if len(p) == 2:
        p[0] = []
    
    # multiple classes in a list
    else:
        p[0] = [p[1]] + p[3]

# create feature
def p_feature(p):
    """feature : IDENTIFIER COLON TYPE
        | IDENTIFIER COLON TYPE LARROW expression
        | IDENTIFIER LPAREN formal_list RPAREN COLON TYPE LBRACE expression RBRACE
        | IDENTIFIER LPAREN RPAREN COLON TYPE LBRACE expression RBRACE"""
    # attribute no init
    if len(p) == 4:
        p[0] = CoolFeature(
                CoolIdentifier(p.lineno(1), p[1]),        # name as id 
                CoolIdentifier(p.lineno(3), p[3]))      # type as id
    # attribute init
    elif len(p) == 6:
        p[0] = CoolFeature(
                CoolIdentifier(p.lineno(1), p[1]),      # name as id 
                CoolIdentifier(p.lineno(3), p[3]),      # type as id 
                p[5])                                   # init expression
    
    # method
    elif p[4].upper() == 'RPAREN':
        # has formal list
        p[0] = CoolFeature(
                CoolIdentifier(p.lineno(1), p[1]),      # name as id 
                CoolIdentifier(p.lineno(6), p[6]),      # type as id                                        # no init
                formal_list=CoolList(p[3]),             # formal list as CoolList
                body=p[8])                              # body expression
    elif p[3].upper() == 'RPAREN':      
        # no formal list
        p[0] = CoolFeature(
                CoolIdentifier(p.lineno(1), p[1]),      # name as id 
                CoolIdentifier(p.lineno(5), p[5]),      # type as id 
                body=p[7])                              # body expression

# create feature list with zero or more features
def p_feature_list(p):
    """feature_list : feature SEMI feature_list
        | empty"""
    # empty list for no features
    if len(p) == 2:
        p[0] = []

    # multiple features in a list
    else:
        p[0] = [p[1]] + p[3]

# create formal
def p_formal(p):
    """formal : IDENTIFIER COLON TYPE"""
    p[0] = CoolFormal(
            CoolIdentifier(p.lineno(1), p[1]),          # name as id
            CoolIdentifier(p.lineno(3), p[3]))          # type as id

# create formal list with one or more formals
def p_formal_list(p):
    """formal_list : formal COMMA formal_list
        | formal"""
    # a single formal in a list
    if len(p) == 2:
        p[0] = [p[1]]

    # multiple formals in a list
    else:
        p[0] = [p[1]] + p[3]

# create expressions
def p_expression(p):
    """expression : expr_assign
        | expr_let 
        | expr_dispatch
        | expr_loop
        | expr_block
        | expr_newtype
        | expr_mathcondition
        | expr_ID
        | expr_int
        | expr_string
        | expr_bool
        | expr_case
        | LPAREN expression RPAREN """
    # omit the parentheses - just take the expression
    if len(p) == 4:
        p[0] = p[2]
    
    # create a specific type of expression
    else:
        p[0] = p[1]

# create an expression list with zero or more expressions
def p_expression_list(p):
    """expression_list : expression SEMI expression_list
        | empty"""
    # empty list for no expressions
    if len(p) == 2:
        p[0] = []
    
    # multiple expressions in a list
    else:
        p[0] = [p[1]] + p[3]

# create assign expression
def p_expr_assign(p):
    """expr_assign : IDENTIFIER LARROW expression"""
    p[0] = CoolExprAssign(
            p.lineno(1),                                # line number 
            CoolIdentifier(p.lineno(1), p[1]),          # name as id
            p[3])                                       # rhs of assignment

# create a let expression
def p_expr_let(p):
    """expr_let : LET binding_list IN expression"""
    p[0] = CoolExprLet(
            p.lineno(1),                                # line number
            p[4],                                       # body expression
            CoolList(p[2]))                             # binding list

# create bindings for let
def p_binding(p):
    """ binding : IDENTIFIER COLON TYPE
        |  IDENTIFIER COLON TYPE LARROW expression """
    # binding no_init
    if len(p) == 4:
        p[0] = CoolExprBinding(
                CoolIdentifier(p.lineno(1), p[1]),      # variable as an id
                CoolIdentifier(p.lineno(3), p[3]))      # type as an id
    
    # binding init
    else:
        # as above, but with a initalizing expression
        p[0] = CoolExprBinding(
                CoolIdentifier(p.lineno(1), p[1]),      # var as id
                CoolIdentifier(p.lineno(3), p[3]),      # type as id
                p[5])                                   # init expression

# a binding list must have at least one or more bindings
def p_binding_list(p):
    """ binding_list : binding COMMA binding_list 
        | binding """
    # single binding in a list 
    if len(p) == 2:
        p[0] = [p[1]]

    # multiple bindings in a list
    else:
        p[0] = [p[1]] + p[3] 

def p_expr_dispatch(p):
    """expr_dispatch : expression DOT IDENTIFIER LPAREN args_list RPAREN  
        | expression DOT IDENTIFIER LPAREN RPAREN
        | expression AT TYPE DOT IDENTIFIER LPAREN args_list RPAREN
        | expression AT TYPE DOT IDENTIFIER LPAREN RPAREN
        | IDENTIFIER LPAREN args_list RPAREN 
        | IDENTIFIER LPAREN RPAREN"""
    
    # dynamic dispatch - has method name, args_list, and an expression
    if len(p) == 7:
        # with an args list
        p[0] = CoolExprDispatch(
            p.lineno(2),                            # line number
            CoolIdentifier(p.lineno(3), p[3]),      # method name as id
            CoolList(p[5]),                         # args list as CoolList
            p[1])                                   # expression
    elif len(p) == 6:
        # no args list
        p[0] = CoolExprDispatch(
                p.lineno(2),                        # line number
                CoolIdentifier(p.lineno(3), p[3]),  # method as id
                None,                               # no arg list
                p[1])                               # expression
    
    # static dispatch - same as dynamic but with a type specified
    elif len(p) == 9:
        # with an args list
        p[0] = CoolExprDispatch(
                p.lineno(2),                        # line number
                CoolIdentifier(p.lineno(5), p[5]),  # method name as id
                CoolList(p[7]),                     # args list as CoolList
                p[1],                               # expression
                CoolIdentifier(p.lineno(3), p[3]))  # static type as id
    elif len(p) == 8:
        # no args list
        p[0] = CoolExprDispatch(
                p.lineno(2),                        # line number 
                CoolIdentifier(p.lineno(5), p[5]),  # method name as id
                None,                               # no arg list
                p[1],                               # expression
                CoolIdentifier(p.lineno(3), p[3]))  # static type as id
    
    # self dispatch - has a method name and an args list
    elif len(p) == 5:
        # has an arg list
        p[0] = CoolExprDispatch(
                p.lineno(2),                        # line number
                CoolIdentifier(p.lineno(1), p[1]),  # method name as id
                CoolList(p[3]))                     # args list as CoolList
    elif len(p) == 4:
        # no args list
        p[0] = CoolExprDispatch(
                p.lineno(1),                        # line number
                CoolIdentifier(p.lineno(1),         # method name as id
                p[1]))                              # expression

# create an args list for dispatch with one or more expressions    
def p_args_list(p):
    """args_list : expression COMMA args_list
        | expression"""
    # single expression in a list 
    if len(p) == 2:
        p[0] = [p[1]]

    # multiple expressions in a list    
    else:
        p[0] = [p[1]] + p[3]

def p_expr_loop(p):
    """ expr_loop : IF expression THEN expression ELSE expression FI
        | WHILE expression LOOP expression POOL """
    # create an if expression
    if p[1].upper() == 'IF':
        p[0] = CoolExprIf(
            p.lineno(1),                            # line number
            p[2],                                   # predicate
            p[4],                                   # then expression
            p[6])                                   # else expression
    
    # create a while loop
    else:
        p[0] = CoolExprWhile(
                p.lineno(1),                        # line number
                p[2],                               # predicate
                p[4])                               # body expression

# create an expression block
def p_expr_block(p):
    """ expr_block : LBRACE expression_list RBRACE"""
    p[0] = CoolExprBlock(
            p.lineno(1),                            # line number
            CoolList(p[2]))                         # expression list

# create a case expression
def p_expr_case(p):
    """expr_case : CASE expression OF element_list ESAC """  
    p[0] = CoolExprCase(    
            p.lineno(1),                            # line number
            p[2],                                   # case expression
            CoolList(p[4]))                         # case element list as CoolList

# create case elements for the case
def p_expr_case_element(p):
    """ expr_case_element : IDENTIFIER COLON TYPE RARROW expression SEMI"""
    p[0] = CoolExprCaseElement(
            p.lineno(1),                            # line number
            CoolIdentifier(p.lineno(1), p[1]),      # variable as id
            CoolIdentifier(p.lineno(3), p[3]),      # type as id
            p[5])                                   # expression

# create a list of elements for case
def p_element_list(p):
    """ element_list : expr_case_element element_list
        | expr_case_element """
    # a single element in a list
    if len(p) == 2:
        p[0] = [p[1]]

    # multiple elements in a list
    else:
        p[0] = [p[1]] + p[3] 

# create new type expression
def p_expr_newtype(p):
    """ expr_newtype : NEW TYPE """ 
    p[0] = CoolExprNew(
            p.lineno(1),                            # line number
            CoolIdentifier(p.lineno(2), p[2]))      # type as id                              

# create math/condition/isvoid expressions
def p_expr_mathcondition(p):
    """expr_mathcondition : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | expression LT expression
        | expression LE expression
        | expression EQUALS expression
        | TILDE expression
        | NOT expression
        | ISVOID expression """

    # create binary operators
    if len(p) == 4:
        # PLUS, MINUS, TIMES, DIVIDE, LT, LE, EQUALS all have the same constuction
        # just a different operator   
        if p[2].upper() == 'PLUS':
            p[0] = CoolExprIsVoidMathConditions(
                    p.lineno(2),                    # line number                  
                    "plus",                         # operation
                    p[1],                           # x expression 
                    p[3])                           # y expression
        elif p[2].upper() == 'MINUS':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "minus", p[1], p[3])
        elif p[2].upper() == 'TIMES':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "times", p[1], p[3])
        elif p[2].upper() == 'DIVIDE':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "divide", p[1], p[3])
        elif p[2].upper() == 'LT':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "lt", p[1], p[3])
        elif p[2].upper() == 'LE':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "le", p[1], p[3])
        elif p[2].upper() == 'EQUALS':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(2), "eq", p[1], p[3])
    
    # single operators
    elif len(p) == 3:
        # TILDE, NOT, ISVOID all have the same constuction just a different operator
        if p[1].upper() == 'TILDE':
            p[0] = CoolExprIsVoidMathConditions(
                    p.lineno(1),                    # line number
                    "negate",                       # operator
                    p[2])                           # expression
        elif p[1].upper() == 'NOT':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(1), "not", p[2])
        elif p[1].upper() == 'ISVOID':
            p[0] = CoolExprIsVoidMathConditions(p.lineno(1), "isvoid", p[2])

# match identifiers
def p_expr_ID(p):
    """ expr_ID : IDENTIFIER"""
    p[0] = CoolExprID(
            p.lineno(1),                            # line number 
            CoolIdentifier(p.lineno(1), p[1]))      # id as id

# match integers
def p_expr_int(p):
    """ expr_int : INTEGER"""
    p[0] = CoolExprInt(
            p.lineno(1),                            # line number
            p[1])                                   # constant (int)

# match strings
def p_expr_string(p):
    """ expr_string : STRING"""
    p[0] = CoolExprString(
            p.lineno(1),                            # line number
            p[1])                                   # constant (string)

# match boolean tokens
def p_expr_bool(p):
    """expr_bool : TRUE
        | FALSE"""
    if p[1].upper() == 'TRUE':
        p[0] = CoolExprBool(
                p.lineno(1),                         # line number
                "true")                              # boolean type
   
    # false is the same as true, just different bool type
    else:
        p[0] = CoolExprBool(p.lineno(1), "false")

# match nothing
def p_empty(p):
    """empty : """
    pass

# catch any thing that is not matched by the grammer
def p_error(p):
    if p is None:
        print("Unexpected end of file!")
        exit(0)
    else:
        # p is the token where we have a syntax error
        print("ERROR: {}: Parser: error on token {}".format(p.lineno, p.value))
        exit(0)


# main program
if __name__ == '__main__':
    import sys

    # create the parse and lexer
    lexer = lexer.Lexer(sys.stdin)
    parser = yacc.yacc()

    # create the ast
    program = parser.parse(lexer=lexer)

    # print the ast
        # replaced the new line char with an empty string 
        # to remove extra empty line
    print(program, end="")
