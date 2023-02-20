from csv import DictReader
import matplotlib.pyplot as plt

CECT = "┌" # Canto Esquerdo Cima Tabela
LHT = "─" # Linha Horizontal Tabela
SVCT = "┬" # Separador Vertical Cima Tabela
CDCT = "┐" # Canto Direito Cima Tabela 
SHET = "├" # Separador Horizontal Esquerdo Tabela
CT = "┼" # Cruz Tabela
SHDT = "┤" # Separador Horizontal Direito Tabela
CEBT = "└" # Canto Esquerdo Baixo Tabela
SVBT = "┴" # Separador Vertical Baixo Tabela
CDBT = "┘" # Canto Direito Baixo Tabela
LVT = "│" # Linha Vertical Tabela

def lerInfo (ficheiro):
    dados = []
    with open(ficheiro, encoding="utf-8") as ficheiroCSV:
        leitor = ficheiroCSV.read().split("\n")
        campos = leitor.pop(0).split(",")
        for linha in leitor:
            if len(linha) <= 0:
                continue
            registo = {campo:valor for campo,valor in zip(campos,linha.split(","))} 
            registo['idade'] = int(registo['idade'])
            registo['tensão'] = int(registo['tensão'])
            registo['colesterol'] = int(registo['colesterol'])
            registo['batimento'] = int(registo['batimento'])
            registo['temDoença'] = int(registo['temDoença'])
            dados.append(registo)

    return dados

def doentesPorSexo(dados):
    distribuicao = {}
    
    distribuicao['M'] = [0,0] # [saudaveis, doentes]
    distribuicao['F'] = [0,0] # [saudaveis, doentes]

    for entrada in dados:
        distribuicao[entrada['sexo']][entrada['temDoença']] += 1

    return distribuicao

def doentesPorFaixaEtaria(dados):
    distribuicao = {}

    idadeMax = max(dados, key=lambda doente: doente['idade'])['idade']   
    limMax = idadeMax // 5 * 5 + 5
    limMin = 0
    while limMin < limMax:
        distribuicao[f"[{limMin}-{limMin+4}]"] = [0,0] # [saudaveis, doentes]
        limMin += 5

    for entrada in dados:
        limMin = entrada['idade'] // 5 * 5
        distribuicao[f"[{limMin}-{limMin+4}]"][entrada['temDoença']] += 1

    return distribuicao

def doentesPorNivelColesterol(dados):
    distribuicao = {}

    minColesterol = min(dados, key=lambda doente: doente['colesterol'])['colesterol']
    limMax = (max(dados, key=lambda doente: doente['colesterol'])['colesterol'] - minColesterol) // 10 + 1
    limMin = 0
    while limMin < limMax:
        distribuicao[limMin] = [0,0] # [saudaveis, doentes]
        limMin += 1

    for entrada in dados:
        nivelColesterol = (entrada['colesterol'] - minColesterol) //10
        distribuicao[nivelColesterol][entrada['temDoença']] += 1

    return distribuicao

def imprimeDistribuicao(distribuicao, nomes = None):

    biggestX = max(map(lambda x : len(str(x)), distribuicao.keys()))
    biggestYsaudavel = max(map(lambda y : len(str(y[0])), distribuicao.values()))
    biggestYdoente = max(map(lambda y : len(str(y[1])), distribuicao.values()))

    if nomes is not None and len(nomes)==3:
        biggestX = max(biggestX, len(str(nomes[0])))
        biggestYsaudavel = max(biggestYsaudavel, len(str(nomes[1])))
        biggestYdoente = max(biggestYdoente, len(str(nomes[2])))

    first = True
    
    if nomes is not None and len(nomes)==3:
        print(CECT + LHT*biggestX + SVCT + LHT*biggestYsaudavel + SVCT + LHT*biggestYdoente + CDCT)
        print(LVT + f"{nomes[0]:^{biggestX}}" + LVT + f"{nomes[1]:^{biggestYsaudavel}}" + LVT + f"{nomes[2]:^{biggestYdoente}}" + LVT)
        first = False

    for x,y in distribuicao.items():
        if first:
            print(CECT + LHT*biggestX + SVCT + LHT*biggestYsaudavel + SVCT + LHT*biggestYdoente + CDCT)
        else:
            print(SHET + LHT*biggestX + CT + LHT*biggestYsaudavel + CT + LHT*biggestYdoente + SHDT)
        
        print(LVT + f"{x:^{biggestX}}" + LVT + f"{y[0]:^{biggestYsaudavel}}" + LVT + f"{y[1]:^{biggestYdoente}}" + LVT)

    print(CEBT + LHT*biggestX + SVBT + LHT*biggestYsaudavel + SVBT + LHT*biggestYdoente + CDBT)

def graficoBarras(distribuicao, titulo):

    x = []
    lastX = 0.5
    for key in distribuicao.keys():
        x.append(lastX)
        lastX+=1

    height = list(map(lambda x : x[0], distribuicao.values()))
    height2 = list(map(lambda x : x[1], distribuicao.values()))

    plt.bar(x, height, width=0.4, color="#FFAAAA")
    plt.bar(list(map(lambda x : x+0.4, x)), height2, alpha=0.5, width=0.4, color="#AAAAFF")
    plt.xticks(list(map(lambda x : x+0.2, x)), list(distribuicao.keys()), rotation="vertical")
    plt.subplots_adjust(bottom=0.15)
    plt.title(titulo + "\nVermelho=Saudável e Azul=Doente")
    #  plt.table(colLabels=["Saudável","Doente"], colColours=["#FFAAAA","#AAAAFF"], cellText=[])
    plt.show()

informacao = lerInfo("myheart.csv")
distrPorSexo = doentesPorSexo(informacao)
distrPorFaixaEtaria = doentesPorFaixaEtaria(informacao)
distrPorNivelColesterol = doentesPorNivelColesterol(informacao)
imprimeDistribuicao(distrPorSexo, ["Sexo","Saudáveis","Doentes"])
imprimeDistribuicao(distrPorFaixaEtaria, ["Faixa Etária", "Saudáveis", "Doentes"])
imprimeDistribuicao(distrPorNivelColesterol, ["Nível Colesterol", "Saudáveis", "Doentes"])
graficoBarras(distrPorFaixaEtaria, "Distribuição por Faixa Etária")
graficoBarras(distrPorSexo, "Distribuição por Sexo")
graficoBarras(distrPorNivelColesterol, "Distribuição por nível de colesterol")
