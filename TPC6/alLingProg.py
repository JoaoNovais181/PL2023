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
        # "EXEC_FUNC",
        "LIST_ELEMS",
        "LIST_COMPR",
        "MANUAL_LIST",
        "CYCLE",
        "CONDITIONAL",
        "PROGRAM",
        "COMMENT",
        "BOPEN",
        "BCLOSE"
        )

t_FUNCTION = r"function\s*\w+\((\s*\w+\s*,)*\s*\w+\s*\)"
t_VAR = r"\w+(\[\w+\])?"
t_TYPE = r"\b(int|double|float)\b"
t_EQUALS = r"="
t_LOGIC_OP = r"(\|\||&&|[><&]|==|in)"
t_MATH_OP = r"[+\-*/]"
t_NUMBER = r"\d+(.\d+)"
t_SEMICOLON = r";"
t_PROGRAM = r"\s*(?i:program)\s*\w+"
t_CONDITIONAL = r"if|else"
t_COLON = r","
t_MANUAL_LIST = r"{\s*(\w+\s*,)\s*\w+\s*}"
t_BOPEN = r"\("
t_BCLOSE = r"\)"

def t_CYCLE(t):
    r"(?i:while|for)"
    return t

def t_COMMENT(t):
    r"(/\*(.|\n)*?\*/)|(//.*)"
    pass

def t_SBOPEN(t):
    r"\["
    t.lexer.stack.append("list")
    t.lexer.begin("list")
    t.lexer.filledList = False
    return t

def t_list_SBCLOSE(t):
    r"\]"
    if len(t.lexer.stack) <= 0:
        raise SyntaxError("Closing Square Bracket does not match any Open Square Bracket")
    state = t.lexer.stack.pop(-1)
    if  state != "list":
        raise SyntaxError("List not properly closed")
    t.lexer.begin(t.lexer.stack[-1])
    return t

def t_list_LIST_ELEMS(t):
    r"(\s*\w+\s*,)\s*\w+\s*"
    if t.lexer.filledList:
        raise SyntaxError("Wring Syntax inside list")
    t.lexer.filledList = True
    return t
    
def t_list_LIST_COMPR(t):
    r"\d+(,\d+)?..\d+"
    if t.lexer.filledList:
        raise SyntaxError("Wring Syntax inside list")
    t.lexer.filledList = True   
    return t

def t_CBOPEN(t):
    r"{"
    t.lexer.stack.append("body")
    t.lexer.begin("body")
    return t

def t_body_CBCLOSE(t):
    r"}"
    if len(t.lexer.stack) <= 0:
        raise SyntaxError("Closing Square Bracket does not match any Open Square Bracket")
    state = t.lexer.stack.pop(-1)
    if  state != "body":
        raise SyntaxError("List not properly closed")
    t.lexer.begin(t.lexer.stack[-1])
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_ignore = " \t"
t_list_ignore = " \t"

def t_error(t):
    print(f"Illegal expression: {t.value[0]} in line {t.lexer.lineno}")

def t_list_error(t):
    print(f"Illegal expression: {t.value[0]} in line {t.lexer.lineno}")

lexer = lex.lex()
lexer.filledList = False
lexer.stack = ["INITIAL"]

data = """/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}

/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
"""

lexer.input(data)

while True:
    token = lexer.token()
    if not token:
        break
    print(token)