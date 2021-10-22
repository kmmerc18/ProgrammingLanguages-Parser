#3aeee2ffb6bdcec698011572b6bbcaf180807419 

# define a class in python for our tokens
class Token:
    def __init__(self, lineno, token, lexeme):
        """
        lineno -  line number and our lexer position
        token - token type (convert to upper case)
        lexeme - actual text (lexeme)
        """
        self.type = token.upper()
        self.value = lexeme
        self.lineno = int(lineno)
        self.lexerpos = int(lineno)

    def __str__(self):
        return "Token({}, {}, {})".format(self.lineno, self.type, self.value)

    def __repr__(self):
        return str(self)

class Lexer: 
    def __init__(self, f):
        """
        f - file-like object containing the CL-lex token information
        """
        # creates a list of all the lines from f
        lines = f.readlines()

        # a list of tokens
        self.__tokens = []  # private variable

        # keep track of the current line
        i = 0
        while i < len(lines):
            line = lines[i]
            # FIXME this might not be the best option
            tok_type = lines[i+1].strip()

            if tok_type in ["identifier", "integer", "string", "type"]:
                lexeme = lines[i+2].strip()
                i += 1
            else:
                lexeme = tok_type

            # increment i by 2
            i += 2

            self.__tokens.append(Token(line, tok_type, lexeme))

        assert(i == len(lines))

        # create an iterator from our __tokens attribute
        self.token_stream = iter(self.__tokens)
    
    def token(self):
        """
        return the next token object or None if there are no more
        """
        try:
            return next(self.token_stream)
        except StopIteration:
            return None
