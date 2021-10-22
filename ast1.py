#3aeee2ffb6bdcec698011572b6bbcaf180807419 

##### AST classes ######
# Classes to provide the proper output for various COOL structures #

# Program (AST) 
    # output the class list
class CoolProgram:
    def __init__(self, class_list):
        self.class_list = class_list

    def __repr__(self):
        # print the elements in the class list
        return repr(self.class_list)

# List
    # output the number of elements and then each element
class CoolList:
    def __init__(self, elements):
        self.elements = elements
        self.size = len(elements)
    
    def __repr__(self):
        output = str(self.size) + "\n"
        for e in self.elements:
            output += repr(e)
        return output

# Class
    # output the class name, no_inherits/ inherits and the superclass, and then
    # the list of features
class CoolClass:
    def __init__(self, name, feature_list=None, superclass=None):
        self.name = name                    # should print as an id
        self.superclass = superclass        # also print as id
        self.feature_list = feature_list    # print as a list
    
    def __repr__(self):
        output = repr(self.name)

        if self.superclass == None:
            output += "no_inherits\n"
        else:
            output += "inherits\n" + repr(self.superclass)
        
        if self.feature_list == None:
            output += "0\n" 
        else:
            output += repr(self.feature_list)

        return output

# Identifier
    # Output the line number of the id from the source file and the name of the id
class CoolIdentifier:
    def __init__(self, lineno, id_string):
        self.lineno = lineno
        self.id_string = id_string

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += self.id_string + "\n"
        return output

# Feature
    # output the name of the feature then:
        # attribute_no_init with the name and type
        # attribute_init with the name, type, and init expression
        # method with the name, formals list, type, and body expression
class CoolFeature:
    def __init__(self, name, feat_type, init=None, formal_list=None, body=None):
        self.name = name
        self.feat_type = feat_type
        self.init = init
        self.formal_list = formal_list
        self.body = body
    
    def __repr__(self):
        if self.init == None:
            if self.body == None:
                output = "attribute_no_init\n"
                output += repr(self.name) + repr(self.feat_type)
            else:
                output = "method\n"
                output += repr(self.name)

                if self.formal_list == None:
                    output += "0\n" 
                else:
                    output += repr(self.formal_list)
                output += repr(self.feat_type) + repr(self.body)
        
        else:
            output = "attribute_init\n"
            output += repr(self.name) + repr(self.feat_type) + repr(self.init)
        
        return output

# Formal
    # output the name and type
class CoolFormal:
    def __init__(self, name, form_type):
        self.name = name
        self.form_type = form_type

    def __repr__(self):
        output = repr(self.name) + repr(self.form_type)
        return output

# Expressions - all begin with outputting the line number

# Assign Expression
    # output assign with the variable and the rhs expression
class CoolExprAssign:
    def __init__(self, lineno, var, rhs):
        self.lineno = lineno
        self.var = var
        self.rhs = rhs
    
    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "assign\n"
        output += repr(self.var) + repr(self.rhs) 
        return output

# Dispatch Expression
    # output:
        # dynamic_dispatch with the expression, method name, and args list
        # static_dispatch with the expression, type, method name, and args list
        # self_dispatch with method name and args list
class CoolExprDispatch:
    def __init__(self, lineno, method, args=None, e=None, static_type=None):
        self.lineno = lineno
        self.e = e
        self.method = method
        self.args = args
        self.static_type = static_type

    def __repr__(self):
        output = str(self.lineno) + "\n"
        
        if self.static_type == None:
            if self.e == None:
                output += "self_dispatch\n"
                output += repr(self.method) 
                if self.args == None:
                    output += "0\n" 
                else:
                    output += repr(self.args)
            else:
                output += "dynamic_dispatch\n"
                output += repr(self.e) + repr(self.method)
                if self.args == None:
                    output += "0\n" 
                else:
                    output += repr(self.args)
        else:
            output += "static_dispatch\n"
            output += repr(self.e) + repr(self.static_type) + repr(self.method)
            if self.args == None:
                output += "0\n" 
            else:
                output += repr(self.args)

        return output#

# If Expression
    # output if, the predicate, the then expression, and the else expression
class CoolExprIf:
    def __init__(self, lineno, predicate, if_then, if_else):
        self.lineno = lineno
        self.predicate = predicate
        self.if_then = if_then
        self.if_else = if_else

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "if\n"
        output += repr(self.predicate) + repr(self.if_then) + repr(self.if_else)
        return output

# While Expression
    # output while, the predicate, and the body expression
class CoolExprWhile:
    def __init__(self, lineno, predicate, body):
        self.lineno = lineno
        self.predicate = predicate
        self.body = body

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "while\n"
        output += repr(self.predicate) + repr(self.body)
        return output

# Block Expression
    # output block and the body expression list
class CoolExprBlock:
    def __init__(self, lineno, body):
        self.lineno = lineno
        self.body = body

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "block\n"
        output += repr(self.body)
        return output

# New Expression
    # output new and the type
class CoolExprNew:
    def __init__(self, lineno, new_class):
        self.lineno = lineno
        self.new_class = new_class

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "new\n"
        output += repr(self.new_class)
        return output

# Math-related expressions
    # output the operation then:
        # operation with the x expression and the y expression
        # operation with the x expression
class CoolExprIsVoidMathConditions:
    def __init__(self, lineno, operation, x, y=None):
        self.lineno = lineno
        self.operation = operation # string with the word for the math in the expr
        self.x = x
        self.y = y

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += self.operation + "\n"
        output += repr(self.x)
        
        if self.y != None:
            output += repr(self.y)

        return output

# Integer Expression
    # output integer with the int constant
class CoolExprInt:
    def __init__(self, lineno, val):
        self.lineno = lineno
        self.val = val

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "integer\n"
        output += self.val + "\n"
        return output

# String Expression
    # output string with the string constant
class CoolExprString:
    def __init__(self, lineno, val):
        self.lineno = lineno
        self.val = val

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "string\n"
        output += self.val + "\n"
        return output

# Identifier Expression
    # output identifier with the associated identifier
class CoolExprID:
    def __init__(self, lineno, val):
        self.lineno = lineno
        self.val = val

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "identifier\n"
        output += repr(self.val)
        return output

# Boolean Expression
    # output the boolean
class CoolExprBool:
    def __init__(self, lineno, val):
        self.lineno = lineno
        self.val = val

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += self.val + "\n"
        return output

# Let Expression
    # output let with the binding list
class CoolExprLet:
    def __init__(self, lineno, body, binding_list=None):
        self.lineno = lineno
        self.body = body
        self.binding_list = binding_list

# Then output the binding list. To output a binding, do either:
    # let_binding_no_init \n variable:identifier type:identifier
    # let_binding_init \n variable:identifier type:identifier value:exp
# Finally, output the expression that is the body of the let.

    def __repr__(self):
        output = str(self.lineno) + "\nlet\n"
        if self.binding_list == None:
            output += "0\n" 
        else:
            output += repr(self.binding_list)
        output += repr(self.body)
        return output

# Let Binding
    # output:
        # let_binding_no_init with the variable and the type
        # let_binding_init wiht the variable, type, and value expression
class CoolExprBinding:
    def __init__(self, var, var_type, init_val=None):
        self.var = var
        self.var_type =  var_type
        self.init_val = init_val

    def __repr__(self):
        
        if self.init_val == None:
            output = "let_binding_no_init\n"
            output += repr(self.var) + repr(self.var_type)
        else:
            output = "let_binding_init\n"
            output += repr(self.var) + repr(self.var_type) + repr(self.init_val)

        return output

# Case Expression
    # output case with the case expression and case list
class CoolExprCase:
    def __init__(self, lineno, case_expr, case_list=None):
        self.lineno = lineno
        self.case_expr = case_expr
        self.case_list = case_list

    def __repr__(self):
        output = str(self.lineno) + "\n"
        output += "case\n" 
        output += repr(self.case_expr)

        if self.case_list == None:
            output += "0\n" 
        else:
            output += repr(self.case_list)  
        return output

# Case Element
    # output the variable, the type, and the body expression
class CoolExprCaseElement:
    def __init__(self, lineno, var, var_type, body):
        self.lineno = lineno
        self.var = var
        self.var_type = var_type
        self.body = body

    def __repr__(self):
        output = repr(self.var)
        output += repr(self.var_type)
        output += repr(self.body)
        return output