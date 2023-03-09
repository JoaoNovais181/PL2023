import re, json

def carregarDados ():

    entradas = []
    regex = re.compile(r'^(?P<idPasta>\d+)::(?P<ano>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})::(?P<nome>[ a-zA-Z]+)::(?P<nomePai>[ a-zA-Z]+)::(?P<nomeMae>[ a-zA-Z]+)::(?P<observacoes>[\w,. ]*)::$')

    with open("./processos.txt", "r") as procFile:
        
        for linha in procFile.readlines():
            if entrada := regex.match(linha): 
                entrada = entrada.groupdict()
                entrada['observacoes'] = entrada['observacoes'].split(". ")
                entradas.append(entrada)

    return entradas

def freqPorAno(dados):

    resultados = {}

    for entrada in dados:
        if entrada['ano'] not in resultados.keys():
            resultados[entrada['ano']] = 0
        resultados[entrada['ano']] += 1

    resultados = dict(sorted(resultados.items(), key = lambda e : e[0]))
    
    for key, value in resultados.items():
        print(f"\tAno: {key} --{{nº de processos}}--> {value}")

    return resultados

def freqNomesPorSeculo(dados):

    resultados = {'proprio':{}, 'apelido':{}}

    for entrada in dados:
        nomePartido = entrada['nome'].split(" ")
        nomeProprio = nomePartido[0]
        apelido = nomePartido[-1]
        seculo = (int(entrada['ano']) - 1) // 100 + 1
    
        if seculo not in resultados['proprio']:
            resultados['proprio'][seculo] = {}
            resultados['apelido'][seculo] = {}

        if nomeProprio not in resultados['proprio'][seculo].keys():
            resultados['proprio'][seculo][nomeProprio] = 0

        if apelido not in resultados['apelido'][seculo].keys():
            resultados['apelido'][seculo][apelido] = 0

        resultados['proprio'][seculo][nomeProprio] += 1
        resultados['apelido'][seculo][apelido] += 1
    
    resultados['proprio'] = dict(sorted(resultados['proprio'].items(), key=lambda e : e[0]))

    print("Distribuição de Nomes Próprios:") 
    for seculo, r in resultados['proprio'].items():
        print(f"\t-> Século {seculo}:")

        r = dict(sorted(r.items(), key = lambda e : e[1], reverse=True))

        for nome, freq in list(r.items())[0:5]:
            print(f"\t\tNome: {nome} --{{Frequência}}--> {freq}")

    resultados['apelido'] = dict(sorted(resultados['apelido'].items(), key=lambda e : e[0]))

    print("Distribuição de Apelidos:") 
    for seculo, r in resultados['apelido'].items():
        print(f"\t-> Século {seculo}:")

        r = dict(sorted(r.items(), key = lambda e : e[1], reverse=True))

        for nome, freq in list(r.items())[0:5]:
            print(f"\t\tNome: {nome} --{{Frequência}}--> {freq}")

    return resultados
        
def freqTiposRelacao(dados):

    resultados = {}
    regex = re.compile(r'[a-zA-Z ,]+,([A-Za-z][a-zA-Z ]+)$')

    for entrada in dados:
        for obs in entrada['observacoes']:
            if obs.find("Foi anex")!=-1 or obs.find("com o nome de")!=-1 or obs.find("Assistente")!=-1 or obs.find("Sao")!=-1 or obs.find("Santa")!=-1:
                continue
            if m:=regex.match(obs):
                if m.group(1) not in resultados.keys():
                    resultados[m.group(1)] = 0
                resultados[m.group(1)] += 1

    resultados = dict(sorted(resultados.items(), key=lambda e : e[1]))

    print("Distribuição dos Tipos de Relação:")
    for tipo, freq in resultados.items():
        print(f"\t{tipo} --{{Frequência}}--> {freq}")

    return resultados

def _20PrimJson(dados, nomeFicheiro):
    
    final = {"processos":dados[0:20]}

    with open(nomeFicheiro, "w") as ficheiroJson:
        json.dump(final, ficheiroJson)


dados = carregarDados()
freqPorAno(dados)
freqNomesPorSeculo(dados)
freqTiposRelacao(dados)
_20PrimJson(dados, "processos.json")
