import sys

print("O programa irá ler até que seja encontrado um EOF\n\nInput:")

texto = ""

## Ler do stdin até ser encontrado o EOF
for linha in sys.stdin:
    texto += linha  ## Concatenar ao texto total a ultima linha lida

print("\nOutput:")

## Tratamento do texto
soma = 0
numAtual = 0
somar = True
aux = ""  ## Variavel que sera usada para detetar o "on" ou "off"

for car in texto:
    if somar and car in "0123456789":
        numAtual = numAtual*10 + int(car)
    else:
        if somar:
            soma += numAtual
            numAtual = 0
        if car == "=":
            print(soma)
        car.lower()
        if somar and car in "off":
            aux += car
            if aux == "off":
                somar = False
                aux = ""
            elif aux not in "off":
                aux = ""
        elif not somar and car in "on":
            aux += car
            if aux == "on":
                somar = True
                aux = ""
            elif aux not in "on":
                aux = ""
