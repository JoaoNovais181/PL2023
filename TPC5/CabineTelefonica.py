import re, sys

REGEXMOEDA = re.compile(r"(?:(?P<multiplicador>\d+)x)?(?P<valor>(?:1|2|5|10|20|50))(?P<tipo>[ce])")
REGEXNUM = re.compile(r"(?P<bloq>601|641)?(?P<inter>00)?(?P<nac>2)?(?P<verde>800)?(?P<azuis>808)?\d+")
ESTADO = "POUSAR"
SALDO = 0

def escreveTroco():
    """
    Função utilizada para calcular o troco a devolver e o escrever
    """
    global SALDO
    i, d = divmod(SALDO, 1)
    d = int(round(d*100,0))
    i = int(i)

    troco = []

    for e in [2, 1]:
        t = i//e
        i -= t*e
        if t > 0:
            troco.append(f"{t}x{e}e")

    for c in [50, 20, 10, 5, 2, 1]:
        t = d//c
        d -= t*c
        if t > 0:
            troco.append(f"{t}x{c}c")

    resposta = "maq: \"troco="
    for m in troco[:-1]:
        resposta += f" {m},"
    resposta += f" {troco[-1]}; Volte Sempre!\""
    print(resposta)



def processarMoeda(mtch):
    """
    Função utilizada para processar o valor de uma moeda
    adicionando o seu valor ao saldo global
    """
    global SALDO

    mult = 1
    gd = mtch.groupdict()
    if gd['multiplicador']:
        mult = int(gd['multiplicador'])

    valor = int(gd['valor'])
    if gd['tipo'] == "c":
        SALDO += mult * (valor/100)
    else:
        if valor not in [1,2]:
            return 1
        SALDO += (mult * valor)

    return 0

def lerMoedas(moedas):
    """
    Função utilizada para ler as moedas e escrever algo
    se alguma for inválida, e ainda escrever o SALDO
    """
    resposta = "maq: \""

    for moeda in moedas:
        if not (mtch := REGEXMOEDA.match(moeda)) or processarMoeda(mtch) :
            resposta += f" {moeda} - moeda inválida;"

    i, d = divmod(SALDO, 1)
    resposta += f"saldo = {int(i)}e{int(round(d*100,0))}c\""
    print(resposta)

def processarNum(mtch):
    """
    Função utilizada para processar o número de telefone
    introduzido pelo utilizador
    """
    global SALDO

    gd = mtch.groupdict()

    if len(mtch.group(0)) < 9:
        return "maq: \"Número inválido. Disque um novo número!\""
    if len(mtch.group(0)) > 9:
        if gd['inter'] is None:
            return "maq: \"Número inválido. Disque um novo número!\""
        custo = 1.5
    else:
        if gd['bloq']:
            return "maq: \"Esse número não é permitido neste telefone. Queira discar novo número!\""
        if gd['nac']:
            custo = 0.25
        elif gd['verde']:
            custo = 0
        elif gd['azuis']:
            custo = 0.1
        else:
            return "maq: \"Número inválido. Disque um novo número!\""
    if SALDO < custo:
        return "maq: \"Saldo insuficiente!\""

    SALDO -= custo

    i, d = divmod(SALDO, 1)
    return f"maq: \"saldo = {int(i)}e{int(round(d*100,0))}c\""


def fazChamada(num):
    """
    Função utilizada para ler o número para fazer uma
    chamada e calcular o preço da mesma
    """
    resposta = ""
    mtch = REGEXNUM.match(num)

    if not mtch:
        print("HEY")
        resposta = "maq: \"Número inválido. Disque um novo número!\""
    else:
        resposta = processarNum(mtch)

    print(resposta)

def main():
    global ESTADO
    global SALDO

    for linha in sys.stdin:
        if len(linha) == 0:
            continue

        linha = linha.strip("\n")
        if "=" in linha:
            acao,num = linha.split("=")
        else:
            l = linha.split(" ")
            acao = l[0]
            linha = "".join(l[1::])

        if ESTADO == "POUSAR":
            if acao == "LEVANTAR":
                print("maq: \"Introduza moedas.\"")
                ESTADO = acao
            else:
                print("Input inválido...")
                return 1
        else: # se o ESTADO nao for POUSAR então é LEVANTAR
            if acao == "POUSAR":
                escreveTroco()
                ESTADO = acao
                SALDO = 0
            elif acao == "MOEDA":
                lerMoedas(linha.split(","))
            elif acao == "T":
                fazChamada(num)
            else:
                print("Input inválido...")
                return 1

    return 0

if __name__ == "__main__":
    main()
