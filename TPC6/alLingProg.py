import ply.lex as lex

states = (
        ("list", "exclusive"),
        ("body", "inclusive")
        )

tokens = (
        "VAR",
        "TYPE",
        "FUNCTION",
        "CBOPEN",
        "CBCLOSE",
        "EQUALS",
        "LOGIC_OP",
        "MATH_OP",
        "NUMBER",
        "SBOPEN",
        "SBCLOSE",
        "SEMICOLON",
        "COLON",
        "EXEC_FUNC",
        "LIST_ELEMS",
        "LIST_COMPR",
        "MANUAL_LIST",
        "CYCLE",
        "CONDITIONAL",
        "PROGRAM",
        "COMMENT"
        )

t_VAR = r"\w+(\[\w+\])"
t_TYPE = r"(int|double|float)"
t_FUNCTION = r"function *\w+\(( *\w+ *,)* *\w+\*\)"
t_EQUALS = r"="
t_LOGIC_OP = r"\|\||&&|[><&]|==|in"
t_MATH_OP = r"[+\-*/]"
t_NUMBER = r"\d+(.\d+)"
t_SEMICOLON = r";"
t_EXEC_FUNC = r"\w+\(( *\w+ *,)* *\w+\*\)"
t_PROGRAM = r"program *\w+"
t_CYCLE = r"while|for"
t_CONDITIONAL = r"if|else"
t_COLON = r","
t_MANUAL_LIST = r"{ *(\w+ *,) *\w+ *}"

def t_COMMENT(t):
    r"(/\*(.|\n)*?\*/)|(//.*)"
    pass

def t_SBOPEN(t):
    r"\["
    t.lexer.push_state("list")

def t_SBCLOSE(t):
    r"\]"
    t.lexer.pop_state()

t_ignore = " \t"
