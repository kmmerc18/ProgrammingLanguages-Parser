    The components of project 3 include parser.py, ast1.py, references.txt, good.cl, and bad.cl. Inside parser.py, 
we create the grammar from which a parser is automatically generated via PLY. Many classes used inside the parser are 
ones created by us in ast1.py, so this is imported immediately. Next is a list of tokens, which our grammar will recognize 
from the lex file passed in at run time. Next, we define precedence, like the order of operations for the various tokens 
as specified in the COOL reference manual. This prevents shift/reduce errors for ambiguous grammar.

    The start method we define as p_program, which is the grammar rule for the first class in a program (often main) which 
contains a list of further classes. We call this type a CoolProgram type as identified in ast1.py. The next grammar definition 
is p_class, which is the grammar rule for well-formed class definitions including classes that take no arguments and do not 
inherit from another class, those that inherit but take no arguments, those that inherit and take arguments, and those that 
take arguments but do not inherit. The class type and the type that a class inherits from are passed as CoolIdentifiers into a 
CoolClass, and those that take arguments are passed them as a CoolList.

    At this point we’ve mentioned two types of lists, feature_lists as a CoolList (for arguments in a CoolClass) and class_list as 
a CoolList(for classes in a program), so we define them next. p_class_list will contain nothing, or a list of individual classes, while 
p_feature_list will contain nothing or a list of individual features. We’ve already defined p_class, which means we have to define 
p_feature next. p_feature can take a number of forms, depending on if the feature is a method or not, and whether it is initialized. 
From our code commenting it should be clear which case belongs to which situation. Methods further may have associated formal lists, 
which we define later. A list of methods or attributes is created with p_feature_list. Formals are then defined with p_formal, and have a 
similar list format, p_formal_list, to that p_feature_list.

    There are 13 different types of expressions we consider in our grammar for COOL: an assignment, a let statement, a dispatch, 
a loop, a block, a new statement, a math condition, an identifier, int, string, boolean, case, or simply an expression 
surrounded by parentheses. The only case where an expression is matched via a grammar containing more than one token is when it is 
the lattermost type. These can be combined together to create an expression list as well, which is used in block expressions. All the 
types of expressions we chose to break into individual definitions for ease of class writing in ast1.py, as well as clarity in our parser
code, though integers and strings (p_expr_int and p_expr_string) are near identical in code and could have been combined. We ultimately did 
combine all the math expressions with grammar for tilde, not, and isvoid because all ten were constructed similarly, and we didn't have 
difficulty implementing this section of code early on the way we had for integer and string.

    Looking at p_expression_list, p_expr_list, p_element_list and p_binding_list, they are equally straighforward as all the other lists mentioned in parser.py. 
Let statements were similarly simplistic, but binding statements did provide some interesting issues early on in the coding process. Due to a series of 
off-by-one errors, determining if a binding included an initializing expression or not was a challenge, but we altered our approach and found these errors 
and these sections are now clearly commented to verify which case is which. A similar issue occured under p_expr_dispatch involving off-by-one errors
and confusion as to which if/elif statement belonged to which production of the grammar, but these are well commented. A recent change to the dynamic
dispatch case with no argument list (args_list) was, rather than passing the CoolExprDispatch an empty list, passing it "None", which helped smooth over
repr issues in ast1.py. This same change was made in the static dispatch case. Despite these issues, the coding for the self dispatch case went relatively
smoothly. In terms of the p_expr_loop definition, the primary issue was a series of off-by-one errors much like those seen in the binding section.

    Cases proved complex in terms of translating the grammar as listed in the COOL reference manual into that recognized by our parser. The terminology, including a
kleene star in an unusual spot, gave us some confusion, but ultimately cases are very similar to many other areas of the grammar that contain lists, so we managed
to break the grammar into a case that contains a list of elements that follows a fairly standard list grammar compared to the other lists in parser.py (see p_element_list), 
then the grammar of the list also contains the grammar of the elements in the list (see p_expr_case_element).

    Compared to cases, new types were easy to write, involving only one definition that contained no if/elif statements. Though the math conditions appear 
complex, they proved not to be, and integrating them went smoothly.

    The end of our code includes error catching statements, as seen in the video guides, to catch if the program reaches the end of the lex file before it was
meant to, as well as print out where any unrecognized or un-handled token appears in the file. The main program runs our parser over a given file, and prints the results.
The print statement contains "end =""" to prevent an excess newline from printing that differs from the output of the COOL parser. 

    Written in parallel to parser.py is ast1.py, which provides a series of classes that specify output for the COOL structures seen in parser.py.
Each type of grammar has its own repr, specifying any output specific to the class itself, and adds on the output of its components' reprs. For example, a class outputs 
the repr of its name (which is a CoolIdentifier), then "no_inherits" or "inherits" for whether it inherits from another class, then the repr for the CoolClass it inherits from (if any),
followed by either 0, or the repr for its feature_list, which is a CoolList. Though the CoolClass's attributes may include a CoolIdentifier, CoolClass, and CoolList, the individual
class itself only needs to call on the repr for those classes, not know how to print the data from each of those classes itself. In this way we avoid redundant code, which allows us
to make changes as needed in only one place in ast1.py, rather than multiple. Once we determined the correct order/input for our classes in parser.py, the actual outputs written as reprs 
were straightforward to write.

    For our test cases in good.cl and bad.cl, we utilized the Cool Syntax definitions as guidelines to test a wide range of options. Good.cl includes test for various constructions of classes
like some combination of inheritance and feature lists.  With in these test classes, there are a variety of features. These have varying combinations of formals, types, and expressions. The
internal expressions test the recursive nature of expressions. Many of the expressions have other expression type embedded within them. To ensure that valid COOL code was written in good.cl,
we used the COOL Parser to check for syntax errors. Similarly, for bad.cl, the definitions were used to determine constructions that were not valid in COOL. This file includes various expressions
that have their components removed, added, or rearranged. Examples include missing semicolons in the class list, no types for various declarations, and omitted tokens and expressions for structures 
like while, if and let statements. s