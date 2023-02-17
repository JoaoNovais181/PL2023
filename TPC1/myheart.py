from csv import DictReader


def lerInfo (ficheiro):
    dados = []
    with open(ficheiro, encoding="utf-8") as ficheiroCSV:
        leitor = DictReader(ficheiroCSV)
        for linha in leitor:
            linha['idade'] = int(linha['idade'])
            linha['tensão'] = int(linha['tensão'])
            linha['colesterol'] = int(linha['colesterol'])
            linha['batimento'] = int(linha['batimento'])
            linha['temDoença'] = int(linha['temDoença'])
            dados.append(linha)

    return dados


## distribuicao = {}

## idade,sexo,tensão,colesterol,batimento,temDoença

def doentesPorSexo(dados):
    distribuicao = {}
    
    distribuicao['M'] = 0
    distribuicao['F'] = 0

    for entrada in dados:
        if entrada['temDoença'] == 1:
            distribuicao[entrada['sexo']] += 1

    return distribuicao

def doentesPorFaixaEtaria(dados):
    distribuicao = {}



informacao = lerInfo("myheart.csv")
distrPorSexo = doentesPorSexo(informacao)
print(distrPorSexo)
